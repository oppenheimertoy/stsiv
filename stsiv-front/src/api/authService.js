import apiClient from './axios'; // Assume this is the Axios instance with the interceptor from the previous message

const login = async (token, password) => {
    const response = await apiClient.post('/user/sign-in', { token, password });
    // Assuming the API response contains access_token and refresh_token
    localStorage.setItem('accessToken', response.data.token);
    localStorage.setItem('refreshToken', response.data.refresh_token);
    return response;
};

const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    // Additional logout logic, such as redirecting the user
};

// Function to refresh the access token
const refreshAccessToken = async () => {
    // This function could be called from the Axios interceptor when needed
    try {
        const response = await apiClient.post('/user/refresh', {
            token: localStorage.getItem('accessToken'),
            refresh_token: localStorage.getItem('refreshToken')
        });
        const { token, refresh_token } = response.data;
        localStorage.setItem('accessToken', token);
        if (refresh_token) { // If a new refresh token is provided
            localStorage.setItem('refreshToken', refresh_token);
        }
        return token;
    } catch (error) {
        console.error('Error refreshing access token:', error);
        // If token refresh fails, handle accordingly, e.g., redirect to login
        logout(); // Clear tokens and handle logout
        throw error;
    }
};

export { login, logout, refreshAccessToken };

