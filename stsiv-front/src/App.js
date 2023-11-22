import React from 'react';
import './global.css';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'; // Import Navigate here
import LoginForm from './components/LoginForm';
import ExperimentsPage from './pages/ExperimentsPage';
import HomePage from './pages/HomePage';
import RegisterForm from './components/RegisterForm'; // Assuming you have this component for registration
import { isAuthenticated } from './utils/auth'; // Utility function for authentication check
import GlobalStyle from './GlobalStyle';

function App() {
    return (
      <>
        <GlobalStyle />
        <Router>
            <Routes>
                <Route path="/login" element={!isAuthenticated() ? <LoginForm /> : <Navigate to="/experiments" />} />
                <Route path="/register" element={!isAuthenticated() ? <RegisterForm /> : <Navigate to="/experiments" />} />
                <Route path="/experiments" element={isAuthenticated() ? <ExperimentsPage /> : <Navigate to="/login" />} />
                <Route path="/" element={<HomePage />} />
                {/* Add other routes here */}
            </Routes>
        </Router>
      </>
    );
}

export default App;
