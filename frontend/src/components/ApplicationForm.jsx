/**
 * ApplicationForm Component - Form to add/log a new job application
 */
import { useState } from 'react'
import { addApplication, APPLICATION_STATUSES } from '../services/tracker'
import '../styles/applicationForm.css'

function ApplicationForm({ onApplicationAdded }) {
  const [formData, setFormData] = useState({
    companyName: '',
    jobTitle: '',
    applicationLink: '',
    status: APPLICATION_STATUSES.APPLIED,
    notes: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setError(null)
    setSuccess(false)

    if (!formData.companyName.trim() || !formData.jobTitle.trim()) {
      setError('Company name and job title are required.')
      return
    }

    setLoading(true)

    try {
      const newApplication = addApplication({
        companyName: formData.companyName,
        jobTitle: formData.jobTitle,
        jobLink: formData.applicationLink,
        status: formData.status,
        notes: formData.notes,
        matchScore: 0,
        matchedKeywords: [],
        missingKeywords: [],
        suggestions: [],
      })

      setSuccess(true)
      setFormData({
        companyName: '',
        jobTitle: '',
        applicationLink: '',
        status: APPLICATION_STATUSES.APPLIED,
        notes: '',
      })

      if (onApplicationAdded) {
        onApplicationAdded(newApplication)
      }

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(`Error saving application: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="application-form-container">
      <div className="form-card">
        <h2 className="form-title">📝 Log New Application</h2>
        <p className="form-subtitle">Track a new job application</p>

        {error && (
          <div className="form-message error-message">
            <span>⚠️</span>
            <p>{error}</p>
          </div>
        )}

        {success && (
          <div className="form-message success-message">
            <span>✅</span>
            <p>Application logged successfully!</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="application-form">
          <div className="form-group">
            <label htmlFor="companyName" className="form-label">
              Company Name *
            </label>
            <input
              id="companyName"
              type="text"
              name="companyName"
              value={formData.companyName}
              onChange={handleChange}
              placeholder="e.g., Google, Microsoft, Stripe"
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="jobTitle" className="form-label">
              Job Title *
            </label>
            <input
              id="jobTitle"
              type="text"
              name="jobTitle"
              value={formData.jobTitle}
              onChange={handleChange}
              placeholder="e.g., Software Engineering Intern"
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="applicationLink" className="form-label">
              Application Link
            </label>
            <input
              id="applicationLink"
              type="url"
              name="applicationLink"
              value={formData.applicationLink}
              onChange={handleChange}
              placeholder="https://..."
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="status" className="form-label">
              Current Status
            </label>
            <select
              id="status"
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="form-select"
            >
              {Object.entries(APPLICATION_STATUSES).map(([key, value]) => (
                <option key={key} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="notes" className="form-label">
              Notes
            </label>
            <textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Add any notes (e.g., interview scheduled, follow-up needed)"
              className="form-textarea"
              rows="4"
            />
          </div>

          <button
            type="submit"
            className={`submit-button ${loading ? 'loading' : ''}`}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Saving...
              </>
            ) : (
              '➕ Log Application'
            )}
          </button>
        </form>
      </div>
    </div>
  )
}

export default ApplicationForm
