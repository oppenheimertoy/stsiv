import React, { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { isAuthenticated } from '../utils/auth';

const ProtectedRoute = () => {
    const [authStatus, setAuthStatus] = useState({ checked: false, isAuthenticated: false });

    useEffect(() => {
        const verifyAuth = async () => {
            const isAuth = await isAuthenticated();
            setAuthStatus({ checked: true, isAuthenticated: isAuth });
        };

        verifyAuth();
    }, []);

    if (!authStatus.checked) {
        // You can replace this with a loading spinner or a splash screen if you like
        return <div>Checking authentication...</div>;
    }

    return authStatus.isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoute;