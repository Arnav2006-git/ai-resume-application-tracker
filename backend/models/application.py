"""Application Tracking model"""
from datetime import datetime
from . import db


class Application(db.Model):
    """Application tracking model"""
    __tablename__ = 'applications'
    
    STATUS_CHOICES = ['Applied', 'OA', 'Interview', 'Rejected', 'Offer']
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=True)
    company_name = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text, default='')
    status = db.Column(db.String(50), default='Applied')  # Applied, OA, Interview, Rejected, Offer
    match_score = db.Column(db.Float, default=0.0)
    missing_keywords = db.Column(db.JSON, default=list)
    matching_keywords = db.Column(db.JSON, default=list)
    suggested_improvements = db.Column(db.JSON, default=list)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, default='')
    job_url = db.Column(db.String(500), default='')
    analysis_method = db.Column(db.String(50), default='tfidf')  # 'ai' or 'tfidf'
    ai_analysis = db.Column(db.JSON, nullable=True)  # Store AI analysis results
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Application {self.company_name} - {self.job_title}>'
    
    def to_dict(self):
        """Convert application to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resume_id': self.resume_id,
            'job_id': self.job_id,
            'company_name': self.company_name,
            'job_title': self.job_title,
            'status': self.status,
            'match_score': self.match_score,
            'missing_keywords': self.missing_keywords,
            'matching_keywords': self.matching_keywords,
            'suggested_improvements': self.suggested_improvements,
            'applied_date': self.applied_date.isoformat(),
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'notes': self.notes,
            'job_url': self.job_url,
            'analysis_method': self.analysis_method,
            'ai_analysis': self.ai_analysis,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
