"""Resume-to-job matching routes"""
from flask import Blueprint, request, jsonify
from utils.text_extractor import extract_keywords
from services.matcher import ResumeMatcher
from services.semantic_matcher import SemanticATSMatcher
from services.db_service import DatabaseService

matching_bp = Blueprint('matching', __name__, url_prefix='/api/matching')


@matching_bp.route('/match', methods=['POST'])
def match_resume():
    """Match resume against job description using AI or Traditional analysis"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        job_description = data.get('job_description')
        company_name = data.get('company_name')
        job_title = data.get('job_title')
        job_url = data.get('job_url', '')
        use_ai = data.get('use_ai', True)  # Option to use AI analysis
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Get user's resume
        resume = DatabaseService.get_resume(user_id)
        if not resume:
            return jsonify({'error': 'Resume not found. Please upload a resume first.'}), 404
        
        # Calculate match score (AI or Traditional)
        analysis = ResumeMatcher.calculate_match_score(
            resume.raw_text, 
            job_description,
            use_ai=use_ai
        )
        
        # Extract match score
        match_score = analysis.get('match_score', 0)
        
        # Save application record
        application = DatabaseService.create_application(
            user_id=user_id,
            resume_id=resume.id,
            company_name=company_name or 'Unknown',
            job_title=job_title or 'Unknown',
            job_description=job_description,
            match_score=match_score,
            matching_keywords=analysis.get('matching_keywords', []),
            missing_keywords=analysis.get('missing_keywords', []),
            suggestions=analysis.get('suggestions', []),
            job_url=job_url,
            analysis_method='ai' if use_ai else 'tfidf',
            ai_analysis=analysis if use_ai else None
        )
        
        return jsonify({
            'analysis': analysis,
            'application': application.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@matching_bp.route('/quick-match', methods=['POST'])
def quick_match():
    """Quick match without saving application - supports AI or Traditional analysis"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text')
        job_description = data.get('job_description')
        use_ai = data.get('use_ai', True)
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Resume text and job description are required'}), 400
        
        # Calculate match score (AI or Traditional)
        analysis = ResumeMatcher.calculate_match_score(
            resume_text, 
            job_description,
            use_ai=use_ai
        )
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@matching_bp.route('/semantic-ats', methods=['POST'])
def semantic_ats_match():
    """Advanced semantic ATS matching - precision-focused analysis"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text')
        job_description = data.get('job_description')
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Resume text and job description are required'}), 400
        
        # Perform semantic ATS matching
        analysis = SemanticATSMatcher.match_resume_and_job(resume_text, job_description)
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@matching_bp.route('/semantic-ats/full', methods=['POST'])
def semantic_ats_full_match():
    """Full semantic ATS match with database save"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        job_description = data.get('job_description')
        company_name = data.get('company_name', '')
        job_title = data.get('job_title', '')
        job_url = data.get('job_url', '')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Get user's resume
        resume = DatabaseService.get_resume(user_id)
        if not resume:
            return jsonify({'error': 'Resume not found. Please upload a resume first.'}), 404
        
        # Perform semantic ATS matching
        analysis = SemanticATSMatcher.match_resume_and_job(resume.raw_text, job_description)
        
        # Save application record
        application = DatabaseService.create_application(
            user_id=user_id,
            resume_id=resume.id,
            company_name=company_name or 'Unknown',
            job_title=job_title or 'Unknown',
            job_description=job_description,
            match_score=analysis['match_score'],
            matching_keywords=analysis['matched_keywords'],
            missing_keywords=analysis['missing_keywords'],
            suggestions=analysis['gaps'],
            job_url=job_url,
            analysis_method='semantic_ats',
            ai_analysis=analysis
        )
        
        return jsonify({
            'analysis': analysis,
            'application': application.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
