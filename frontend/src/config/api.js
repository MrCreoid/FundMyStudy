const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_CONFIG = {
  BASE_URL: API_URL,
  ENDPOINTS: {
    LOGIN: '/auth/login',
    PROFILE: '/profile',
    SCHOLARSHIPS: '/scholarships',
    ELIGIBILITY: '/scholarships/check-eligibility',
    SCRAPER: '/scraper/run'
  }
};