"""File handling utilities for resume uploads"""
import os
from werkzeug.utils import secure_filename
from config import Config


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def get_file_extension(filename):
    """Extract file extension"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else None


def save_upload_file(file):
    """Save uploaded file to disk"""
    if not file or not allowed_file(file.filename):
        return None, "File not allowed"
    
    try:
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath, None
    except Exception as e:
        return None, str(e)


def delete_file(filepath):
    """Delete a file from disk"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    except Exception as e:
        return False
