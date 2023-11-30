import { refreshAccessToken, logout } from "../api/authService";

const isAuthenticated = async () => {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');

    // If there is an access token, we assume the user is authenticated
    if (accessToken != null) {
        console.log("Some shit")
        return true;
    }

    // If there's no access token but there is a refresh token, try to refresh the token
    if (refreshToken) {
        try {
            const newAccessToken = await refreshAccessToken(); // Use the refresh function from authService
            return Boolean(newAccessToken); // Return true if the token has been successfully refreshed
        } catch (error) {
            // If token refresh fails (e.g., refresh token is invalid or expired)
            console.error('Session expired or user is not authenticated:', error);
            logout(); // Clear tokens and handle logout
            return false;
        }
    }

    // If neither token is present, the user is not authenticated
    return false;
};

export { isAuthenticated };