from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()

def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """
    Initialize database with sample data
    """
    try:
        # Import all models to ensure they are registered
        from models import User, Resume, Job, AnalysisResult
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

def create_sample_data():
    """
    Create sample data for demonstration
    """
    from models import Job
    from datetime import datetime
    import json
    
    db = SessionLocal()
    try:
        # Check if sample data already exists
        if db.query(Job).count() > 0:
            logger.info("Sample data already exists")
            return
        
        # Sample jobs data
        sample_jobs = [
            {
                "title": "Senior Python Developer",
                "company": "TechCorp Inc.",
                "location": "San Francisco, CA",
                "salary_range": "$120,000 - $150,000",
                "description": "We are looking for an experienced Python developer to join our team...",
                "required_skills": json.dumps(["Python", "Django", "PostgreSQL", "AWS", "Docker"]),
                "industry": "Technology",
                "experience_level": "Senior",
                "posted_date": datetime.utcnow()
            },
            {
                "title": "Data Scientist",
                "company": "DataFlow Solutions",
                "location": "New York, NY",
                "salary_range": "$100,000 - $130,000",
                "description": "Join our data science team to work on cutting-edge ML projects...",
                "required_skills": json.dumps(["Python", "Machine Learning", "TensorFlow", "SQL", "Statistics"]),
                "industry": "Data Science",
                "experience_level": "Mid-Level",
                "posted_date": datetime.utcnow()
            },
            {
                "title": "Frontend Developer",
                "company": "WebCraft Studios",
                "location": "Austin, TX",
                "salary_range": "$80,000 - $110,000",
                "description": "Create beautiful and responsive web applications...",
                "required_skills": json.dumps(["React", "JavaScript", "TypeScript", "CSS", "HTML"]),
                "industry": "Technology",
                "experience_level": "Mid-Level",
                "posted_date": datetime.utcnow()
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudScale Technologies",
                "location": "Seattle, WA",
                "salary_range": "$110,000 - $140,000",
                "description": "Manage and scale our cloud infrastructure...",
                "required_skills": json.dumps(["AWS", "Docker", "Kubernetes", "Terraform", "Linux"]),
                "industry": "Technology",
                "experience_level": "Senior",
                "posted_date": datetime.utcnow()
            },
            {
                "title": "Product Manager",
                "company": "InnovateLabs",
                "location": "Boston, MA",
                "salary_range": "$90,000 - $120,000",
                "description": "Lead product development and strategy...",
                "required_skills": json.dumps(["Product Management", "Agile", "Analytics", "Leadership", "Strategy"]),
                "industry": "Product",
                "experience_level": "Mid-Level",
                "posted_date": datetime.utcnow()
            }
        ]
        
        # Insert sample jobs
        for job_data in sample_jobs:
            job = Job(**job_data)
            db.add(job)
        
        db.commit()
        logger.info(f"Created {len(sample_jobs)} sample jobs")
        
    except Exception as e:
        logger.error(f"Error creating sample data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
