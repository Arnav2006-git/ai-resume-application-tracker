// Application Tracker Page Logic
let allApplications = [];

document.addEventListener('DOMContentLoaded', function() {
    loadApplications();
    setupFiltersAndSort();
    setupModal();
});

// Load applications
async function loadApplications() {
    try {
        const response = await apiCall('GET', `/applications?user_id=${USER_ID}`);
        allApplications = response.applications;
        
        if (allApplications.length === 0) {
            document.getElementById('emptyState').style.display = 'block';
            document.getElementById('applicationsContainer').innerHTML = '';
        } else {
            document.getElementById('emptyState').style.display = 'none';
            displayApplications(allApplications);
        }
        
        updateStatistics();
    } catch (error) {
        console.error('Error loading applications:', error);
        showNotification('Error loading applications.', 'error');
    }
}

// Display applications
function displayApplications(applications) {
    const container = document.getElementById('applicationsContainer');
    container.innerHTML = '';
    
    applications.forEach(app => {
        const card = createApplicationCard(app);
        container.appendChild(card);
    });
}

// Create application card
function createApplicationCard(app) {
    const card = document.createElement('div');
    card.className = 'application-card';
    
    const statusClass = app.status.toLowerCase().replace(/\s+/g, '-');
    const statusBadgeClass = `status-badge ${statusClass}`;
    
    card.innerHTML = `
        <div class="application-info">
            <div class="application-header">
                <div>
                    <div class="company-name">${app.company_name}</div>
                    <div class="job-title">${app.job_title}</div>
                </div>
                <span class="${statusBadgeClass}">${app.status}</span>
            </div>
            <div class="match-score">Match Score: ${app.match_score}%</div>
            <div style="color: #9ca3af; font-size: 12px;">Applied: ${formatDate(app.applied_date)}</div>
        </div>
        <div class="action-buttons">
            <button class="btn btn-primary" onclick="viewApplication(${app.id})">View Details</button>
            <button class="btn btn-secondary" onclick="updateStatus(${app.id})">Update Status</button>
            <button class="btn btn-danger" onclick="deleteApplication(${app.id})">Delete</button>
        </div>
    `;
    
    return card;
}

// View application details
function viewApplication(appId) {
    const app = allApplications.find(a => a.id === appId);
    if (!app) return;
    
    const modal = document.getElementById('applicationModal');
    const modalBody = document.getElementById('modalBody');
    
    let keywordsHTML = '';
    if (app.matching_keywords && app.matching_keywords.length > 0) {
        keywordsHTML += '<div style="margin-bottom: 20px;">';
        keywordsHTML += '<h5>✅ Matching Keywords</h5>';
        keywordsHTML += '<div style="display: flex; flex-wrap: wrap; gap: 8px;">';
        app.matching_keywords.slice(0, 15).forEach(kw => {
            keywordsHTML += `<span class="keyword-tag matching">${kw}</span>`;
        });
        keywordsHTML += '</div></div>';
    }
    
    if (app.missing_keywords && app.missing_keywords.length > 0) {
        keywordsHTML += '<div style="margin-bottom: 20px;">';
        keywordsHTML += '<h5>❌ Missing Keywords</h5>';
        keywordsHTML += '<div style="display: flex; flex-wrap: wrap; gap: 8px;">';
        app.missing_keywords.slice(0, 15).forEach(kw => {
            keywordsHTML += `<span class="keyword-tag missing">${kw}</span>`;
        });
        keywordsHTML += '</div></div>';
    }
    
    let suggestionsHTML = '';
    if (app.suggested_improvements && app.suggested_improvements.length > 0) {
        suggestionsHTML += '<div style="margin-bottom: 20px;">';
        suggestionsHTML += '<h5>💡 Suggestions</h5>';
        suggestionsHTML += '<ul style="list-style-position: inside;">';
        app.suggested_improvements.forEach(sugg => {
            suggestionsHTML += `<li style="margin-bottom: 8px;">${sugg}</li>`;
        });
        suggestionsHTML += '</ul></div>';
    }
    
    const statusClass = app.status.toLowerCase().replace(/\s+/g, '-');
    
    modalBody.innerHTML = `
        <h3>${app.company_name} - ${app.job_title}</h3>
        <p style="color: #6b7280; margin-bottom: 15px;">
            <span class="status-badge ${statusClass}">${app.status}</span>
            <span style="margin-left: 15px;">Match Score: ${app.match_score}%</span>
        </p>
        
        <div style="margin-bottom: 20px;">
            <h5>Details</h5>
            <p><strong>Applied:</strong> ${formatDate(app.applied_date)}</p>
            <p><strong>Deadline:</strong> ${app.deadline ? formatDate(app.deadline) : 'Not set'}</p>
            ${app.job_url ? `<p><strong>Job URL:</strong> <a href="${app.job_url}" target="_blank">${app.job_url}</a></p>` : ''}
        </div>
        
        ${keywordsHTML}
        ${suggestionsHTML}
        
        <div style="margin-bottom: 20px;">
            <h5>Notes</h5>
            <textarea id="appNotes" style="width: 100%; padding: 10px; border: 1px solid #e5e7eb; border-radius: 6px; font-family: inherit;" rows="4">${app.notes}</textarea>
            <button class="btn btn-primary" style="margin-top: 10px;" onclick="saveNotes(${app.id})">Save Notes</button>
        </div>
    `;
    
    modal.classList.remove('hidden');
}

