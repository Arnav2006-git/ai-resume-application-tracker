"""Resume processing service"""
from utils.text_extractor import extract_text, extract_keywords, extract_email, extract_phone
from utils.file_handler import get_file_extension
from services.ai_analyzer import AIResumeAnalyzer
import re


class ResumeProcessor:
    """Process and extract information from resumes"""
    
    COMMON_SKILLS = [
        'python', 'java', 'javascript', 'c++', 'c#', 'sql', 'html', 'css',
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'rest api',
        'machine learning', 'data analysis', 'tableau', 'power bi',
        'agile', 'scrum', 'jira', 'linux', 'windows', 'mongodb', 'postgresql'
    ]
    
    @staticmethod
    def process_resume(filepath, use_ai=True):
        """Process resume and extract structured information using AI or traditional methods"""
        try:
            file_type = get_file_extension(filepath)
            raw_text = extract_text(filepath, file_type)
            
            if not raw_text.strip():
                raise Exception("Resume is empty or could not be extracted. Please ensure it's a valid file with readable text.")
            
            # Extract various components
            skills = ResumeProcessor.extract_skills(raw_text)
            keywords = extract_keywords(raw_text)
            email = extract_email(raw_text)
            phone = extract_phone(raw_text)
            
            # AI-based analysis
            ai_analysis = None
            if use_ai:
                try:
                    ai_analysis = AIResumeAnalyzer.analyze_resume(raw_text)
                except Exception as ai_error:
                    print(f"Warning: AI analysis failed, using traditional analysis: {str(ai_error)}")
                    ai_analysis = None
            
            parsed_data = {
                'email': email,
                'phone': phone,
                'skills': skills,
                'keywords': keywords,
                'text_length': len(raw_text),
                'word_count': len(raw_text.split()),
                'ai_analysis': ai_analysis
            }
            
            return raw_text, skills, keywords, parsed_data
        except Exception as e:
            raise Exception(f"Error processing resume: {str(e)}")
    
    @staticmethod
    def extract_skills(text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in ResumeProcessor.COMMON_SKILLS:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    @staticmethod
    def extract_experience_years(text):
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\s*years?\s*(?:of\s*)?experience',
            r'(?:exp|experience).*?(\d+)\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None
    
    @staticmethod
    def extract_education(text):
        """Extract education information from text"""
        degrees = ['bachelor', 'master', 'phd', 'diploma', 'associate', 'b.s.', 'm.s.']
        education = []
        
        text_lower = text.lower()
        for degree in degrees:
            if degree in text_lower:
                education.append(degree)
        
        return education
    
    @staticmethod
    def extract_skills(text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in ResumeProcessor.COMMON_SKILLS:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    @staticmethod
    def extract_experience_years(text):
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\s*years?\s*(?:of\s*)?experience',
            r'(?:exp|experience).*?(\d+)\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None
    
    @staticmethod
    def extract_education(text):
        """Extract education information from text"""
        degrees = ['bachelor', 'master', 'phd', 'diploma', 'associate', 'b.s.', 'm.s.']
        education = []
        
        text_lower = text.lower()
        for degree in degrees:
            if degree in text_lower:
                education.append(degree)
        
        return education
