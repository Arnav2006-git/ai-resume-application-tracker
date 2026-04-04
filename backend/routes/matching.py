"""Resume-to-job matching routes"""
from flask import Blueprint, request, jsonify
from utils.text_extractor import extract_keywords
from services.matcher import ResumeMatcher
from services.db_service import DatabaseService

matching_bp = Blueprint('matching', __name__, url_prefix='/api/matching')


@matching_bp.route('/match', methods=['POST'])
def match_resume():
    """Match resume against job description"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        job_description = data.get('job_description')
        company_name = data.get('company_name')
        job_title = data.get('job_title')
        job_url = data.get('job_url', '')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Get user's resume
        resume = DatabaseService.get_resume(user_id)
        if not resume:
            return jsonify({'error': 'Resume not found. Please upload a resume first.'}), 404
        
        # Extract job keywords and skills
        job_keywords = extract_keywords(job_description)
        job_skills = ResumeMatcher.__dict__.get('COMMON_SKILLS', [])
        
        # Calculate match score
        match_score = ResumeMatcher.calculate_match_score(resume.raw_text, job_description)
        
        # Get detailed analysis
        analysis = ResumeMatcher.get_detailed_analysis(
            resume.raw_text,
            resume.extracted_keywords,
            job_description,
            job_keywords,
            match_score
        )
        
        # Save application record
        application = DatabaseService.create_application(
            user_id=user_id,
            resume_id=resume.id,
            company_name=company_name or 'Unknown',
            job_title=job_title or 'Unknown',
            job_description=job_description,
            match_score=match_score,
            matching_keywords=analysis['matching_keywords'],
            missing_keywords=analysis['missing_keywords'],
            suggestions=analysis['suggestions'],
            job_url=job_url
        )
        
        return jsonify({
            'analysis': analysis,
            'application': application.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@matching_bp.route('/quick-match', methods=['POST'])
def quick_match():
    """Quick match without saving application"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text')
        job_description = data.get('job_description')
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Resume text and job description are required'}), 400
        
        # Extract keywords
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_description)
        
        # Calculate match score
        match_score = ResumeMatcher.calculate_match_score(resume_text, job_description)
        
        # Get detailed analysis
        analysis = ResumeMatcher.get_detailed_analysis(
            resume_text,
            resume_keywords,
            job_description,
            job_keywords,
            match_score
        )
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
