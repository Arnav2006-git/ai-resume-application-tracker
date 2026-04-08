"""Resume model"""
from datetime import datetime
from . import db


class Resume(db.Model):
    """Resume model for storing user resumes"""
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False, unique=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # pdf, docx, txt
    raw_text = db.Column(db.Text, nullable=False)
    extracted_skills = db.Column(db.JSON, default=list)
    extracted_keywords = db.Column(db.JSON, default=list)
    parsed_data = db.Column(db.JSON, default=dict)
    ai_analysis = db.Column(db.JSON, nullable=True)  # Store AI analysis from Gemini
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='resume', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Resume {self.user_id}>'
    
    def to_dict(self):
        """Convert resume to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_type': self.file_type,
            'extracted_skills': self.extracted_skills,
            'extracted_keywords': self.extracted_keywords,
            'ai_analysis': self.ai_analysis,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
