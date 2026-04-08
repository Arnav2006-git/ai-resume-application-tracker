/**
 * API Service - Handle all backend communication
 */

// Get API base URL from environment or use default
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api';

// Utility to handle API responses
const handleResponse = async (response) => {
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'An error occurred');
  }
  return data;
};

// Utility to make API requests
const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  return handleResponse(response);
};

/**
 * Resume API endpoints
 */
export const resumeAPI = {
  // Upload resume file
  upload: async (file, userId = 'default_user') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    const response = await fetch(`${API_BASE_URL}/resume/upload`, {
      method: 'POST',
      body: formData,
      // Note: Do NOT set Content-Type header, browser will set it with boundary
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || 'Upload failed');
    }

    return response.json();
  },

  // Get resume for user
  get: async (userId = 'default_user') => {
    return apiCall('/resume/get', {
      method: 'GET',
    });
  },

  // Delete resume
  delete: async (userId = 'default_user') => {
    return apiCall('/resume/delete', {
      method: 'DELETE',
    });
  },
};

/**
 * Matching API endpoints
 */
export const matchingAPI = {
  // Quick match without database save
  quickMatch: async (resumeText, jobDescription) => {
    return apiCall('/matching/quick-match', {
      method: 'POST',
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
      }),
    });
  },

  // Full match with database save
  match: async (jobDescription, companyName = '', jobTitle = '', userId = 'default_user') => {
    return apiCall('/matching/match', {
      method: 'POST',
      body: JSON.stringify({
        user_id: userId,
        job_description: jobDescription,
        company_name: companyName,
        job_title: jobTitle,
      }),
    });
  },
};

/**
 * Health check
 */
export const apiHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`);
    return response.ok;
  } catch {
    return false;
  }
};
