import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from models import Job, AnalysisResult
from schemas import JobMatchResponse
from database import SessionLocal

logger = logging.getLogger(__name__)

class JobMatcher:
    def __init__(self):
        """Initialize the job matcher with similarity algorithms"""
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Skill importance weights
        self.skill_weights = {
            'programming_languages': 1.0,
            'frameworks': 0.9,
            'tools': 0.8,
            'databases': 0.8,
            'cloud_platforms': 0.7,
            'soft_skills': 0.6
        }
        
        # Experience level matching
        self.experience_levels = {
            'entry': (0, 2),
            'junior': (1, 3),
            'mid-level': (2, 5),
            'senior': (4, 8),
            'lead': (6, 12),
            'principal': (8, 15),
            'executive': (10, 20)
        }

    async def find_matches(self, analysis: AnalysisResult, limit: int = 10) -> List[JobMatchResponse]:
        """Find job matches for a resume analysis"""
        try:
            db = SessionLocal()
            
            # Get all active jobs
            jobs = db.query(Job).filter(Job.is_active == True).all()
            
            if not jobs:
                logger.warning("No active jobs found in database")
                return []
            
            # Calculate match scores for each job
            matches = []
            for job in jobs:
                match_score = self._calculate_match_score(analysis, job)
                
                if match_score > 0.3:  # Only include jobs with reasonable match
                    match_reasons = self._get_match_reasons(analysis, job, match_score)
                    missing_skills = self._get_missing_skills(analysis, job)
                    extra_skills = self._get_extra_skills(analysis, job)
                    
                    job_match = JobMatchResponse(
                        job_id=job.id,
                        title=job.title,
                        company=job.company,
                        location=job.location,
                        salary_range=job.salary_range,
                        description=job.description,
                        required_skills=json.loads(job.required_skills) if job.required_skills else [],
                        preferred_skills=json.loads(job.preferred_skills) if job.preferred_skills else [],
                        industry=job.industry,
                        experience_level=job.experience_level,
                        employment_type=job.employment_type,
                        remote_work=job.remote_work,
                        match_score=round(match_score, 2),
                        match_reasons=match_reasons,
                        missing_skills=missing_skills,
                        extra_skills=extra_skills,
                        company_size=job.company_size,
                        benefits=json.loads(job.benefits) if job.benefits else [],
                        requirements=json.loads(job.requirements) if job.requirements else [],
                        posted_date=job.posted_date,
                        application_deadline=job.application_deadline
                    )
                    
                    matches.append(job_match)
            
            db.close()
            
            # Sort by match score and return top matches
            matches.sort(key=lambda x: x.match_score, reverse=True)
            return matches[:limit]
            
        except Exception as e:
            logger.error(f"Error finding job matches: {str(e)}")
            raise Exception(f"Job matching failed: {str(e)}")

    def _calculate_match_score(self, analysis: AnalysisResult, job: Job) -> float:
        """Calculate overall match score between analysis and job"""
        try:
            # Extract skills from analysis
            analysis_skills = json.loads(analysis.skills) if analysis.skills else []
            analysis_skills_lower = [skill.lower() for skill in analysis_skills]
            
            # Extract required skills from job
            required_skills = json.loads(job.required_skills) if job.required_skills else []
            required_skills_lower = [skill.lower() for skill in required_skills]
            
            # Calculate different match components
            skills_score = self._calculate_skills_match(analysis_skills_lower, required_skills_lower)
            experience_score = self._calculate_experience_match(analysis.experience_years, job.experience_level)
            industry_score = self._calculate_industry_match(analysis.industry, job.industry)
            location_score = self._calculate_location_match(analysis, job)
            
            # Weighted combination
            overall_score = (
                skills_score * 0.4 +
                experience_score * 0.3 +
                industry_score * 0.2 +
                location_score * 0.1
            )
            
            return min(overall_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating match score: {str(e)}")
            return 0.0

    def _calculate_skills_match(self, analysis_skills: List[str], required_skills: List[str]) -> float:
        """Calculate skills matching score"""
        if not required_skills:
            return 0.5  # Neutral score if no required skills specified
        
        if not analysis_skills:
            return 0.0
        
        # Calculate exact matches
        exact_matches = sum(1 for skill in required_skills if skill in analysis_skills)
        exact_score = exact_matches / len(required_skills)
        
        # Calculate partial matches using TF-IDF similarity
        if len(analysis_skills) > 1 and len(required_skills) > 1:
            try:
                # Create text representations
                analysis_text = " ".join(analysis_skills)
                required_text = " ".join(required_skills)
                
                # Calculate TF-IDF similarity
                tfidf_matrix = self.vectorizer.fit_transform([analysis_text, required_text])
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                
                # Combine exact and similarity scores
                combined_score = (exact_score * 0.7) + (similarity * 0.3)
                return min(combined_score, 1.0)
                
            except Exception as e:
                logger.warning(f"TF-IDF similarity calculation failed: {str(e)}")
                return exact_score
        
        return exact_score

    def _calculate_experience_match(self, experience_years: float, job_level: str) -> float:
        """Calculate experience level matching score"""
        if not job_level or experience_years is None:
            return 0.5
        
        job_level_lower = job_level.lower()
        
        # Get expected experience range for job level
        if job_level_lower in self.experience_levels:
            min_exp, max_exp = self.experience_levels[job_level_lower]
        else:
            # Default ranges for unknown levels
            if 'senior' in job_level_lower or 'lead' in job_level_lower:
                min_exp, max_exp = 5, 10
            elif 'junior' in job_level_lower or 'entry' in job_level_lower:
                min_exp, max_exp = 0, 3
            else:
                min_exp, max_exp = 2, 6
        
        # Calculate match score
        if min_exp <= experience_years <= max_exp:
            return 1.0  # Perfect match
        elif experience_years < min_exp:
            # Underqualified - score decreases with gap
            gap = min_exp - experience_years
            return max(0.0, 1.0 - (gap * 0.2))
        else:
            # Overqualified - still good but not perfect
            gap = experience_years - max_exp
            return max(0.5, 1.0 - (gap * 0.1))

    def _calculate_industry_match(self, analysis_industry: str, job_industry: str) -> float:
        """Calculate industry matching score"""
        if not analysis_industry or not job_industry:
            return 0.5
        
        analysis_industry_lower = analysis_industry.lower()
        job_industry_lower = job_industry.lower()
        
        # Exact match
        if analysis_industry_lower == job_industry_lower:
            return 1.0
        
        # Related industries
        related_industries = {
            'technology': ['software', 'it', 'tech', 'computer'],
            'finance': ['banking', 'financial', 'investment'],
            'healthcare': ['medical', 'health', 'pharmaceutical'],
            'education': ['academic', 'teaching', 'university'],
            'marketing': ['advertising', 'digital', 'social media'],
            'sales': ['business development', 'account management'],
            'consulting': ['advisory', 'strategy', 'management'],
            'manufacturing': ['production', 'engineering', 'industrial']
        }
        
        # Check for related industries
        for industry, related in related_industries.items():
            if (industry in analysis_industry_lower and any(r in job_industry_lower for r in related)) or \
               (industry in job_industry_lower and any(r in analysis_industry_lower for r in related)):
                return 0.8
        
        # Check for keyword overlap
        analysis_words = set(analysis_industry_lower.split())
        job_words = set(job_industry_lower.split())
        
        if analysis_words & job_words:  # If there's any overlap
            return 0.6
        
        return 0.3  # Different industries

    def _calculate_location_match(self, analysis: AnalysisResult, job: Job) -> float:
        """Calculate location matching score"""
        # This is a simplified implementation
        # In a real system, you'd use geocoding and distance calculations
        
        if not job.location:
            return 0.5  # Remote or location not specified
        
        # Check for remote work
        if job.remote_work:
            return 1.0  # Perfect match for remote work
        
        # For now, return a neutral score
        # In a real implementation, you'd check if the candidate's location
        # matches the job location or is within a reasonable distance
        return 0.7

    def _get_match_reasons(self, analysis: AnalysisResult, job: Job, match_score: float) -> List[str]:
        """Get reasons why this job is a good match"""
        reasons = []
        
        # Skills match reasons
        analysis_skills = json.loads(analysis.skills) if analysis.skills else []
        required_skills = json.loads(job.required_skills) if job.required_skills else []
        
        if analysis_skills and required_skills:
            matching_skills = [skill for skill in required_skills 
                             if skill.lower() in [s.lower() for s in analysis_skills]]
            
            if matching_skills:
                reasons.append(f"Matches {len(matching_skills)} required skills: {', '.join(matching_skills[:3])}")
        
        # Experience match reasons
        if analysis.experience_years and job.experience_level:
            if 'senior' in job.experience_level.lower() and analysis.experience_years >= 5:
                reasons.append("Experience level matches senior position requirements")
            elif 'junior' in job.experience_level.lower() and analysis.experience_years <= 3:
                reasons.append("Experience level suitable for junior position")
        
        # Industry match reasons
        if analysis.industry and job.industry:
            if analysis.industry.lower() == job.industry.lower():
                reasons.append(f"Industry experience in {analysis.industry}")
        
        # Education match reasons
        if analysis.education_score and analysis.education_score >= 80:
            reasons.append("Strong educational background")
        
        # Overall score reasons
        if match_score >= 0.8:
            reasons.append("Excellent overall match")
        elif match_score >= 0.6:
            reasons.append("Good overall match")
        elif match_score >= 0.4:
            reasons.append("Moderate match")
        
        return reasons[:3]  # Limit to top 3 reasons

    def _get_missing_skills(self, analysis: AnalysisResult, job: Job) -> List[str]:
        """Get skills that are required but missing from the resume"""
        analysis_skills = json.loads(analysis.skills) if analysis.skills else []
        required_skills = json.loads(job.required_skills) if job.required_skills else []
        
        if not analysis_skills or not required_skills:
            return []
        
        analysis_skills_lower = [skill.lower() for skill in analysis_skills]
        missing_skills = [skill for skill in required_skills 
                         if skill.lower() not in analysis_skills_lower]
        
        return missing_skills[:5]  # Limit to top 5 missing skills

    def _get_extra_skills(self, analysis: AnalysisResult, job: Job) -> List[str]:
        """Get skills that the candidate has but aren't required for the job"""
        analysis_skills = json.loads(analysis.skills) if analysis.skills else []
        required_skills = json.loads(job.required_skills) if job.required_skills else []
        preferred_skills = json.loads(job.preferred_skills) if job.preferred_skills else []
        
        if not analysis_skills:
            return []
        
        all_job_skills = [skill.lower() for skill in required_skills + preferred_skills]
        extra_skills = [skill for skill in analysis_skills 
                       if skill.lower() not in all_job_skills]
        
        return extra_skills[:5]  # Limit to top 5 extra skills

    async def get_job_recommendations(self, analysis: AnalysisResult, limit: int = 5) -> List[Dict[str, Any]]:
        """Get personalized job recommendations based on analysis"""
        try:
            matches = await self.find_matches(analysis, limit * 2)  # Get more matches for filtering
            
            recommendations = []
            for match in matches:
                recommendation = {
                    'job_id': match.job_id,
                    'title': match.title,
                    'company': match.company,
                    'match_score': match.match_score,
                    'why_recommended': self._get_recommendation_reason(match),
                    'next_steps': self._get_next_steps(match)
                }
                recommendations.append(recommendation)
            
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error getting job recommendations: {str(e)}")
            return []

    def _get_recommendation_reason(self, match: JobMatchResponse) -> str:
        """Get reason why this job is recommended"""
        if match.match_score >= 0.8:
            return "Excellent match based on your skills and experience"
        elif match.match_score >= 0.6:
            return "Good match with some areas for growth"
        else:
            return "Potential match with opportunity to learn new skills"

    def _get_next_steps(self, match: JobMatchResponse) -> List[str]:
        """Get suggested next steps for the job application"""
        steps = []
        
        if match.missing_skills:
            steps.append(f"Consider learning: {', '.join(match.missing_skills[:2])}")
        
        steps.append("Tailor your resume to highlight relevant experience")
        steps.append("Prepare for technical interviews in your field")
        
        if match.remote_work:
            steps.append("Highlight your remote work experience")
        
        return steps[:3]

    async def analyze_job_market_trends(self) -> Dict[str, Any]:
        """Analyze current job market trends"""
        try:
            db = SessionLocal()
            
            # Get all active jobs
            jobs = db.query(Job).filter(Job.is_active == True).all()
            
            if not jobs:
                return {"error": "No jobs found for analysis"}
            
            # Analyze trends
            trends = {
                'total_jobs': len(jobs),
                'top_skills': self._get_top_skills(jobs),
                'industry_distribution': self._get_industry_distribution(jobs),
                'experience_level_distribution': self._get_experience_distribution(jobs),
                'salary_ranges': self._get_salary_ranges(jobs),
                'remote_work_percentage': self._get_remote_work_percentage(jobs)
            }
            
            db.close()
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing job market trends: {str(e)}")
            return {"error": str(e)}

    def _get_top_skills(self, jobs: List[Job]) -> List[Dict[str, Any]]:
        """Get most in-demand skills"""
        skill_counts = {}
        
        for job in jobs:
            if job.required_skills:
                skills = json.loads(job.required_skills)
                for skill in skills:
                    skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Sort by count and return top 10
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        return [{"skill": skill, "count": count} for skill, count in top_skills]

    def _get_industry_distribution(self, jobs: List[Job]) -> List[Dict[str, Any]]:
        """Get industry distribution"""
        industry_counts = {}
        
        for job in jobs:
            if job.industry:
                industry_counts[job.industry] = industry_counts.get(job.industry, 0) + 1
        
        return [{"industry": industry, "count": count} 
                for industry, count in industry_counts.items()]

    def _get_experience_distribution(self, jobs: List[Job]) -> List[Dict[str, Any]]:
        """Get experience level distribution"""
        experience_counts = {}
        
        for job in jobs:
            if job.experience_level:
                experience_counts[job.experience_level] = experience_counts.get(job.experience_level, 0) + 1
        
        return [{"level": level, "count": count} 
                for level, count in experience_counts.items()]

    def _get_salary_ranges(self, jobs: List[Job]) -> List[Dict[str, Any]]:
        """Get salary range distribution"""
        salary_ranges = {}
        
        for job in jobs:
            if job.salary_range:
                salary_ranges[job.salary_range] = salary_ranges.get(job.salary_range, 0) + 1
        
        return [{"range": range_str, "count": count} 
                for range_str, count in salary_ranges.items()]

    def _get_remote_work_percentage(self, jobs: List[Job]) -> float:
        """Get percentage of jobs offering remote work"""
        if not jobs:
            return 0.0
        
        remote_jobs = sum(1 for job in jobs if job.remote_work)
        return round((remote_jobs / len(jobs)) * 100, 2)
