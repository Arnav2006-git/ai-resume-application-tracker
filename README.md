# AI Resume Match + Internship Tracker

A full-stack web application that helps students and job seekers improve their internship and job application process. The platform analyzes resume-to-job fit, tracks applications, and provides AI-powered suggestions for improvement.

## Features

### 📊 Resume Matching
- Upload resume (PDF, DOCX, TXT formats)
- Paste job description
- Get instant match score (0-100%)
- View matching and missing keywords
- Receive personalized improvement suggestions

### 📋 Application Tracking
- Save matched applications
- Track application status (Applied, OA, Interview, Rejected, Offer)
- Monitor deadlines
- Add custom notes
- View application statistics and analytics

### 💡 Smart Analytics
- Match score distribution
- Application status breakdown
- Keyword analysis
- Improvement suggestions
- Export functionality

## Tech Stack

### Backend
- **Framework**: Flask 2.3
- **Database**: SQLAlchemy ORM with SQLite (configurable to PostgreSQL)
- **Text Processing**: PyPDF2, python-docx, scikit-learn
- **API**: RESTful Flask API with CORS support
- **ML/NLP**: TF-IDF vectorization, cosine similarity matching

### Frontend
- **HTML/CSS/JavaScript**: Vanilla (no frameworks for lightweight deployment)
- **Responsive Design**: Mobile-first CSS Grid/Flexbox
- **Client-side Storage**: localStorage for user sessions
- **API Communication**: Fetch API with error handling

### DevOps
- **Containerization**: Docker & Docker Compose
- **Server**: Gunicorn (production), Flask dev server (development)

## Project Structure

```
resume-match-tracker/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── models/
│   │   ├── resume.py          # Resume model
│   │   ├── application.py      # Application tracking model
│   │   └── job_posting.py      # Job posting model
│   ├── routes/
│   │   ├── resume.py          # Resume endpoints
│   │   ├── matching.py        # Matching endpoints
│   │   └── applications.py     # Application tracking endpoints
│   ├── services/
│   │   ├── resume_processor.py # Resume text extraction & processing
│   │   ├── matcher.py         # Resume-to-job matching logic
│   │   └── db_service.py      # Database operations
│   ├── utils/
│   │   ├── file_handler.py    # File upload handling
│   │   └── text_extractor.py  # Text extraction utilities
│   └── migrations/
│       └── init.sql           # Database schema
├── frontend/
│   ├── index.html             # Dashboard page
│   ├── css/
│   │   └── styles.css         # Main CSS
│   ├── js/
│   │   ├── app.js             # Shared utilities & API calls
│   │   ├── matcher.js         # Resume matcher page logic
│   │   └── tracker.js         # Application tracker page logic
│   └── pages/
│       ├── matcher.html       # Resume matcher page
│       └── tracker.html       # Application tracker page
├── .env                       # Environment variables
├── .gitignore                 # Git ignore rules
├── docker-compose.yml         # Docker composition
└── README.md                  # This file
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for frontend build tools, optional)
- PostgreSQL or SQLite
- Docker & Docker Compose (optional)

### Local Development Setup

#### 1. Clone and navigate to project
```bash
cd Project
```

#### 2. Create Python virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install backend dependencies
```bash
pip install -r backend/requirements.txt
```

#### 4. Set up environment variables
Create `.env` file in the root directory:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///resume_tracker.db
```

#### 5. Initialize database
```bash
cd backend
python
>>> from app import create_app
>>> app = create_app()
>>> exit()
```

#### 6. Start backend server
```bash
cd backend
python app.py
```
Backend runs on `http://localhost:5000`

#### 7. Open frontend
Open `frontend/index.html` in your browser or run a local server:
```bash
# Using Python
cd frontend
python -m http.server 8000

# Using Node.js
cd frontend
npx http-server
```
Frontend runs on `http://localhost:8000`

## API Endpoints

### Resume Management
- `POST /api/resume/upload` - Upload resume file
- `GET /api/resume/get?user_id=USER_ID` - Get resume info
- `DELETE /api/resume/delete?user_id=USER_ID` - Delete resume