// Update status
async function updateStatus(appId) {
    const app = allApplications.find(a => a.id === appId);
    if (!app) return;
    
    const newStatus = prompt('Update status (Applied, OA, Interview, Rejected, Offer):', app.status);
    
    if (!newStatus) return;
    
    const validStatuses = ['Applied', 'OA', 'Interview', 'Rejected', 'Offer'];
    if (!validStatuses.includes(newStatus)) {
        showNotification('Invalid status.', 'error');
        return;
    }
    
    try {
        await apiCall('PUT', `/applications/${appId}/status`, { status: newStatus });
        showNotification('Status updated!', 'success');
        loadApplications();
    } catch (error) {
        showNotification('Error updating status: ' + error.message, 'error');
    }
}

// Save notes
async function saveNotes(appId) {
    const notes = document.getElementById('appNotes').value;
    
    try {
        await apiCall('PUT', `/applications/${appId}/notes`, { notes });
        showNotification('Notes saved!', 'success');
    } catch (error) {
        showNotification('Error saving notes: ' + error.message, 'error');
    }
}

// Delete application
async function deleteApplication(appId) {
    if (!confirm('Are you sure you want to delete this application?')) return;
    
    try {
        await apiCall('DELETE', `/applications/${appId}`);
        showNotification('Application deleted!', 'success');
        loadApplications();
    } catch (error) {
        showNotification('Error deleting application: ' + error.message, 'error');
    }
}

// Update statistics
function updateStatistics() {
    const stats = {
        total: allApplications.length,
        applied: allApplications.filter(a => a.status === 'Applied').length,
        oa: allApplications.filter(a => a.status === 'OA').length,
        interview: allApplications.filter(a => a.status === 'Interview').length,
        rejected: allApplications.filter(a => a.status === 'Rejected').length,
        offer: allApplications.filter(a => a.status === 'Offer').length
    };
    
    document.getElementById('totalStat').textContent = stats.total;
    document.getElementById('appliedStat').textContent = stats.applied;
    document.getElementById('oaStat').textContent = stats.oa;
    document.getElementById('interviewStat').textContent = stats.interview;
    document.getElementById('rejectedStat').textContent = stats.rejected;
    document.getElementById('offerStat').textContent = stats.offer;
}

// Setup filters and sorting
function setupFiltersAndSort() {
    const statusFilter = document.getElementById('statusFilter');
    const sortBy = document.getElementById('sortBy');
    
    statusFilter.addEventListener('change', applyFiltersAndSort);
    sortBy.addEventListener('change', applyFiltersAndSort);
}

// Apply filters and sorting
function applyFiltersAndSort() {
    const statusFilter = document.getElementById('statusFilter').value;
    const sortBy = document.getElementById('sortBy').value;
    
    let filtered = allApplications;
    
    // Apply status filter
    if (statusFilter) {
        filtered = filtered.filter(app => app.status === statusFilter);
    }
    
    // Apply sorting
    if (sortBy === 'date-desc') {
        filtered.sort((a, b) => new Date(b.applied_date) - new Date(a.applied_date));
    } else if (sortBy === 'date-asc') {
        filtered.sort((a, b) => new Date(a.applied_date) - new Date(b.applied_date));
    } else if (sortBy === 'score-desc') {
        filtered.sort((a, b) => b.match_score - a.match_score);
    } else if (sortBy === 'score-asc') {
        filtered.sort((a, b) => a.match_score - b.match_score);
    }
    
    displayApplications(filtered);
}

// Setup modal
function setupModal() {
    const modal = document.getElementById('applicationModal');
    const closeBtn = document.querySelector('.close-btn');
    
    closeBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
}
