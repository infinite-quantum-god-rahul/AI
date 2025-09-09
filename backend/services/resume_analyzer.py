import spacy
import re
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from schemas import ResumeAnalysisResponse, SkillAnalysis, EducationInfo, ExperienceInfo

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    def __init__(self):
        """Initialize the resume analyzer with NLP models and skill databases"""
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Please install: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Initialize NLTK components
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Skill databases
        self.technical_skills = self._load_technical_skills()
        self.soft_skills = self._load_soft_skills()
        self.programming_languages = self._load_programming_languages()
        self.frameworks = self._load_frameworks()
        self.tools = self._load_tools()
        
        # Education keywords
        self.education_keywords = {
            'phd': 'Doctorate',
            'doctorate': 'Doctorate',
            'master': 'Masters',
            'bachelor': 'Bachelors',
            'associate': 'Associates',
            'diploma': 'Diploma',
            'certificate': 'Certificate',
            'high school': 'High School'
        }
        
        # Industry keywords
        self.industry_keywords = {
            'technology': ['software', 'tech', 'it', 'computer', 'programming', 'development'],
            'finance': ['banking', 'financial', 'investment', 'accounting', 'finance'],
            'healthcare': ['medical', 'health', 'hospital', 'pharmaceutical', 'clinical'],
            'education': ['teaching', 'education', 'academic', 'university', 'school'],
            'marketing': ['marketing', 'advertising', 'brand', 'digital', 'social media'],
            'sales': ['sales', 'business development', 'account management', 'revenue'],
            'consulting': ['consulting', 'advisory', 'strategy', 'management consulting'],
            'manufacturing': ['manufacturing', 'production', 'engineering', 'industrial']
        }

    def _load_technical_skills(self) -> List[str]:
        """Load technical skills database"""
        return [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node.js', 'django', 'flask', 'fastapi', 'spring', 'express', 'laravel',
            'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins',
            'git', 'github', 'gitlab', 'ci/cd', 'devops', 'microservices',
            'machine learning', 'ai', 'data science', 'pandas', 'numpy', 'tensorflow',
            'pytorch', 'scikit-learn', 'tableau', 'power bi', 'excel', 'r',
            'html', 'css', 'bootstrap', 'tailwind', 'sass', 'less',
            'rest api', 'graphql', 'json', 'xml', 'soap', 'web services'
        ]

    def _load_soft_skills(self) -> List[str]:
        """Load soft skills database"""
        return [
            'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
            'time management', 'project management', 'agile', 'scrum', 'collaboration',
            'adaptability', 'creativity', 'analytical', 'detail oriented', 'self motivated',
            'mentoring', 'training', 'presentation', 'negotiation', 'customer service',
            'multitasking', 'organization', 'planning', 'strategic thinking', 'innovation'
        ]

    def _load_programming_languages(self) -> List[str]:
        """Load programming languages database"""
        return [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby',
            'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl',
            'bash', 'powershell', 'sql', 'html', 'css', 'xml', 'yaml', 'json'
        ]

    def _load_frameworks(self) -> List[str]:
        """Load frameworks and libraries database"""
        return [
            'react', 'angular', 'vue', 'ember', 'svelte', 'next.js', 'nuxt.js',
            'django', 'flask', 'fastapi', 'spring', 'express', 'laravel', 'symfony',
            'rails', 'asp.net', 'tornado', 'bottle', 'cherrypy', 'falcon',
            'bootstrap', 'tailwind', 'material ui', 'ant design', 'chakra ui',
            'jquery', 'lodash', 'moment', 'axios', 'fetch', 'graphql'
        ]

    def _load_tools(self) -> List[str]:
        """Load tools and technologies database"""
        return [
            'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack',
            'docker', 'kubernetes', 'jenkins', 'travis ci', 'circleci', 'github actions',
            'aws', 'azure', 'gcp', 'heroku', 'netlify', 'vercel', 'firebase',
            'postman', 'insomnia', 'swagger', 'postman', 'figma', 'sketch', 'adobe',
            'vscode', 'intellij', 'eclipse', 'sublime', 'atom', 'vim', 'emacs',
            'linux', 'ubuntu', 'centos', 'windows', 'macos', 'bash', 'powershell'
        ]

    async def analyze_resume(self, resume_content: str) -> ResumeAnalysisResponse:
        """Main method to analyze a resume"""
        start_time = datetime.now()
        
        try:
            # Clean and preprocess the resume content
            cleaned_content = self._clean_text(resume_content)
            
            # Extract different components
            skills = self._extract_skills(cleaned_content)
            experience_years = self._extract_experience_years(cleaned_content)
            education = self._extract_education(cleaned_content)
            experience = self._extract_experience(cleaned_content)
            industry = self._identify_industry(cleaned_content)
            job_titles = self._extract_job_titles(cleaned_content)
            companies = self._extract_companies(cleaned_content)
            
            # Calculate scores
            skills_score = self._calculate_skills_score(skills)
            experience_score = self._calculate_experience_score(experience_years, experience)
            education_score = self._calculate_education_score(education)
            overall_score = (skills_score + experience_score + education_score) / 3
            
            # Generate recommendations
            suggestions = self._generate_suggestions(skills, experience_years, education)
            strengths = self._identify_strengths(skills, experience, education)
            weaknesses = self._identify_weaknesses(skills, experience, education)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ResumeAnalysisResponse(
                skills=skills,
                experience_years=experience_years,
                education_level=self._get_highest_education_level(education),
                industry=industry,
                job_titles=job_titles,
                companies=companies,
                education=education,
                experience=experience,
                overall_score=round(overall_score, 2),
                skills_score=round(skills_score, 2),
                experience_score=round(experience_score, 2),
                education_score=round(education_score, 2),
                suggestions=suggestions,
                strengths=strengths,
                weaknesses=weaknesses,
                analysis_date=datetime.now(),
                processing_time=round(processing_time, 2)
            )
            
        except Exception as e:
            logger.error(f"Error analyzing resume: {str(e)}")
            raise Exception(f"Resume analysis failed: {str(e)}")

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove special characters but keep alphanumeric and basic punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', ' ', text)
        
        return text.lower()

    def _extract_skills(self, text: str) -> List[SkillAnalysis]:
        """Extract skills from resume text"""
        skills = []
        text_lower = text.lower()
        
        # Extract technical skills
        for skill in self.technical_skills:
            if skill.lower() in text_lower:
                confidence = self._calculate_skill_confidence(skill, text_lower)
                skills.append(SkillAnalysis(
                    skill=skill.title(),
                    confidence=confidence,
                    category="Technical"
                ))
        
        # Extract soft skills
        for skill in self.soft_skills:
            if skill.lower() in text_lower:
                confidence = self._calculate_skill_confidence(skill, text_lower)
                skills.append(SkillAnalysis(
                    skill=skill.title(),
                    confidence=confidence,
                    category="Soft Skills"
                ))
        
        # Remove duplicates and sort by confidence
        unique_skills = {}
        for skill in skills:
            if skill.skill not in unique_skills or skill.confidence > unique_skills[skill.skill].confidence:
                unique_skills[skill.skill] = skill
        
        return sorted(unique_skills.values(), key=lambda x: x.confidence, reverse=True)

    def _calculate_skill_confidence(self, skill: str, text: str) -> float:
        """Calculate confidence score for a skill"""
        # Count occurrences
        count = text.count(skill.lower())
        
        # Base confidence on frequency and context
        if count == 0:
            return 0.0
        elif count == 1:
            return 0.7
        elif count == 2:
            return 0.85
        else:
            return min(1.0, 0.9 + (count - 2) * 0.05)

    def _extract_experience_years(self, text: str) -> float:
        """Extract years of experience from resume"""
        # Look for patterns like "5 years", "3+ years", "2-4 years"
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\s*-\s*(\d+)\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\s*years?\s*(?:of\s*)?(?:experience|exp)'
        ]
        
        max_years = 0
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Range pattern
                    years = (int(match[0]) + int(match[1])) / 2
                else:
                    years = int(match)
                max_years = max(max_years, years)
        
        # If no explicit years found, estimate from job entries
        if max_years == 0:
            max_years = self._estimate_experience_from_jobs(text)
        
        return min(max_years, 50)  # Cap at 50 years

    def _estimate_experience_from_jobs(self, text: str) -> float:
        """Estimate experience from job entries"""
        # Look for date patterns in job descriptions
        date_patterns = [
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*-\s*present',
            r'(\d{4})\s*-\s*current'
        ]
        
        total_months = 0
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    if match[1].lower() in ['present', 'current']:
                        # Assume current year
                        end_year = datetime.now().year
                    else:
                        end_year = int(match[1])
                    
                    start_year = int(match[0])
                    months = (end_year - start_year) * 12
                    total_months += months
        
        return total_months / 12 if total_months > 0 else 0

    def _extract_education(self, text: str) -> List[EducationInfo]:
        """Extract education information"""
        education = []
        
        # Look for degree patterns
        degree_patterns = [
            r'(bachelor|master|phd|doctorate|associate|diploma|certificate)\s*(?:of|in)?\s*([^,\n]+)',
            r'([^,\n]+)\s*(?:bachelor|master|phd|doctorate|associate|diploma|certificate)'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    degree = match[0].strip()
                    field = match[1].strip()
                    
                    # Extract institution
                    institution = self._extract_institution(text, field)
                    
                    education.append(EducationInfo(
                        degree=degree.title(),
                        institution=institution,
                        graduation_year=self._extract_graduation_year(text, field)
                    ))
        
        return education

    def _extract_institution(self, text: str, field: str) -> str:
        """Extract institution name"""
        # Look for university/college names near the field
        institution_keywords = ['university', 'college', 'institute', 'school']
        
        for keyword in institution_keywords:
            pattern = rf'([^,\n]*{keyword}[^,\n]*)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return "Unknown Institution"

    def _extract_graduation_year(self, text: str, field: str) -> Optional[int]:
        """Extract graduation year"""
        # Look for years near education information
        year_pattern = r'\b(19|20)\d{2}\b'
        matches = re.findall(year_pattern, text)
        
        if matches:
            # Return the most recent year
            return max([int(match) for match in matches])
        
        return None

    def _extract_experience(self, text: str) -> List[ExperienceInfo]:
        """Extract work experience"""
        experience = []
        
        # Look for job title patterns
        title_patterns = [
            r'(senior|junior|lead|principal|staff)?\s*([^,\n]+)\s*(?:at|@|in)\s*([^,\n]+)',
            r'([^,\n]+)\s*(?:at|@|in)\s*([^,\n]+)'
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    title = match[0].strip() if len(match) == 2 else f"{match[0]} {match[1]}".strip()
                    company = match[-1].strip()
                    
                    experience.append(ExperienceInfo(
                        title=title.title(),
                        company=company.title(),
                        duration=self._extract_duration(text, title, company),
                        description=self._extract_job_description(text, title, company),
                        skills_used=self._extract_job_skills(text, title, company)
                    ))
        
        return experience

    def _extract_duration(self, text: str, title: str, company: str) -> str:
        """Extract job duration"""
        # Look for date patterns near the job
        date_patterns = [
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*-\s*present',
            r'(\d{4})\s*-\s*current'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if len(match) == 2:
                    return f"{match[0]} - {match[1]}"
                else:
                    return f"{match[0]} - Present"
        
        return "Duration not specified"

    def _extract_job_description(self, text: str, title: str, company: str) -> str:
        """Extract job description"""
        # This is a simplified version - in a real implementation,
        # you'd use more sophisticated NLP to extract descriptions
        return f"Worked as {title} at {company}"

    def _extract_job_skills(self, text: str, title: str, company: str) -> List[str]:
        """Extract skills used in specific job"""
        # Look for skills mentioned near the job title
        job_skills = []
        for skill in self.technical_skills + self.soft_skills:
            if skill.lower() in text.lower():
                job_skills.append(skill.title())
        
        return job_skills[:5]  # Limit to top 5 skills

    def _identify_industry(self, text: str) -> str:
        """Identify the industry from resume content"""
        text_lower = text.lower()
        industry_scores = {}
        
        for industry, keywords in self.industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                industry_scores[industry] = score
        
        if industry_scores:
            return max(industry_scores, key=industry_scores.get).title()
        
        return "General"

    def _extract_job_titles(self, text: str) -> List[str]:
        """Extract job titles from resume"""
        titles = []
        
        # Common job title patterns
        title_patterns = [
            r'(senior|junior|lead|principal|staff)?\s*([^,\n]+)\s*(?:developer|engineer|manager|analyst|specialist|consultant)',
            r'(software|data|web|frontend|backend|full.?stack|devops|cloud|security)\s*([^,\n]+)'
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    title = " ".join(match).strip()
                else:
                    title = match.strip()
                
                if len(title) > 3:  # Filter out very short matches
                    titles.append(title.title())
        
        return list(set(titles))  # Remove duplicates

    def _extract_companies(self, text: str) -> List[str]:
        """Extract company names from resume"""
        companies = []
        
        # Look for company patterns
        company_patterns = [
            r'(?:at|@|in)\s*([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Corp|Ltd|Company|Technologies|Solutions|Systems)?)',
            r'([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Corp|Ltd|Company|Technologies|Solutions|Systems))'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                company = match.strip()
                if len(company) > 2 and company not in companies:
                    companies.append(company)
        
        return companies

    def _get_highest_education_level(self, education: List[EducationInfo]) -> str:
        """Get the highest education level"""
        if not education:
            return "Not Specified"
        
        levels = {
            'phd': 5,
            'doctorate': 5,
            'master': 4,
            'bachelor': 3,
            'associate': 2,
            'diploma': 1,
            'certificate': 1
        }
        
        highest_level = "Not Specified"
        highest_score = 0
        
        for edu in education:
            degree_lower = edu.degree.lower()
            for level, score in levels.items():
                if level in degree_lower and score > highest_score:
                    highest_score = score
                    highest_level = edu.degree
        
        return highest_level

    def _calculate_skills_score(self, skills: List[SkillAnalysis]) -> float:
        """Calculate skills score based on number and relevance of skills"""
        if not skills:
            return 0.0
        
        # Base score on number of skills
        base_score = min(len(skills) * 2, 50)  # Max 50 points for skills count
        
        # Bonus for high-confidence skills
        confidence_bonus = sum(skill.confidence * 5 for skill in skills)
        
        # Bonus for technical skills
        technical_bonus = sum(10 for skill in skills if skill.category == "Technical")
        
        total_score = base_score + confidence_bonus + technical_bonus
        return min(total_score, 100)  # Cap at 100

    def _calculate_experience_score(self, years: float, experience: List[ExperienceInfo]) -> float:
        """Calculate experience score"""
        if years == 0:
            return 0.0
        
        # Base score on years of experience
        base_score = min(years * 5, 50)  # Max 50 points for years
        
        # Bonus for number of positions
        position_bonus = min(len(experience) * 5, 25)  # Max 25 points for positions
        
        # Bonus for seniority keywords
        seniority_bonus = 0
        for exp in experience:
            title_lower = exp.title.lower()
            if any(keyword in title_lower for keyword in ['senior', 'lead', 'principal', 'staff']):
                seniority_bonus += 5
        
        total_score = base_score + position_bonus + seniority_bonus
        return min(total_score, 100)  # Cap at 100

    def _calculate_education_score(self, education: List[EducationInfo]) -> float:
        """Calculate education score"""
        if not education:
            return 0.0
        
        # Base score on highest education level
        highest_level = self._get_highest_education_level(education)
        
        level_scores = {
            'phd': 100,
            'doctorate': 100,
            'master': 80,
            'bachelor': 60,
            'associate': 40,
            'diploma': 30,
            'certificate': 20
        }
        
        base_score = 0
        for level, score in level_scores.items():
            if level in highest_level.lower():
                base_score = score
                break
        
        # Bonus for multiple degrees
        if len(education) > 1:
            base_score += min(len(education) * 5, 20)
        
        return min(base_score, 100)

    def _generate_suggestions(self, skills: List[SkillAnalysis], years: float, education: List[EducationInfo]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Skills suggestions
        if len(skills) < 10:
            suggestions.append("Consider adding more relevant skills to your resume")
        
        technical_skills = [s for s in skills if s.category == "Technical"]
        if len(technical_skills) < 5:
            suggestions.append("Add more technical skills to improve your profile")
        
        # Experience suggestions
        if years < 2:
            suggestions.append("Consider gaining more work experience or highlighting relevant projects")
        
        # Education suggestions
        if not education:
            suggestions.append("Add your educational background to your resume")
        
        # Industry-specific suggestions
        suggestions.append("Tailor your resume to specific job requirements")
        suggestions.append("Use action verbs to describe your achievements")
        suggestions.append("Include quantifiable results and metrics")
        
        return suggestions[:5]  # Limit to 5 suggestions

    def _identify_strengths(self, skills: List[SkillAnalysis], experience: List[ExperienceInfo], education: List[EducationInfo]) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        
        # Skills strengths
        if len(skills) >= 15:
            strengths.append("Comprehensive skill set")
        
        technical_skills = [s for s in skills if s.category == "Technical"]
        if len(technical_skills) >= 8:
            strengths.append("Strong technical background")
        
        # Experience strengths
        if len(experience) >= 3:
            strengths.append("Diverse work experience")
        
        # Education strengths
        if education:
            highest_level = self._get_highest_education_level(education)
            if 'master' in highest_level.lower() or 'phd' in highest_level.lower():
                strengths.append("Advanced education")
        
        return strengths

    def _identify_weaknesses(self, skills: List[SkillAnalysis], experience: List[ExperienceInfo], education: List[EducationInfo]) -> List[str]:
        """Identify areas for improvement"""
        weaknesses = []
        
        # Skills weaknesses
        if len(skills) < 8:
            weaknesses.append("Limited skill set")
        
        # Experience weaknesses
        if len(experience) < 2:
            weaknesses.append("Limited work experience")
        
        # Education weaknesses
        if not education:
            weaknesses.append("Missing educational information")
        
        return weaknesses
