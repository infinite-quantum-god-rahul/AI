from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ResumeUploadResponse(BaseModel):
    resume_id: int
    filename: str
    message: str

class SkillAnalysis(BaseModel):
    skill: str
    confidence: float
    category: str  # Technical, Soft, Language, etc.

class EducationInfo(BaseModel):
    degree: str
    institution: str
    graduation_year: Optional[int] = None
    gpa: Optional[float] = None

class ExperienceInfo(BaseModel):
    title: str
    company: str
    duration: str
    description: str
    skills_used: List[str]

class ResumeAnalysisResponse(BaseModel):
    # Basic Information
    skills: List[SkillAnalysis]
    experience_years: float
    education_level: str
    industry: str
    
    # Detailed Information
    job_titles: List[str]
    companies: List[str]
    education: List[EducationInfo]
    experience: List[ExperienceInfo]
    
    # Scores
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    
    # Recommendations
    suggestions: List[str]
    strengths: List[str]
    weaknesses: List[str]
    
    # Metadata
    analysis_date: datetime
    processing_time: float

class JobMatchResponse(BaseModel):
    job_id: int
    title: str
    company: str
    location: str
    salary_range: Optional[str] = None
    description: str
    required_skills: List[str]
    preferred_skills: List[str] = []
    industry: str
    experience_level: str
    employment_type: str
    remote_work: bool
    
    # Match Information
    match_score: float
    match_reasons: List[str]
    missing_skills: List[str] = []
    extra_skills: List[str] = []
    
    # Additional Information
    company_size: Optional[str] = None
    benefits: List[str] = []
    requirements: List[str] = []
    posted_date: datetime
    application_deadline: Optional[datetime] = None

class JobSearchRequest(BaseModel):
    keywords: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    experience_level: Optional[str] = None
    employment_type: Optional[str] = None
    remote_work: Optional[bool] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    limit: int = 20
    offset: int = 0

class ResumeSearchRequest(BaseModel):
    skills: List[str] = []
    experience_years: Optional[float] = None
    education_level: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    limit: int = 20
    offset: int = 0

class DashboardAnalytics(BaseModel):
    total_resumes: int
    total_jobs: int
    total_analyses: int
    recent_analyses: List[Dict[str, Any]]
    top_skills: List[Dict[str, Any]]
    industry_distribution: List[Dict[str, Any]]
    average_scores: Dict[str, float]

class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: datetime
    request_id: Optional[str] = None

class SuccessResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime

class FileUploadResponse(BaseModel):
    filename: str
    file_size: int
    file_type: str
    upload_date: datetime
    message: str

class BatchAnalysisRequest(BaseModel):
    resume_ids: List[int]
    options: Optional[Dict[str, Any]] = {}

class BatchAnalysisResponse(BaseModel):
    total_processed: int
    successful: int
    failed: int
    results: List[ResumeAnalysisResponse]
    errors: List[ErrorResponse]

class UserProfile(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    total_resumes: int
    total_analyses: int
    average_score: Optional[float] = None

class NotificationSettings(BaseModel):
    email_notifications: bool = True
    job_matches: bool = True
    analysis_complete: bool = True
    weekly_summary: bool = True

class UserSettings(BaseModel):
    profile: UserProfile
    notifications: NotificationSettings
    preferences: Dict[str, Any] = {}

class APIUsageStats(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    last_request: Optional[datetime] = None
    rate_limit_remaining: int
    rate_limit_reset: datetime
