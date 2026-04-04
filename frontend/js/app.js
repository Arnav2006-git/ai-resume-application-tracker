// Global configuration and utilities
const API_BASE_URL = 'http://localhost:5000/api';
const USER_ID = localStorage.getItem('userId') || 'default_user';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set user ID
    if (!localStorage.getItem('userId')) {
        localStorage.setItem('userId', USER_ID);
    }
    
    // Load stats if on dashboard
    if (document.getElementById('stats')) {
        loadStats();
    }
});

// Fetch wrapper with error handling
async function apiCall(method, endpoint, data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `API Error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await apiCall('GET', `/applications/stats?user_id=${USER_ID}`);
        
        document.getElementById('totalApps').textContent = response.total;
        document.getElementById('appliedApps').textContent = response.applied;
        document.getElementById('interviewApps').textContent = response.interview;
        document.getElementById('offersApps').textContent = response.offer;
        document.getElementById('avgScore').textContent = response.average_score + '%';
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles if not already present
    if (!document.getElementById('notificationStyles')) {
        const style = document.createElement('style');
        style.id = 'notificationStyles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 6px;
                color: white;
                z-index: 9999;
                animation: slideIn 0.3s ease;
            }
            
            .notification-success {
                background-color: #10b981;
            }
            
            .notification-error {
                background-color: #ef4444;
            }
            
            .notification-warning {
                background-color: #f59e0b;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

// Create keyword tag
function createKeywordTag(keyword, isMatching = false) {
    const tag = document.createElement('span');
    tag.className = `keyword-tag ${isMatching ? 'matching' : 'missing'}`;
    tag.textContent = keyword;
    return tag;
}

// Validate file size
function isFileSizeValid(file, maxSizeMB = 16) {
    return file.size <= maxSizeMB * 1024 * 1024;
}

// Export data as JSON
function exportAsJSON(data, filename) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}

// Export data as CSV
function exportAsCSV(data, filename) {
    const csv = data.map(row => Object.values(row).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}

export { apiCall, USER_ID, loadStats, showNotification, formatDate, createKeywordTag, isFileSizeValid, exportAsJSON, exportAsCSV };
