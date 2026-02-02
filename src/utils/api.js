// API Configuration
// Uses environment variable in production, falls back to localhost for development
// Uses environment variable in production, or defaults to relative path (proxy)
// Falls back to localhost only in development
export const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000');

export const apiUrl = (path) => `${API_BASE_URL}${path}`;
