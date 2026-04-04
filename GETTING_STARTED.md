# Getting Started Guide

Welcome to **AI Resume Match + Internship Tracker**! This guide will help you get up and running quickly.

## 🚀 Quick Start (5 minutes)

### Windows
1. Double-click `setup.bat` to automatically set up everything
2. The script will:
   - Create a Python virtual environment
   - Install all dependencies
   - Initialize the database
   - Show you the next steps

### macOS/Linux
1. Run the setup script:
   ```bash
   bash setup.sh
   ```
2. The script will set everything up for you

## 📋 Manual Setup

If the automated setup doesn't work, follow these steps:

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3: Start the Backend
```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 4: Open the Frontend
In a new terminal (keep backend running):
```bash
cd frontend
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser

---

## 💡 How to Use

### Upload Your Resume
1. Click on **"Resume Matcher"** in the navigation
2. Click the upload area or drag-and-drop your resume
3. Upload and wait for processing

### Match with Job Descriptions
1. Fill in the company name and job title
2. Paste the job description
3. Click **"Match Resume"**
4. Review your match score and suggestions

### Track Your Applications
1. Click **"Application Tracker"**
2. View all your applications
3. Update statuses as you progress
4. Add notes and track deadlines

---

## 📁 Project Structure Overview

```
Project/
├── backend/              # Python Flask backend
│   ├── app.py           # Main application
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   └── utils/           # Helper functions
│
├── frontend/            # Web interface
│   ├── index.html       # Dashboard
│   ├── pages/           # Other pages
│   ├── css/             # Styling
│   └── js/              # JavaScript logic
│
├── README.md            # Full documentation
├── API_DOCUMENTATION.md # API reference
└── setup.bat/.sh        # Setup scripts
```

---

## 🔧 Configuration

### Environment Variables (.env)
The project uses a `.env` file for configuration. Key variables:
- `FLASK_ENV` - Development or production
- `SECRET_KEY` - Session encryption key
- `DATABASE_URL` - Database connection string

Default setup uses SQLite (no configuration needed).

### Database
- **Default**: SQLite (local file `resume_tracker.db`)
- **Production**: PostgreSQL recommended
- Database is auto-created on first run

---

## 📊 Features

### Resume Analysis
- Extract text from PDF, DOCX, and TXT files
- Identify skills and keywords automatically
- Compare with job requirements

### Intelligent Matching
- Calculate match score (0-100%)
- Show matching keywords
- Highlight missing keywords
- Generate improvement suggestions

### Application Tracking
- Save matched applications
- Track status (Applied, OA, Interview, Rejected, Offer)
- Monitor deadlines
- Add detailed notes
- View statistics and analytics

---

## 🐛 Troubleshooting

### Backend Won't Start
```
❌ "Port 5000 already in use"
✅ Solution: Change port in backend/app.py or kill the process using 5000
```

### File Upload Error
```
❌ "File type not allowed"
✅ Solution: Use only PDF, DOCX, or TXT files
```

### Database Error
```
❌ "No such table: resumes"
✅ Solution: Delete resume_tracker.db and restart backend
```

### JavaScript Errors in Browser
```
❌ "200 OK response, but no data"
✅ Solution: Backend not running? Check http://localhost:5000
```

### CORS Issues
```
❌ "Cross-Origin Request Blocked"
✅ Solution: Backend CORS is already enabled, check if running on correct port
```

---

## 📈 Next Steps

### Enhance Your Experience
1. **Add more skills** to the skill database in `services/resume_processor.py`
2. **Customize suggestions** in `services/matcher.py`
3. **Change styling** in `frontend/css/styles.css`
4. **Add features** like email notifications or integrations

### Deploy
1. Set up PostgreSQL database
2. Configure production settings in `.env`
3. Use Docker: `docker-compose up --build`
4. Deploy to cloud (Heroku, AWS, DigitalOcean, etc.)

### Integrate with External Services
- LinkedIn API for profile import
- Email service for notifications
- Calendar API for deadline tracking
- Job board APIs for recommendations

---

## 📞 Getting Help

### Documentation
- Read [README.md](README.md) for full documentation
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- Review code comments for implementation details

### Common Questions

**Q: Can I have multiple resumes?**
A: Currently one per user. Modify database schema to support multiple.

**Q: How is the match score calculated?**
A: Uses TF-IDF vectorization and cosine similarity (see `services/matcher.py`).

**Q: Can I export my data?**
A: Yes! Frontend has export buttons for JSON format.

**Q: Is my data secure?**
A: Data is local by default. Add authentication for production use.

---

## 🎯 Pro Tips

1. **Better Matches**: More detailed resumes with keywords = better matching
2. **Organize Notes**: Use application notes to track communication and next steps
3. **Bulk Upload**: You can quickly match multiple jobs with same resume
4. **Track Trends**: View statistics to identify which sectors/companies interest you
5. **Tailor Resumes**: Use suggestions to create role-specific resume versions

---

## 📚 Learning Resources

### Technologies Used
- **Python**: [python.org](https://python.org)
- **Flask**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **SQLAlchemy**: [sqlalchemy.org](https://sqlalchemy.org)
- **scikit-learn**: [scikit-learn.org](https://scikit-learn.org)

### Recommended Courses
- Python Backend Development with Flask
- Machine Learning for Text Analysis
- Full-Stack Web Development
- Database Design and SQL

---

## 🎉 Ready to Start?

1. Run the setup script
2. Upload your resume
3. Start matching with jobs
4. Track your applications
5. Get hired! 🚀

---

**Version**: 1.0.0  
**Last Updated**: April 2024  
**Questions?** Check the documentation files or review the code comments.
