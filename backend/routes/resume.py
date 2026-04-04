"""Resume upload and management routes"""
from flask import Blueprint, request, jsonify, current_app
import os
from utils.file_handler import allowed_file, save_upload_file, delete_file
from services.resume_processor import ResumeProcessor
from services.db_service import DatabaseService

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')


@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    """Upload and process a resume"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        user_id = request.form.get('user_id', 'default_user')
        
        # Save file
        filepath, error = save_upload_file(file)
        if error:
            return jsonify({'error': error}), 400
        
        # Process resume
        raw_text, skills, keywords, parsed_data = ResumeProcessor.process_resume(filepath)
        
        # Save to database
        resume = DatabaseService.create_resume(
            user_id=user_id,
            filename=file.filename,
            file_path=filepath,
            file_type=file.filename.rsplit('.', 1)[1].lower(),
            raw_text=raw_text,
            skills=skills,
            keywords=keywords,
            parsed_data=parsed_data
        )
        
        return jsonify({
            'message': 'Resume uploaded successfully',
            'resume': resume.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@resume_bp.route('/get', methods=['GET'])
def get_resume():
    """Get user's resume information"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        resume = DatabaseService.get_resume(user_id)
        
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        return jsonify(resume.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@resume_bp.route('/delete', methods=['DELETE'])
def delete_resume():
    """Delete user's resume"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        resume = DatabaseService.get_resume(user_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Delete file
        if os.path.exists(resume.file_path):
            delete_file(resume.file_path)
        
        # Delete from database
        DatabaseService.delete_resume(user_id)
        
        return jsonify({'message': 'Resume deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
