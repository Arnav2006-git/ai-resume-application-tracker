# AI Resume Analysis Setup Guide

## Overview
The application now uses Google Gemini AI for intelligent resume analysis instead of relying solely on keyword-based matching. This provides much better insights into resume content and job fit.

## Setup Instructions

### 1. Get Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key"
3. Create a new API key for your project
4. Copy the API key

### 2. Configure Environment Variable
Add the following to your `.env` file in the `backend` directory:
```
GEMINI_API_KEY=your-api-key-here
```

### 3. Install Dependencies
The required package `google-generativeai` has been added to `requirements.txt`. Install it using:
```bash
pip install -r requirements.txt
```

## Features

### AI-Based Resume Analysis (on upload)
When you upload a resume, the system will now:
- Extract a professional summary
- Identify technical and soft skills
- Determine experience level
- Extract education information
- Identify strengths and areas for improvement
- Recognize certifications and languages

The AI analysis is stored in the database and returned with resume data.

### AI-Based Job Matching (new)
When matching a resume to a job description:
- The system attempts to use AI for intelligent matching (if API key is configured)
- Falls back to TF-IDF matching if AI is unavailable
- Returns detailed insights on skill matches, gaps, and recommendations

### API Endpoints

#### Resume Upload (with AI Analysis)
**Endpoint:** `POST /api/resume/upload`

Request (form-data):
- `file`: Resume file (PDF, DOCX, or TXT)
- `user_id`: User identifier

Response:
```json
{
  "message": "Resume uploaded successfully",
  "resume": {
    "id": 1,
    "user_id": "user123",
    "filename": "resume.pdf",
    "file_type": "pdf",
    "extracted_skills": ["Python", "JavaScript", ...],
    "extracted_keywords": ["database", "API", ...],
    "ai_analysis": {
      "summary": "...",
      "skills": [...],
      "experience_level": "Mid-level",
      "years_of_experience": 5,
      "strengths": [...],
      "areas_for_improvement": [...]
    }
  }
}
```

#### AI-Based Job Matching
**Endpoint:** `POST /api/matching/match`

Request (JSON):
```json
{
  "user_id": "user123",
  "job_description": "...",
  "company_name": "Tech Corp",
  "job_title": "Software Engineer",
  "job_url": "https://...",
  "use_ai": true
}
```

Response (AI Method):
```json
{
  "analysis": {
    "match_score": 85,
    "match_percentage": "85%",
    "matching_skills": ["Python", "React", ...],
    "missing_skills": ["Kubernetes", ...],
    "overall_assessment": "...",
    "improvement_suggestions": [...]
  },
  "application": {...}
}
```

## Error Handling

### PDF Extraction Errors
If you get "Error extracting PDF" messages:
1. Ensure the PDF is not corrupted
2. The PDF should have extractable text (not a scanned image PDF)
3. Try converting to a different format (DOCX or TXT)

### AI Analysis Errors
If AI analysis fails:
- The system will fall back to traditional keyword-based analysis
- Check that `GEMINI_API_KEY` is correctly set
- Verify the API key has proper permissions

## Performance Notes

- AI analysis takes slightly longer than keyword-based analysis
- For first-time setup, allow 2-3 seconds for API initialization
- The analysis results are cached in the database for future reference

## Privacy & Security

- Resume text is sent to Google's API for analysis
- API key should be kept secure (use environment variables, never commit to git)
- Review Google's privacy policy for API usage details
