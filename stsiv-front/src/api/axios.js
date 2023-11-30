import axios from 'axios';
import { refreshAccessToken } from './authService';

// Create an Axios instance to attach the interceptor
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/v1/',
});

apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Add a response interceptor
apiClient.interceptors.response.use(undefined, async (error) => {
  const originalRequest = error.config;
  
  // Check if we received a 401 Unauthorized response
  if (error.response.status === 401 && !originalRequest._retry) {
    
    // Mark this request as already tried
    originalRequest._retry = true;
    
    try {
      // Get a new token
      const newAccessToken = await refreshAccessToken();
      
      // Update the authorization header with the new token
      originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
      
      // Return the original request with the new access token
      return apiClient(originalRequest);
    } catch (refreshError) {
      // If token refresh fails, you might want to force a logout here
      return Promise.reject(refreshError);
    }
  }
  
  // If the error wasn't a 401, continue with the error
  return Promise.reject(error);
});

export default apiClient;