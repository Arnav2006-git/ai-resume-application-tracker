// Resume Matcher Page Logic
let uploadedResumeData = null;

document.addEventListener('DOMContentLoaded', function() {
    setupUploadArea();
    setupMatchForm();
});

// Setup upload area
function setupUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    const resumeFile = document.getElementById('resumeFile');
    const uploadBtn = document.getElementById('uploadBtn');
    
    // Click to upload
    uploadArea.addEventListener('click', () => resumeFile.click());
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            resumeFile.files = files;
            handleFileSelect(files[0]);
        }
    });
    
    // File input change
    resumeFile.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    // Upload button
    uploadBtn.addEventListener('click', uploadResume);
}

// Handle file selection
function handleFileSelect(file) {
    // Validate file
    const allowedExtensions = ['pdf', 'docx', 'txt'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
        showNotification('File type not allowed. Please use PDF, DOCX, or TXT.', 'error');
        return;
    }
    
    if (!isFileSizeValid(file)) {
        showNotification('File size exceeds 16MB limit.', 'error');
        return;
    }
    
    // Show upload button
    document.getElementById('uploadBtn').style.display = 'inline-block';
    showNotification('File selected. Click "Upload Resume" to upload.', 'success');
}

// Upload resume
async function uploadResume() {
    const resumeFile = document.getElementById('resumeFile');
    
    if (!resumeFile.files.length) {
        showNotification('Please select a file first.', 'error');
        return;
    }
    
    const file = resumeFile.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', USER_ID);
    
    try {
        const response = await fetch(`${API_BASE_URL}/resume/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }
        
        const data = await response.json();
        uploadedResumeData = data.resume;
        
        // Update UI
        displayResumeInfo(data.resume);
        showNotification('Resume uploaded successfully!', 'success');
        
        // Enable match button
        document.getElementById('matchBtn').disabled = false;
    } catch (error) {
        console.error('Upload error:', error);
        showNotification('Error uploading resume: ' + error.message, 'error');
    }
}

// Display resume information
function displayResumeInfo(resumeData) {
    document.getElementById('resumeFileName').textContent = resumeData.filename;
    document.getElementById('resumeSkills').textContent = resumeData.extracted_skills.join(', ') || 'No skills found';
    document.getElementById('resumeKeywords').textContent = resumeData.extracted_keywords.slice(0, 10).join(', ') + '...';
    document.getElementById('resumeInfo').classList.remove('hidden');
}

// Setup match form
function setupMatchForm() {
    const matchForm = document.getElementById('matchForm');
    matchForm.addEventListener('submit', handleMatch);
}

// Handle matching
async function handleMatch(e) {
    e.preventDefault();
    
    if (!uploadedResumeData) {
        showNotification('Please upload a resume first.', 'error');
        return;
    }
    
    const companyName = document.getElementById('companyName').value;
    const jobTitle = document.getElementById('jobTitle').value;
    const jobUrl = document.getElementById('jobUrl').value;
    const jobDescription = document.getElementById('jobDescription').value;
    
    if (!jobDescription.trim()) {
        showNotification('Please enter a job description.', 'error');
        return;
    }
    
    try {
        // Show loading state
        document.getElementById('matchBtn').disabled = true;
        document.getElementById('matchBtn').textContent = 'Matching...';
        
        const response = await apiCall('POST', '/matching/match', {
            user_id: USER_ID,
            company_name: companyName,
            job_title: jobTitle,
            job_description: jobDescription,
            job_url: jobUrl
        });
        
        // Display results
        displayResults(response.analysis);
        
        // Store application data for saving
        window.currentApplication = response.application;
        window.currentAnalysis = response.analysis;
        
        showNotification('Match analysis complete!', 'success');
    } catch (error) {
        console.error('Match error:', error);
        showNotification('Error performing match: ' + error.message, 'error');
    } finally {
        document.getElementById('matchBtn').disabled = false;
        document.getElementById('matchBtn').textContent = 'Match Resume';
    }
}

// Display match results
function displayResults(analysis) {
    const resultsSection = document.getElementById('resultsSection');
    
    // Update score
    const scoreValue = Math.round(analysis.match_percentage);
    document.getElementById('scoreValue').textContent = scoreValue + '%';
    
    // Update score circle color
    const scoreCircle = document.getElementById('scoreCircle');
    scoreCircle.className = 'score-circle';
    if (scoreValue >= 75) {
        scoreCircle.classList.add('high-score');
        document.getElementById('scoreMessage').textContent = '✅ Excellent Match! You meet most requirements.';
    } else if (scoreValue >= 50) {
        scoreCircle.classList.add('medium-score');
        document.getElementById('scoreMessage').textContent = '🟡 Moderate Match. Some improvements needed.';
    } else {
        scoreCircle.classList.add('low-score');
        document.getElementById('scoreMessage').textContent = '❌ Low Match. Consider tailoring your resume.';
    }
    
    // Display matching keywords
    const matchingContainer = document.getElementById('matchingKeywords');
    matchingContainer.innerHTML = '';
    analysis.matching_keywords.slice(0, 10).forEach(keyword => {
        matchingContainer.appendChild(createKeywordTag(keyword, true));
    });
    document.getElementById('matchingCount').textContent = analysis.matching_count;
    
    // Display missing keywords
    const missingContainer = document.getElementById('missingKeywords');
    missingContainer.innerHTML = '';
    analysis.missing_keywords.slice(0, 10).forEach(keyword => {
        missingContainer.appendChild(createKeywordTag(keyword, false));
    });
    document.getElementById('missingCount').textContent = analysis.missing_count;
    
    // Display suggestions
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = '';
    analysis.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });
    
    // Setup save and download buttons
    document.getElementById('saveAppBtn').onclick = saveApplication;
    document.getElementById('downloadResultBtn').onclick = downloadResults;
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Save as application
async function saveApplication() {
    if (!window.currentApplication) {
        showNotification('No application data to save.', 'error');
        return;
    }
    
    showNotification('Application saved to your tracker!', 'success');
    setTimeout(() => {
        window.location.href = 'tracker.html';
    }, 1500);
}

// Download results
function downloadResults() {
    const data = {
        analysis: window.currentAnalysis,
        timestamp: new Date().toISOString()
    };
    
    exportAsJSON(data, `resume-match-${Date.now()}.json`);
    showNotification('Results downloaded!', 'success');
}
