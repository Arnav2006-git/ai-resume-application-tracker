"""Database models"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .resume import Resume
from .application import Application
from .job_posting import JobPosting

__all__ = ['db', 'Resume', 'Application', 'JobPosting']
