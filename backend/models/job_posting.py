"""Job Posting model"""
from datetime import datetime
from . import db


class JobPosting(db.Model):
    """Job posting model for storing job descriptions"""
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, default='')
    extracted_keywords = db.Column(db.JSON, default=list)
    extracted_skills = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='job_posting', lazy=True)
    
    def __repr__(self):
        return f'<JobPosting {self.company_name} - {self.job_title}>'
    
    def to_dict(self):
        """Convert job posting to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_title': self.job_title,
            'company_name': self.company_name,
            'description': self.description,
            'requirements': self.requirements,
            'extracted_keywords': self.extracted_keywords,
            'extracted_skills': self.extracted_skills,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
