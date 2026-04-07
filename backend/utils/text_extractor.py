"""Text extraction from various file formats"""
import PyPDF2
from docx import Document
import re

# Common English stop words to filter out
STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 
    'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 
    'between', 'both', 'by', 'can', 'could', 'did', 'do', 'does', 'doing', 'down', 
    'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 
    'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 
    'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'might', 'more', 
    'most', 'must', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'only', 
    'or', 'other', 'out', 'over', 'own', 'same', 'should', 'so', 'some', 'such', 
    'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 
    'these', 'they', 'this', 'those', 'to', 'too', 'under', 'until', 'up', 'very', 
    'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 
    'why', 'with', 'you', 'your', 'yours', 'yourself', 'yourselves', 'also', 'are', 
    'as', 'be', 'been', 'but', 'by', 'even', 'get', 'had', 'has', 'have', 'he', 
    'see', 'she', 'such', 'us', 'use', 'using', 'would', 'year', 'years', 'work', 'working',
    'developed', 'responsible', 'supported', 'led', 'managed', 'created',  # common resume verbs
    # Generic/common words that aren't meaningful skills
    'new', 'related', 'full', 'control', 'modern', 'computer', 'team', 'teams',
    'experience', 'basic', 'currently', 'closely', 'applications', 'application',
    'science', 'skills', 'engineering', 'code', 'version', 'build', 'building',
    'communication', 'collaborate', 'debug', 'degree', 'bachelor', 'master',
    'backend', 'frontend', 'data', 'integration', 'internship', 'tools', 'tool',
    'requirement', 'requirements', 'required', 'strong', 'excellent', 'good',
    'ability', 'abilities', 'knowledge', 'understanding', 'experience', 'background',
    'technical', 'technical', 'role', 'position', 'job', 'work', 'project', 'projects',
    'team', 'company', 'organization', 'industry', 'field', 'area', 'level',
    'opportunity', 'opportunities', 'member', 'developer', 'developer', 'engineer'
}


def extract_from_pdf(filepath):
    """Extract text from PDF file"""
    try:
        text = []
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        return '\n'.join(text)
    except Exception as e:
        raise Exception(f"Error extracting PDF: {str(e)}")


def extract_from_docx(filepath):
    """Extract text from DOCX file"""
    try:
        doc = Document(filepath)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text)
    except Exception as e:
        raise Exception(f"Error extracting DOCX: {str(e)}")


def extract_from_txt(filepath):
    """Extract text from TXT file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error extracting TXT: {str(e)}")


def extract_text(filepath, file_type):
    """Extract text based on file type"""
    extractors = {
        'pdf': extract_from_pdf,
        'docx': extract_from_docx,
        'txt': extract_from_txt
    }
    
    extractor = extractors.get(file_type)
    if not extractor:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    return extractor(filepath)


def clean_text(text):
    """Clean extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep important ones
    text = re.sub(r'[^\w\s\-,.\(\)]', '', text)
    return text.strip()


def extract_keywords(text, min_length=3):
    """Extract keywords from text, filtering out stop words"""
    # Clean text
    text = clean_text(text.lower())
    # Split into words
    words = text.split()
    # Filter by length, uniqueness, and stop words
    keywords = list(set([
        w for w in words 
        if len(w) >= min_length 
        and w.isalpha() 
        and w not in STOP_WORDS
    ]))
    return sorted(keywords)


def extract_email(text):
    """Extract email from text"""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    return emails[0] if emails else None


def extract_phone(text):
    """Extract phone number from text"""
    pattern = r'\+?1?\d{9,15}'
    phones = re.findall(pattern, text)
    return phones if phones else []
