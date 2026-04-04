#!/bin/bash
# Quick Start Script for Resume Matcher Tracker

echo "🚀 AI Resume Match + Internship Tracker - Setup Script"
echo "======================================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version || python3 --version

# Create virtual environment
echo "✓ Creating virtual environment..."
python -m venv venv || python3 -m venv venv

# Activate virtual environment
if [ -d "venv/Scripts" ]; then
    source venv/Scripts/activate  # Windows
else
    source venv/bin/activate  # macOS/Linux
fi

# Install dependencies
echo "✓ Installing Python dependencies..."
pip install -r backend/requirements.txt

# Create uploads directory
echo "✓ Creating uploads directory..."
mkdir -p uploads

# Initialize database
echo "✓ Initializing database..."
cd backend
python << 'EOF'
from app import create_app, db
app = create_app('development')
with app.app_context():
    db.create_all()
    print("✓ Database initialized successfully!")
EOF

echo ""
echo "===================="
echo "✅ Setup Complete!"
echo "===================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend (in backend/ directory):"
echo "   python app.py"
echo ""
echo "2. Open frontend in browser:"
echo "   - Open frontend/index.html directly, or"
echo "   - Run local server: python -m http.server 8000"
echo ""
echo "Backend will run on: http://localhost:5000"
echo "Frontend will run on: http://localhost:8000"
echo ""
