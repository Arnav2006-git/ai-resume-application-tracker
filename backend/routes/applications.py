"""Application tracking routes"""
from flask import Blueprint, request, jsonify
from services.db_service import DatabaseService

applications_bp = Blueprint('applications', __name__, url_prefix='/api/applications')


@applications_bp.route('', methods=['GET'])
def get_applications():
    """Get all applications for a user"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        applications = DatabaseService.get_user_applications(user_id)
        
        return jsonify({
            'applications': [app.to_dict() for app in applications],
            'count': len(applications)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/<int:app_id>/status', methods=['PUT'])
def update_status(app_id):
    """Update application status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'error': 'Status is required'}), 400
        
        if status not in ['Applied', 'OA', 'Interview', 'Rejected', 'Offer']:
            return jsonify({'error': 'Invalid status'}), 400
        
        app = DatabaseService.update_application_status(app_id, status)
        
        if not app:
            return jsonify({'error': 'Application not found'}), 404
        
        return jsonify({
            'message': 'Status updated',
            'application': app.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/<int:app_id>/notes', methods=['PUT'])
def update_notes(app_id):
    """Update application notes"""
    try:
        data = request.get_json()
        notes = data.get('notes', '')
        
        app = DatabaseService.update_application_notes(app_id, notes)
        
        if not app:
            return jsonify({'error': 'Application not found'}), 404
        
        return jsonify({
            'message': 'Notes updated',
            'application': app.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/<int:app_id>', methods=['DELETE'])
def delete_application(app_id):
    """Delete an application"""
    try:
        DatabaseService.delete_application(app_id)
        
        return jsonify({'message': 'Application deleted'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        stats = DatabaseService.get_application_statistics(user_id)
        
        return jsonify(stats), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
