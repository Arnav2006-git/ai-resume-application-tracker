"""Main Flask application"""
from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import configuration
from config import config

# Import models
from models import db

# Import blueprints
from routes.resume import resume_bp
from routes.matching import matching_bp
from routes.applications import applications_bp


def create_app(config_name='development'):
    """Create and configure Flask application"""
    # Load environment variables
    load_dotenv()
    
    # Create app instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    app.register_blueprint(resume_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(applications_bp)
    
    # Root route
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'AI Resume Match + Internship Tracker API',
            'version': '1.0.0',
            'status': 'running'
        }), 200
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    # Determine config from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(config_name)
    
    # Run app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config_name == 'development'
    )
