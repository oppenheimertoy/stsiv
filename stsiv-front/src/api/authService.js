import axios from './axios';

const login = async (token, password) => {
    const response = await axios.post('user/sign-in', { token, password });
    localStorage.setItem('token', response.data.token);
    return response.data;
};

const logout = () => {
    localStorage.removeItem('token');
    // Additional logout logic
};

export { login, logout };

