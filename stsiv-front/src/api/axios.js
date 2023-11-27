import axios from 'axios';


// Helper function to refresh the token
const refreshAccessToken = async () => {
  try {
    // Send a request to the refresh endpoint with the stored refresh token
    const response = await axios.post('/refresh', {
      refresh_token: localStorage.getItem('refreshToken'), // Use the correct key for your stored refresh token
    });
    const { token, refresh_token } = response.data;
    
    // Store the new tokens
    localStorage.setItem('accessToken', token);
    localStorage.setItem('refreshToken', refresh_token);
    
    return token;
  } catch (error) {
    console.error('Error refreshing access token:', error);
    // Handle errors, e.g., redirect to login if refresh fails
    throw error;
  }
};

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