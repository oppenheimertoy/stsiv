const isAuthenticated = () => {
    return localStorage.getItem('accessToken') !== null;
};
export { isAuthenticated };
