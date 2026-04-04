# API Documentation

This document describes all available API endpoints for the AI Resume Match + Internship Tracker application.

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API uses `user_id` as a simple identifier. In production, implement JWT tokens.

---

## Resume Management

### 1. Upload Resume

**Endpoint:** `POST /resume/upload`

**Description:** Upload a resume file for processing and analysis.

**Request:**
```
Content-Type: multipart/form-data

Parameters:
- file (required): Resume file (PDF, DOCX, or TXT)
- user_id (optional): User identifier (defaults to 'default_user')
```

**Response:** `201 Created`
```json
{
  "message": "Resume uploaded successfully",
  "resume": {
    "id": 1,
    "user_id": "user123",
    "filename": "my_resume.pdf",
    "file_type": "pdf",
    "extracted_skills": ["python", "java", "sql"],
    "extracted_keywords": ["software", "engineer", "backend"],
    "created_at": "2024-04-04T10:30:00",
    "updated_at": "2024-04-04T10:30:00"
  }
}
```

**Errors:**
- `400 Bad Request`: No file provided or file type not allowed
- `500 Internal Server Error`: Processing error

---

### 2. Get Resume

**Endpoint:** `GET /resume/get`

**Description:** Retrieve stored resume information for a user.

**Query Parameters:**
- `user_id` (optional): User identifier (defaults to 'default_user')

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": "user123",
  "filename": "my_resume.pdf",
  "file_type": "pdf",
  "extracted_skills": ["python", "java", "sql"],
  "extracted_keywords": ["software", "engineer", "backend"],
  "created_at": "2024-04-04T10:30:00",
  "updated_at": "2024-04-04T10:30:00"
}
```

**Errors:**
- `404 Not Found`: Resume not found for user
- `500 Internal Server Error`: Server error

---

### 3. Delete Resume

**Endpoint:** `DELETE /resume/delete`

**Description:** Delete a user's resume.

**Query Parameters:**
- `user_id` (optional): User identifier (defaults to 'default_user')

**Response:** `200 OK`
```json
{
  "message": "Resume deleted successfully"
}
```

**Errors:**
- `404 Not Found`: Resume not found for user
- `500 Internal Server Error`: Server error

---

## Resume Matching

### 4. Match Resume to Job

**Endpoint:** `POST /matching/match`

**Description:** Calculate match score between user's resume and a job description.

**Request Body:**
```json
{
  "user_id": "user123",
  "company_name": "Google",
  "job_title": "Software Engineer",
  "job_description": "We are looking for a talented software engineer...",
  "job_url": "https://careers.google.com/job123" // optional
}
```

**Response:** `200 OK`
```json
{
  "analysis": {
    "overall_score": 82.5,
    "match_percentage": 82.5,
    "matching_count": 12,
    "missing_count": 5,
    "matching_keywords": ["python", "java", "backend", "api", "database"],
    "missing_keywords": ["kubernetes", "docker", "aws", "gcp"],
    "suggestions": [
      "Excellent match! You meet most of the job requirements.",
      "Make sure to highlight your relevant experience in your cover letter."
    ]
  },
  "application": {
    "id": 1,
    "user_id": "user123",
    "company_name": "Google",
    "job_title": "Software Engineer",
    "match_score": 82.5,
    "status": "Applied",
    "created_at": "2024-04-04T10:35:00",
    "updated_at": "2024-04-04T10:35:00"
  }
}
```

**Errors:**
- `400 Bad Request`: Missing required fields
- `404 Not Found`: Resume not found
- `500 Internal Server Error`: Matching error

---

### 5. Quick Match (No Save)

**Endpoint:** `POST /matching/quick-match`

**Description:** Quick match without saving application record.

**Request Body:**
```json
{
  "resume_text": "Full resume text here...",
  "job_description": "Full job description here..."
}
```

**Response:** `200 OK`
```json
{
  "overall_score": 75.3,
  "match_percentage": 75.3,
  "matching_count": 10,
  "missing_count": 8,
  "matching_keywords": ["python", "java"],
  "missing_keywords": ["kubernetes", "docker"],
  "suggestions": ["Try to include these missing keywords..."]
}
```

**Errors:**
- `400 Bad Request`: Missing required text
- `500 Internal Server Error`: Matching error

---

## Application Tracking

### 6. Get All Applications

**Endpoint:** `GET /applications`

**Description:** Retrieve all applications for a user.

**Query Parameters:**
- `user_id` (optional): User identifier (defaults to 'default_user')

**Response:** `200 OK`
```json
{
  "applications": [
    {
      "id": 1,
      "user_id": "user123",
      "company_name": "Google",
      "job_title": "Software Engineer",
      "status": "Interview",
      "match_score": 82.5,
      "applied_date": "2024-04-01T10:00:00",
      "deadline": "2024-04-30T23:59:59",
      "notes": "Great company, very interested",
      "matching_keywords": ["python", "api"],
      "missing_keywords": ["docker"],
      "suggested_improvements": ["Consider adding Docker experience"],
      "created_at": "2024-04-01T10:00:00",
      "updated_at": "2024-04-04T15:30:00"
    }
  ],
  "count": 1
}
```

**Errors:**
- `500 Internal Server Error`: Server error

---

### 7. Update Application Status

**Endpoint:** `PUT /applications/{id}/status`

**Description:** Update the status of an application.

**Path Parameters:**
- `id`: Application ID

**Request Body:**
```json
{
  "status": "Interview"
}
```

**Status Options:** `Applied`, `OA`, `Interview`, `Rejected`, `Offer`

**Response:** `200 OK`
```json
{
  "message": "Status updated",
  "application": {
    "id": 1,
    "status": "Interview",
    "updated_at": "2024-04-04T15:30:00"
  }
}
```

**Errors:**
- `400 Bad Request`: Status not provided or invalid
- `404 Not Found`: Application not found
- `500 Internal Server Error`: Server error

---

### 8. Update Application Notes

**Endpoint:** `PUT /applications/{id}/notes`

**Description:** Add or update notes for an application.

**Path Parameters:**
- `id`: Application ID

**Request Body:**
```json
{
  "notes": "Had a great interview, asked about project experience"
}
```

**Response:** `200 OK`
```json
{
  "message": "Notes updated",
  "application": {
    "id": 1,
    "notes": "Had a great interview...",
    "updated_at": "2024-04-04T15:30:00"
  }
}
```

**Errors:**
- `404 Not Found`: Application not found
- `500 Internal Server Error`: Server error

---

### 9. Delete Application

**Endpoint:** `DELETE /applications/{id}`

**Description:** Delete an application record.

**Path Parameters:**
- `id`: Application ID

**Response:** `200 OK`
```json
{
  "message": "Application deleted"
}
```

**Errors:**
- `500 Internal Server Error`: Server error

---

### 10. Get Application Statistics

**Endpoint:** `GET /applications/stats`

**Description:** Get statistics of all applications for a user.

**Query Parameters:**
- `user_id` (optional): User identifier (defaults to 'default_user')

**Response:** `200 OK`
```json
{
  "total": 10,
  "applied": 4,
  "oa": 2,
  "interview": 2,
  "rejected": 1,
  "offer": 1,
  "average_score": 76.5
}
```

**Errors:**
- `500 Internal Server Error`: Server error

---

## Error Handling

All error responses follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

---

## Example Usage

### Using cURL

```bash
# Upload resume
curl -X POST http://localhost:5000/api/resume/upload \
  -F "file=@resume.pdf" \
  -F "user_id=user123"

# Match resume to job
curl -X POST http://localhost:5000/api/matching/match \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "company_name": "Google",
    "job_title": "Software Engineer",
    "job_description": "We are looking for..."
  }'

# Get applications
curl http://localhost:5000/api/applications?user_id=user123

# Update status
curl -X PUT http://localhost:5000/api/applications/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Interview"}'
```

### Using JavaScript/Fetch

```javascript
// Upload resume
const formData = new FormData();
formData.append('file', resumeFile);
formData.append('user_id', 'user123');

const response = await fetch('http://localhost:5000/api/resume/upload', {
  method: 'POST',
  body: formData
});

// Match resume
const matchResponse = await fetch('http://localhost:5000/api/matching/match', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 'user123',
    company_name: 'Google',
    job_description: '...'
  })
});
```

---

## Rate Limiting
Currently not implemented. In production, add rate limiting to prevent abuse.

## Versioning
Current API Version: `1.0.0`

Future versions will maintain backward compatibility where possible.

---

**Last Updated:** April 2024
