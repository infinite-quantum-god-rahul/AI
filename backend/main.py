from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
import os
from typing import List, Optional
import logging
from datetime import datetime, timedelta
import json

from database import get_db, engine, Base
from models import Resume, Job, User, AnalysisResult
from schemas import (
    ResumeAnalysisResponse, 
    JobMatchResponse, 
    UserCreate, 
    UserResponse,
    ResumeUploadResponse
)
from services.resume_analyzer import ResumeAnalyzer
from services.job_matcher import JobMatcher
from services.auth_service import AuthService
from utils.file_processor import FileProcessor
from utils.error_handler import ErrorHandler
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Analyzer & Job Matching Platform",
    description="Advanced AI-powered resume analysis and job matching system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize services
resume_analyzer = ResumeAnalyzer()
job_matcher = JobMatcher()
auth_service = AuthService()
file_processor = FileProcessor()
error_handler = ErrorHandler()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Resume Analyzer & Job Matching Platform",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        return await auth_service.register_user(user_data, db)
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_handler.handle_error(e)
        )

@app.post("/api/auth/login")
async def login_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    try:
        return await auth_service.login_user(user_data, db)
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_handler.handle_error(e)
        )

@app.post("/api/resume/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Upload and process resume file"""
    try:
        # Validate file
        if not file_processor.is_valid_file(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Please upload PDF or DOCX files only."
            )
        
        # Process file
        file_content = await file_processor.process_file(file)
        
        # Save to database
        resume = Resume(
            filename=file.filename,
            content=file_content,
            user_id=user_id,
            upload_date=datetime.utcnow()
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return ResumeUploadResponse(
            resume_id=resume.id,
            filename=file.filename,
            message="Resume uploaded successfully"
        )
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_handler.handle_error(e)
        )

@app.post("/api/resume/analyze/{resume_id}", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """Analyze resume using AI"""
    try:
        # Get resume from database
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        # Analyze resume
        analysis_result = await resume_analyzer.analyze_resume(resume.content)
        
        # Save analysis result
        analysis = AnalysisResult(
            resume_id=resume_id,
            skills=json.dumps(analysis_result.skills),
            experience_years=analysis_result.experience_years,
            education_level=analysis_result.education_level,
            industry=analysis_result.industry,
            score=analysis_result.overall_score,
            suggestions=json.dumps(analysis_result.suggestions),
            analysis_date=datetime.utcnow()
        )
        db.add(analysis)
        db.commit()
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_handler.handle_error(e)
        )

@app.get("/api/jobs/match/{resume_id}", response_model=List[JobMatchResponse])
async def get_job_matches(
    resume_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get job matches for a resume"""
    try:
        # Get resume and analysis
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        analysis = db.query(AnalysisResult).filter(
            AnalysisResult.resume_id == resume_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume analysis not found. Please analyze the resume first."
            )
        
        # Get job matches
        matches = await job_matcher.find_matches(analysis, limit)
        
        return matches
        
    except Exception as e:
        logger.error(f"Job matching error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_handler.handle_error(e)
        )

@app.get("/api/jobs", response_model=List[JobMatchResponse])
async def get_all_jobs(
    skip: int = 0,
    limit: int = 20,
    industry: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all available jobs with optional filtering"""
    try:
        query = db.query(Job)
        
        if industry:
            query = query.filter(Job.industry.ilike(f"%{industry}%"))
        
        jobs = query.offset(skip).limit(limit).all()
        
        return [
            JobMatchResponse(
                job_id=job.id,
                title=job.title,
                company=job.company,
                location=job.location,
                salary_range=job.salary_range,
                description=job.description,
                required_skills=json.loads(job.required_skills) if job.required_skills else [],
                match_score=0.0,
                match_reasons=[]
            )
            for job in jobs
        ]
        
    except Exception as e:
        logger.error(f"Jobs fetch error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_handler.handle_error(e)
        )

@app.get("/api/analytics/dashboard")
async def get_dashboard_analytics(db: Session = Depends(get_db)):
    """Get dashboard analytics"""
    try:
        total_resumes = db.query(Resume).count()
        total_jobs = db.query(Job).count()
        total_analyses = db.query(AnalysisResult).count()
        
        # Get recent analyses
        recent_analyses = db.query(AnalysisResult).order_by(
            AnalysisResult.analysis_date.desc()
        ).limit(5).all()
        
        return {
            "total_resumes": total_resumes,
            "total_jobs": total_jobs,
            "total_analyses": total_analyses,
            "recent_analyses": [
                {
                    "id": analysis.id,
                    "resume_id": analysis.resume_id,
                    "score": analysis.score,
                    "industry": analysis.industry,
                    "analysis_date": analysis.analysis_date.isoformat()
                }
                for analysis in recent_analyses
            ]
        }
        
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_handler.handle_error(e)
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
