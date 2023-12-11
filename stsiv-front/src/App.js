import React from 'react';
import './global.css';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'; // Import Navigate here
import LoginForm from './components/LoginForm';
import ExperimentsPage from './pages/ExperimentsPage';
import HomePage from './pages/HomePage';
import RegisterForm from './components/RegisterForm'; // Assuming you have this component for registration
import {isAuthenticated} from './utils/auth'
import GlobalStyle from './GlobalStyle';
import ProtectedRoute from './components/ProtectedRoute';
import ExperimentDetailPage from './pages/ExperimentDetailPage';
import VersionDetailPage from './pages/VersionDetailPage';

function App() {
    return (
      <>
        <GlobalStyle />
        <Router>
            <Routes>
                <Route element={<ProtectedRoute />}>
                  <Route path="/experiments" element={isAuthenticated() ? <ExperimentsPage /> : <Navigate to="/login" />} />
                  <Route path="/experiment/:experimentId" element={<ExperimentDetailPage />} />
                  <Route path="/experiment/:experimentId/version/:versionId" element={<VersionDetailPage />} />
                  <Route index element={isAuthenticated() ? <ExperimentsPage /> : <Navigate to="/login" />} />
                </Route>
                <Route path="/login" element={isAuthenticated() ? <LoginForm /> : <Navigate to="/experiments" />} />
                <Route path="/register" element={isAuthenticated() ? <RegisterForm /> : <Navigate to="/experiments" />} />
                <Route path="/" element={isAuthenticated() ? <HomePage /> : <Navigate to="/experiments" />} />
            </Routes>
        </Router>
      </>
    );
}

export default App;
