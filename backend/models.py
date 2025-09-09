from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    file_size = Column(Integer)
    file_type = Column(String(50))
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    analyses = relationship("AnalysisResult", back_populates="resume")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False)
    salary_range = Column(String(100))
    description = Column(Text, nullable=False)
    required_skills = Column(Text)  # JSON string
    preferred_skills = Column(Text)  # JSON string
    industry = Column(String(100), index=True)
    experience_level = Column(String(50))  # Entry, Mid-Level, Senior, Executive
    employment_type = Column(String(50))  # Full-time, Part-time, Contract, Internship
    remote_work = Column(Boolean, default=False)
    posted_date = Column(DateTime, default=datetime.utcnow)
    application_deadline = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Additional fields for better matching
    company_size = Column(String(50))  # Startup, Small, Medium, Large, Enterprise
    benefits = Column(Text)  # JSON string
    requirements = Column(Text)  # JSON string

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    
    # Extracted information
    skills = Column(Text)  # JSON string of extracted skills
    experience_years = Column(Float)
    education_level = Column(String(100))
    industry = Column(String(100))
    job_titles = Column(Text)  # JSON string of job titles
    companies = Column(Text)  # JSON string of companies
    
    # Analysis scores
    overall_score = Column(Float)
    skills_score = Column(Float)
    experience_score = Column(Float)
    education_score = Column(Float)
    
    # Suggestions and recommendations
    suggestions = Column(Text)  # JSON string of suggestions
    strengths = Column(Text)  # JSON string of strengths
    weaknesses = Column(Text)  # JSON string of weaknesses
    
    # Metadata
    analysis_date = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)  # Time taken to process in seconds
    model_version = Column(String(50), default="1.0")
    
    # Relationships
    resume = relationship("Resume", back_populates="analyses")

class JobMatch(Base):
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    
    # Match scores
    overall_match_score = Column(Float, nullable=False)
    skills_match_score = Column(Float)
    experience_match_score = Column(Float)
    location_match_score = Column(Float)
    salary_match_score = Column(Float)
    
    # Match reasons
    match_reasons = Column(Text)  # JSON string of reasons
    missing_skills = Column(Text)  # JSON string of missing skills
    extra_skills = Column(Text)  # JSON string of extra skills
    
    # Metadata
    match_date = Column(DateTime, default=datetime.utcnow)
    is_viewed = Column(Boolean, default=False)
    is_applied = Column(Boolean, default=False)
    
    # Relationships
    resume = relationship("Resume")
    job = relationship("Job")

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String(255), unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Relationships
    user = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(Integer, nullable=True)
    details = Column(Text)  # JSON string of additional details
    ip_address = Column(String(45))
    user_agent = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
