"""Database service layer"""
from models import db, Resume, Application, JobPosting
from datetime import datetime


class DatabaseService:
    """Handle all database operations"""
    
    # Resume operations
    @staticmethod
    def create_resume(user_id, filename, file_path, file_type, raw_text, skills, keywords, parsed_data):
        """Create a new resume record"""
        try:
            # Check if user already has a resume
            existing = Resume.query.filter_by(user_id=user_id).first()
            if existing:
                db.session.delete(existing)
            
            ai_analysis = parsed_data.get('ai_analysis')
            
            resume = Resume(
                user_id=user_id,
                filename=filename,
                file_path=file_path,
                file_type=file_type,
                raw_text=raw_text,
                extracted_skills=skills,
                extracted_keywords=keywords,
                parsed_data=parsed_data,
                ai_analysis=ai_analysis
            )
            db.session.add(resume)
            db.session.commit()
            return resume
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating resume: {str(e)}")
    
    @staticmethod
    def get_resume(user_id):
        """Get user's resume"""
        return Resume.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def delete_resume(user_id):
        """Delete user's resume"""
        try:
            resume = Resume.query.filter_by(user_id=user_id).first()
            if resume:
                db.session.delete(resume)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting resume: {str(e)}")
    
    # Job posting operations
    @staticmethod
    def create_job_posting(user_id, job_title, company_name, description, requirements, keywords, skills):
        """Create a new job posting record"""
        try:
            job = JobPosting(
                user_id=user_id,
                job_title=job_title,
                company_name=company_name,
                description=description,
                requirements=requirements,
                extracted_keywords=keywords,
                extracted_skills=skills
            )
            db.session.add(job)
            db.session.commit()
            return job
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating job posting: {str(e)}")
    
    @staticmethod
    def get_job_posting(job_id):
        """Get job posting by ID"""
        return JobPosting.query.get(job_id)
    
    # Application operations
    @staticmethod
    def create_application(user_id, resume_id, company_name, job_title, job_description, 
                          match_score, matching_keywords, missing_keywords, suggestions, job_url='',
                          analysis_method='tfidf', ai_analysis=None):
        """Create a new application record"""
        try:
            application = Application(
                user_id=user_id,
                resume_id=resume_id,
                company_name=company_name,
                job_title=job_title,
                job_description=job_description,
                match_score=match_score,
                matching_keywords=matching_keywords,
                missing_keywords=missing_keywords,
                suggested_improvements=suggestions,
                job_url=job_url,
                status='Applied',
                analysis_method=analysis_method,
                ai_analysis=ai_analysis
            )
            db.session.add(application)
            db.session.commit()
            return application
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating application: {str(e)}")
    
    @staticmethod
    def get_user_applications(user_id):
        """Get all applications for a user"""
        return Application.query.filter_by(user_id=user_id).order_by(Application.created_at.desc()).all()
    
    @staticmethod
    def update_application_status(application_id, status):
        """Update application status"""
        try:
            app = Application.query.get(application_id)
            if app:
                app.status = status
                app.updated_at = datetime.utcnow()
                db.session.commit()
            return app
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating application: {str(e)}")
    
    @staticmethod
    def update_application_notes(application_id, notes):
        """Update application notes"""
        try:
            app = Application.query.get(application_id)
            if app:
                app.notes = notes
                app.updated_at = datetime.utcnow()
                db.session.commit()
            return app
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating application notes: {str(e)}")
    
    @staticmethod
    def delete_application(application_id):
        """Delete an application"""
        try:
            app = Application.query.get(application_id)
            if app:
                db.session.delete(app)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting application: {str(e)}")
    
    @staticmethod
    def get_application_statistics(user_id):
        """Get statistics for user applications"""
        applications = Application.query.filter_by(user_id=user_id).all()
        
        total = len(applications)
        if total == 0:
            return {
                'total': 0,
                'applied': 0,
                'oa': 0,
                'interview': 0,
                'rejected': 0,
                'offer': 0,
                'average_score': 0
            }
        
        stats = {
            'total': total,
            'applied': len([a for a in applications if a.status == 'Applied']),
            'oa': len([a for a in applications if a.status == 'OA']),
            'interview': len([a for a in applications if a.status == 'Interview']),
            'rejected': len([a for a in applications if a.status == 'Rejected']),
            'offer': len([a for a in applications if a.status == 'Offer']),
            'average_score': round(sum([a.match_score for a in applications]) / total, 2)
        }
        
        return stats
