"""Text extraction from various file formats"""
import PyPDF2
from docx import Document
import re


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
    """Extract keywords from text"""
    # Clean text
    text = clean_text(text.lower())
    # Split into words
    words = text.split()
    # Filter by length and unique
    keywords = list(set([w for w in words if len(w) >= min_length and w.isalpha()]))
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
