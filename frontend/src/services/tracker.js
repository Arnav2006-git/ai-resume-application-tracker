/**
 * Tracker Service - Manage job applications data
 */

const STORAGE_KEY = 'resume_match_applications';

// Generate unique ID for each application
const generateId = () => `app_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

// Status constants
export const APPLICATION_STATUSES = {
  APPLIED: 'Applied',
  OA: 'OA',
  INTERVIEW: 'Interview',
  REJECTED: 'Rejected',
  OFFER: 'Offer',
};

// Status colors for UI
export const STATUS_COLORS = {
  Applied: '#6366f1',
  OA: '#f59e0b',
  Interview: '#8b5cf6',
  Rejected: '#ef4444',
  Offer: '#10b981',
};

/**
 * Get all applications
 */
export const getApplications = () => {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error('Error loading applications:', error);
    return [];
  }
};

/**
 * Add new application
 */
export const addApplication = (appData) => {
  try {
    const applications = getApplications();
    const newApplication = {
      id: generateId(),
      ...appData,
      matchScore: appData.matchScore || 0,
      matchedKeywords: appData.matchedKeywords || [],
      missingKeywords: appData.missingKeywords || [],
      suggestions: appData.suggestions || [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      notes: appData.notes || '',
    };
    applications.push(newApplication);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(applications));
    return newApplication;
  } catch (error) {
    console.error('Error adding application:', error);
    throw error;
  }
};

/**
 * Update application status
 */
export const updateApplicationStatus = (appId, newStatus) => {
  try {
    const applications = getApplications();
    const index = applications.findIndex((app) => app.id === appId);
    if (index === -1) throw new Error('Application not found');

    applications[index].status = newStatus;
    applications[index].updatedAt = new Date().toISOString();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(applications));
    return applications[index];
  } catch (error) {
    console.error('Error updating application status:', error);
    throw error;
  }
};

/**
 * Update application notes
 */
export const updateApplicationNotes = (appId, notes) => {
  try {
    const applications = getApplications();
    const index = applications.findIndex((app) => app.id === appId);
    if (index === -1) throw new Error('Application not found');

    applications[index].notes = notes;
    applications[index].updatedAt = new Date().toISOString();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(applications));
    return applications[index];
  } catch (error) {
    console.error('Error updating application notes:', error);
    throw error;
  }
};

/**
 * Delete application
 */
export const deleteApplication = (appId) => {
  try {
    let applications = getApplications();
    applications = applications.filter((app) => app.id !== appId);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(applications));
  } catch (error) {
    console.error('Error deleting application:', error);
    throw error;
  }
};

/**
 * Get application by ID
 */
export const getApplicationById = (appId) => {
  try {
    const applications = getApplications();
    return applications.find((app) => app.id === appId);
  } catch (error) {
    console.error('Error getting application:', error);
    return null;
  }
};

/**
 * Get applications grouped by status
 */
export const getApplicationsByStatus = (status) => {
  try {
    const applications = getApplications();
    return applications.filter((app) => app.status === status);
  } catch (error) {
    console.error('Error getting applications by status:', error);
    return [];
  }
};

/**
 * Get statistics
 */
export const getApplicationStats = () => {
  try {
    const applications = getApplications();
    const stats = {
      total: applications.length,
      applied: applications.filter((a) => a.status === APPLICATION_STATUSES.APPLIED).length,
      oa: applications.filter((a) => a.status === APPLICATION_STATUSES.OA).length,
      interview: applications.filter((a) => a.status === APPLICATION_STATUSES.INTERVIEW).length,
      rejected: applications.filter((a) => a.status === APPLICATION_STATUSES.REJECTED).length,
      offer: applications.filter((a) => a.status === APPLICATION_STATUSES.OFFER).length,
    };
    return stats;
  } catch (error) {
    console.error('Error calculating stats:', error);
    return {
      total: 0,
      applied: 0,
      oa: 0,
      interview: 0,
      rejected: 0,
      offer: 0,
    };
  }
};
