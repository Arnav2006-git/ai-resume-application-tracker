import { useState } from 'react'
import './App.css'
import { matchingAPI } from './services/api'
import { parseResumeFile } from './utils/fileParser'
import { addApplication } from './services/tracker'
import Dashboard from './components/Dashboard'
import ApplicationForm from './components/ApplicationForm'

function App() {
  const [currentPage, setCurrentPage] = useState('matcher') // 'matcher', 'dashboard', 'form'
  const [resume, setResume] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [fileName, setFileName] = useState('')
  const [error, setError] = useState(null)
  const [resumeText, setResumeText] = useState(null)

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0]
    if (file) {
      setError(null)
      try {
        // Extract text from the resume file
        const text = await parseResumeFile(file)
        setResume(file)
        setFileName(file.name)
        setResumeText(text)
      } catch (err) {
        setError(`Failed to parse resume: ${err.message}`)
        setResume(null)
        setFileName('')
      }
    }
  }

  const handleAnalyze = async () => {
    if (!resume || !jobDescription.trim()) {
      setError('Please upload a resume and enter a job description.')
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Call the backend API with new AI-based matching
      const response = await matchingAPI.quickMatch(resumeText, jobDescription, true)

      // Extract numeric match score
      let matchScore = response.match_score || 0
      if (typeof matchScore === 'string') {
        matchScore = parseFloat(matchScore.replace('%', '')) || 0
      }

      // Transform backend response to match UI expectations
      setResults({
        matchScore: Math.round(matchScore),
        matchPercentage: matchScore,
        matchCount: response.matching_skills?.length || response.matching_keywords?.length || 0,
        missingCount: response.missing_skills?.length || response.missing_keywords?.length || 0,
        matchedKeywords: response.matching_skills || response.matching_keywords || [],
        missingKeywords: response.missing_skills || response.missing_keywords || [],
        suggestions: response.improvement_suggestions || response.suggestions || [],
      })
    } catch (err) {
      setError(`Analysis failed: ${err.message}. Make sure the backend is running on http://127.0.0.1:5000`)
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveApplication = () => {
    if (results) {
      try {
        addApplication({
          companyName: 'From Resume Match',
          jobTitle: 'Analyzed Position',
          status: 'Applied',
          matchScore: results.matchScore,
          matchedKeywords: results.matchedKeywords,
          missingKeywords: results.missingKeywords,
          suggestions: results.suggestions,
        })
        setError(null)
        setSuccess('Application saved to tracker!')
        setTimeout(() => {
          setCurrentPage('dashboard')
          setSuccess(null)
        }, 2000)
      } catch (err) {
        setError(`Error saving application: ${err.message}`)
      }
    }
  }

  const [success, setSuccess] = useState(null)

  const handleClear = () => {
    setResume(null)
    setFileName('')
    setJobDescription('')
    setResults(null)
    setError(null)
    setResumeText(null)
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-top">
          <div className="header-branding">
            <h1 className="app-title">ResumeIQ</h1>
          </div>
          <nav className="app-nav">
            <button
              className={`nav-button ${currentPage === 'matcher' ? 'active' : ''}`}
              onClick={() => setCurrentPage('matcher')}
            >
              🔍 Analyzer
            </button>
            <button
              className={`nav-button ${currentPage === 'dashboard' ? 'active' : ''}`}
              onClick={() => setCurrentPage('dashboard')}
            >
              📊 Dashboard
            </button>
            <button
              className={`nav-button ${currentPage === 'form' ? 'active' : ''}`}
              onClick={() => setCurrentPage('form')}
            >
              ➕ Add Application
            </button>
          </nav>
        </div>
      </header>

      <main className="app-main">
        {/* Resume Matcher Page */}
        {currentPage === 'matcher' && (
          <>
            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                <div>
                  <strong>Error:</strong> {error}
                  <details style={{ marginTop: '10px', fontSize: '12px', color: '#666' }}>
                    <summary>Debug Info (click to expand)</summary>
                    <p>Make sure:</p>
                    <ul>
                      <li>Backend is running: http://127.0.0.1:5000</li>
                      <li>Gemini API key is set in backend/.env</li>
                      <li>Resume file was successfully extracted</li>
                      <li>Job description is not empty</li>
                    </ul>
                  </details>
                </div>
              </div>
            )}

            {success && (
              <div className="success-message">
                <span className="success-icon">✅</span>
                <div>
                  <strong>Success:</strong> {success}
                </div>
              </div>
            )}

            <div className="form-section">
              <div className="input-grid">
                <div className="form-card">
                  <h3 className="section-title">Upload Resume</h3>
                  <div className="upload-area">
                    <label htmlFor="resume-input" className="upload-label">
                      <div className="upload-content">
                        <span className="upload-icon">📄</span>
                        <span className="upload-text">
                          {fileName ? `Selected: ${fileName}` : 'Click to upload PDF or DOCX'}
                        </span>
                        <span className="upload-hint">or drag and drop</span>
                      </div>
                    </label>
                    <input
                      id="resume-input"
                      type="file"
                      accept=".pdf,.docx"
                      onChange={handleResumeUpload}
                      className="file-input"
                    />
                  </div>
                </div>

                <div className="form-card">
                  <h3 className="section-title">Job Description</h3>
                  <textarea
                    className="job-textarea"
                    placeholder="Paste the job description here..."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                  />
                </div>
              </div>

              <div className="button-group">
                <button
                  className={`analyze-button ${loading ? 'loading' : ''}`}
                  onClick={handleAnalyze}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="spinner"></span>
                      Analyzing...
                    </>
                  ) : (
                    '🚀 Analyze Match'
                  )}
                </button>
                <button
                  className="clear-button"
                  onClick={handleClear}
                  disabled={loading}
                >
                  Clear
                </button>
              </div>
            </div>

            {results && (
              <div className="results-section">
                <div className="results-card">
                  <h2 className="results-title">Analysis Results</h2>

                  <div className="result-item">
                    <h3>Match Score</h3>
                    <div className="match-score-box">
                      <div className="score-circle">
                        <div className="score-value">{results.matchScore}%</div>
                        <div className="score-label">Match</div>
                      </div>
                      <div className="score-details">
                        <p>
                          <strong>Overall Match:</strong> {results.matchPercentage.toFixed(1)}% similarity
                        </p>
                        <p>
                          <strong>Matched Keywords:</strong> {results.matchCount} found
                        </p>
                        <p>
                          <strong>Missing Keywords:</strong> {results.missingCount} needed
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="result-item">
                    <h3>✅ Matched Keywords ({results.matchedKeywords.length})</h3>
                    {results.matchedKeywords.length > 0 ? (
                      <div className="keywords-list">
                        {results.matchedKeywords.map((keyword, index) => (
                          <span key={index} className="keyword-tag keyword-matched">
                            {keyword}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <div className="no-keywords">
                        <p>No matching keywords found. Consider updating your resume with job-specific terms.</p>
                      </div>
                    )}
                  </div>

                  <div className="result-item">
                    <h3>❌ Missing Keywords ({results.missingKeywords.length})</h3>
                    {results.missingKeywords.length > 0 ? (
                      <div className="keywords-list">
                        {results.missingKeywords.slice(0, 15).map((keyword, index) => (
                          <span key={index} className="keyword-tag keyword-missing">
                            {keyword}
                          </span>
                        ))}
                        {results.missingKeywords.length > 15 && (
                          <span className="keyword-tag keyword-more">
                            +{results.missingKeywords.length - 15} more
                          </span>
                        )}
                      </div>
                    ) : (
                      <div className="no-keywords">
                        <p>You have all the key terms! Your resume is well-aligned with the job description.</p>
                      </div>
                    )}
                  </div>

                  <div className="result-item">
                    <h3>💡 Suggestions</h3>
                    {results.suggestions.length > 0 ? (
                      <div className="suggestions-list">
                        {results.suggestions.map((suggestion, index) => (
                          <div key={index} className="suggestion-item">
                            <span className="suggestion-number">{index + 1}</span>
                            <p>{suggestion}</p>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="no-suggestions">
                        <p>No specific suggestions at this time.</p>
                      </div>
                    )}
                  </div>

                  <div className="results-actions">
                    <button
                      className="save-to-tracker-button"
                      onClick={handleSaveApplication}
                    >
                      ✅ Save to Tracker
                    </button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* Dashboard Page */}
        {currentPage === 'dashboard' && <Dashboard />}

        {/* Application Form Page */}
        {currentPage === 'form' && <ApplicationForm onApplicationAdded={() => setCurrentPage('dashboard')} />}
      </main>

      <footer className="app-footer">
        <p>Track and optimize your job applications | Version 1.0</p>
      </footer>
    </div>
  )
}

export default App
