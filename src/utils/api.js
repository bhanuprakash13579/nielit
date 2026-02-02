// API Configuration
// Automatically use relative path (proxy) if on Vercel, otherwise use env var or localhost
const isVercel = typeof window !== 'undefined' && window.location.hostname.includes('vercel.app');
export const API_BASE_URL = isVercel ? '' : (import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000'));

export const apiUrl = (path) => `${API_BASE_URL}${path}`;