### Resume Matching
- `POST /api/matching/match` - Match resume to job
- `POST /api/matching/quick-match` - Quick match without saving

### Application Tracking
- `GET /api/applications?user_id=USER_ID` - Get all applications
- `PUT /api/applications/{id}/status` - Update application status
- `PUT /api/applications/{id}/notes` - Update application notes
- `DELETE /api/applications/{id}` - Delete application
- `GET /api/applications/stats?user_id=USER_ID` - Get statistics

## Database Schema

### Resumes Table
- `id` - Primary key
- `user_id` - User identifier
- `filename` - Original filename
- `file_path` - Stored file path
- `raw_text` - Extracted resume text
- `extracted_skills` - JSON array of skills
- `extracted_keywords` - JSON array of keywords
- `created_at`, `updated_at` - Timestamps

### Applications Table
- `id` - Primary key
- `user_id` - User identifier
- `resume_id` - Foreign key to resumes
- `company_name` - Company name
- `job_title` - Job title
- `status` - Current status (Applied, OA, Interview, Rejected, Offer)
- `match_score` - Similarity score (0-100)
- `matching_keywords` - JSON array of matched keywords
- `missing_keywords` - JSON array of missing keywords
- `suggested_improvements` - JSON array of suggestions
- `deadline` - Application deadline
- `notes` - User notes
- `created_at`, `updated_at` - Timestamps

### Job Postings Table
- `id` - Primary key
- `user_id` - User identifier
- `job_title` - Job title
- `company_name` - Company name
- `description` - Job description
- `extracted_keywords` - JSON array of keywords
- `extracted_skills` - JSON array of skills
- `created_at`, `updated_at` - Timestamps

## Deployment

### Docker Deployment
```bash
docker-compose up --build
```

This will:
- Build and run the Flask backend on `localhost:5000`
- Serve the frontend on `localhost:3000`

### Production Deployment
1. Update `.env` with production values
2. Set `FLASK_ENV=production`
3. Use PostgreSQL instead of SQLite
4. Use Gunicorn as WSGI server
5. Set up HTTPS/SSL certificates
6. Configure environment-specific settings

## Usage Guide

### Step 1: Upload Resume
1. Go to "Resume Matcher"
2. Click upload area or drag-and-drop your resume
3. Click "Upload Resume"

### Step 2: Paste Job Description
1. Fill in Company Name and Job Title
2. Optionally add Job URL
3. Paste the job description in the text area
4. Click "Match Resume"

### Step 3: Review Results
- See overall match score
- Check matching keywords
- Review missing keywords
- Read improvement suggestions

### Step 4: Track Applications
1. Save applications from match results
2. Go to "Application Tracker"
3. Monitor status and deadlines
4. Update status as you progress
5. Add notes for each application

## Key Features Explained

### Match Score Calculation
- Uses TF-IDF vectorization and cosine similarity
- Compares resume text with job description
- ML-based keyword extraction and comparison
- Score ranges from 0-100%

### Keyword Extraction
- Identifies technical skills and keywords
- Compares against predefined skill database
- Highlights missing critical keywords
- Suggests where to improve

### Application Tracking
- Multiple status levels (Applied, OA, Interview, etc.)
- Deadline monitoring and notifications (future)
- Notes for each application
- Performance analytics and insights

## Future Enhancements

- [ ] Email notifications for deadlines
- [ ] Calendar integration
- [ ] Interview scheduling
- [ ] Resume optimization AI
- [ ] Job recommendation engine
- [ ] Multiple resume versions
- [ ] Team collaboration features
- [ ] Advanced analytics dashboard
- [ ] LinkedIn profile integration
- [ ] Automated application tracking

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
- Open an issue on GitHub
- Check existing documentation
- Contact the development team

## Acknowledgments

- Inspired by various resume matching and job tracking tools
- Built with Python, Flask, and modern web technologies
- Thanks to the open-source community

---

**Last Updated**: April 2024
**Version**: 1.0.0
