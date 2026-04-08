"""AI-based resume analysis using Google Gemini API"""
import google.generativeai as genai
from flask import current_app
import json


class AIResumeAnalyzer:
    """Analyze resumes using Google Gemini AI"""
    
    @staticmethod
    def initialize_gemini(api_key):
        """Initialize Gemini API with API key"""
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
    
    @staticmethod
    def analyze_resume(resume_text):
        """Analyze resume using Gemini AI and extract key information"""
        try:
            api_key = current_app.config.get('GEMINI_API_KEY')
            model_name = current_app.config.get('GEMINI_MODEL', 'gemini-1.5-flash')
            
            AIResumeAnalyzer.initialize_gemini(api_key)
            model = genai.GenerativeModel(model_name)
            
            prompt = f"""Analyze the following resume and provide a structured analysis in JSON format.
            
Resume Content:
{resume_text}

Please analyze and return ONLY a valid JSON object (no additional text) with the following structure:
{{
    "summary": "A 2-3 sentence professional summary of the candidate",
    "skills": ["list", "of", "technical", "skills", "found"],
    "experience_level": "Junior/Mid-level/Senior/Executive",
    "years_of_experience": number,
    "education": ["Bachelor of Science in Computer Science", "Master of Arts in Business"],
    "strengths": ["key strength 1", "key strength 2", "key strength 3"],
    "areas_for_improvement": ["area 1", "area 2"],
    "key_qualifications": ["qualification 1", "qualification 2"],
    "career_focus": "The primary career field or specialization",
    "certifications": ["certification 1", "certification 2"],
    "languages": ["language 1", "language 2"]
}}

Important: Return ONLY valid JSON, no markdown code blocks, no explanations."""
            
            response = model.generate_content(prompt)
            
            # Parse the response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            analysis_result = json.loads(response_text)
            return analysis_result
            
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing AI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error analyzing resume with AI: {str(e)}")
    
    @staticmethod
    def match_resume_with_job(resume_text, job_description):
        """Match resume with job description using AI for intelligent analysis"""
        try:
            api_key = current_app.config.get('GEMINI_API_KEY')
            model_name = current_app.config.get('GEMINI_MODEL', 'gemini-1.5-flash')
            
            AIResumeAnalyzer.initialize_gemini(api_key)
            model = genai.GenerativeModel(model_name)
            
            prompt = f"""Analyze how well the following resume matches the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide analysis in JSON format ONLY (no additional text):
{{
    "match_score": 85,
    "match_percentage": "85%",
    "matching_skills": ["skill1", "skill2", "skill3"],
    "missing_skills": ["skill4", "skill5"],
    "strengths_for_role": ["relevant experience", "required skill"],
    "experience_fit": "Your X years of experience aligns well with the role requirements",
    "improvement_suggestions": ["Highlight your achievement in X", "Develop skills in Y"],
    "overall_assessment": "Brief assessment of how well the candidate fits the position"
}}

Return ONLY valid JSON."""
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            analysis_result = json.loads(response_text)
            return analysis_result
            
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing AI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error matching resume with AI: {str(e)}")
