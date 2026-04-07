/**
 * Dashboard Component - Display and manage all job applications
 */
import { useState, useEffect } from 'react'
import {
  getApplications,
  updateApplicationStatus,
  updateApplicationNotes,
  deleteApplication,
  APPLICATION_STATUSES,
  STATUS_COLORS,
  getApplicationStats,
} from '../services/tracker'
import '../styles/dashboard.css'

function Dashboard() {
  const [applications, setApplications] = useState([])
  const [filteredApps, setFilteredApps] = useState([])
  const [selectedStatus, setSelectedStatus] = useState('All')
  const [stats, setStats] = useState({
    total: 0,
    applied: 0,
    oa: 0,
    interview: 0,
    rejected: 0,
    offer: 0,
  })
  const [editingId, setEditingId] = useState(null)
  const [editingNotes, setEditingNotes] = useState('')

  // Load applications on mount
  useEffect(() => {
    loadApplications()
  }, [])

  // Filter applications when status changes
  useEffect(() => {
    if (selectedStatus === 'All') {
      setFilteredApps(applications)
    } else {
      setFilteredApps(applications.filter((app) => app.status === selectedStatus))
    }
  }, [applications, selectedStatus])

  const loadApplications = () => {
    const apps = getApplications()
    setApplications(apps)
    setStats(getApplicationStats())
  }

  const handleStatusChange = (appId, newStatus) => {
    try {
      updateApplicationStatus(appId, newStatus)
      loadApplications()
    } catch (error) {
      console.error('Error updating status:', error)
    }
  }

  const handleDelete = (appId) => {
    if (window.confirm('Are you sure you want to delete this application?')) {
      try {
        deleteApplication(appId)
        loadApplications()
      } catch (error) {
        console.error('Error deleting application:', error)
      }
    }
  }

  const handleEditNotes = (appId, currentNotes) => {
    setEditingId(appId)
    setEditingNotes(currentNotes)
  }

  const handleSaveNotes = (appId) => {
    try {
      updateApplicationNotes(appId, editingNotes)
      setEditingId(null)
      setEditingNotes('')
      loadApplications()
    } catch (error) {
      console.error('Error saving notes:', error)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  }

  return (
    <div className="dashboard-container">
      {/* Statistics Cards */}
      <div className="stats-section">
        <div className="stats-grid">
          <div className="stat-card total">
            <div className="stat-number">{stats.total}</div>
            <div className="stat-label">Total Applications</div>
          </div>
          <div className="stat-card applied">
            <div className="stat-number">{stats.applied}</div>
            <div className="stat-label">Applied</div>
          </div>
          <div className="stat-card oa">
            <div className="stat-number">{stats.oa}</div>
            <div className="stat-label">OA (Online Assessment)</div>
          </div>
          <div className="stat-card interview">
            <div className="stat-number">{stats.interview}</div>
            <div className="stat-label">Interview</div>
          </div>
          <div className="stat-card rejected">
            <div className="stat-number">{stats.rejected}</div>
            <div className="stat-label">Rejected</div>
          </div>
          <div className="stat-card offer">
            <div className="stat-number">{stats.offer}</div>
            <div className="stat-label">Offer</div>
          </div>
        </div>
      </div>

      {/* Filter Buttons */}
      <div className="filter-section">
        <h3 className="filter-title">Filter by Status</h3>
        <div className="filter-buttons">
          {['All', ...Object.values(APPLICATION_STATUSES)].map((status) => (
            <button
              key={status}
              className={`filter-button ${selectedStatus === status ? 'active' : ''}`}
              onClick={() => setSelectedStatus(status)}
            >
              {status}
            </button>
          ))}
        </div>
      </div>

      {/* Applications List */}
      <div className="applications-section">
        <h2 className="section-title">📋 Your Applications</h2>

        {filteredApps.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <h3>No applications yet</h3>
            <p>
              {selectedStatus === 'All'
                ? 'Start by logging your first job application'
                : `No applications with "${selectedStatus}" status`}
            </p>
          </div>
        ) : (
          <div className="applications-list">
            {filteredApps.map((app) => (
              <div key={app.id} className="application-card">
                <div 
                  className="app-header"
                  style={{
                    backgroundColor: `${STATUS_COLORS[app.status]}15`,
                    borderColor: STATUS_COLORS[app.status],
                    borderWidth: '2px 0 1px 0',
                    marginLeft: '-20px',
                    marginRight: '-20px',
                    marginTop: '-20px',
                    marginBottom: '16px',
                    paddingLeft: '20px',
                    paddingRight: '20px',
                    paddingTop: '16px',
                    paddingBottom: '16px'
                  }}
                >
                  <div className="app-info">
                    <h3 className="app-company">{app.companyName}</h3>
                    <p className="app-title">{app.jobTitle}</p>
                  </div>
                  <div className="app-meta">
                    <span className="app-date">{formatDate(app.createdAt)}</span>
                    <select
                      value={app.status}
                      onChange={(e) => handleStatusChange(app.id, e.target.value)}
                      className="status-select"
                      style={{ borderColor: STATUS_COLORS[app.status] }}
                    >
                      {Object.values(APPLICATION_STATUSES).map((status) => (
                        <option key={status} value={status}>
                          {status}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {app.jobLink && (
                  <div className="app-link">
                    <a href={app.jobLink} target="_blank" rel="noopener noreferrer" className="link-button">
                      🔗 View Listing
                    </a>
                  </div>
                )}

                <div className="app-notes-section">
                  {editingId === app.id ? (
                    <div className="notes-edit">
                      <textarea
                        value={editingNotes}
                        onChange={(e) => setEditingNotes(e.target.value)}
                        className="notes-textarea"
                        rows="4"
                        placeholder="Add notes..."
                      />
                      <div className="notes-actions">
                        <button
                          onClick={() => handleSaveNotes(app.id)}
                          className="save-button"
                        >
                          ✓ Save
                        </button>
                        <button
                          onClick={() => setEditingId(null)}
                          className="cancel-button"
                        >
                          ✕ Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div
                      className="notes-display"
                      onClick={() => handleEditNotes(app.id, app.notes || '')}
                    >
                      <p className="notes-label">📝 Notes</p>
                      <p className="notes-text">
                        {app.notes || 'Click to add notes...'}
                      </p>
                    </div>
                  )}
                </div>

                <div className="app-actions">
                  <button
                    onClick={() => handleDelete(app.id)}
                    className="delete-button"
                    title="Delete application"
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard
