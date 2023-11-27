import React, { useEffect, useState } from 'react';
import apiClient from '../api/axios';
import { useNavigate } from 'react-router-dom'; // For navigation on click

const ExperimentsPage = () => {
    const [experiments, setExperiments] = useState([]);
    const navigate = useNavigate();

    // Dummy user info - replace with real data
    const userInfo = {
        name: "User Name",
        email: "user@example.com"
    };

    useEffect(() => {
        const fetchExperiments = async () => {
            try {
                const response = await apiClient.get('/experiment/list');
                setExperiments(response.data);
            } catch (error) {
                console.error('Failed to fetch experiments:', error);
            }
        };

        fetchExperiments();
    }, []);

    const handleExperimentClick = (experimentId) => {
        // Navigate to the experiment detail page
        navigate(`/experiment/${experimentId}`);
    };

    return (
        <div className="container mt-4">
            <div className="row">
                {/* User Info Section */}
                <div className="col-md-4">
                    <div className="user-info">
                        <h4>User Information</h4>
                        <p>Name: {userInfo.name}</p>
                        <p>Email: {userInfo.email}</p>
                    </div>
                </div>

                {/* Experiments List */}
                <div className="col-md-8">
                    <h2>Experiments</h2>
                    <div className="experiments-list">
                        {experiments.length > 0 ? (
                            experiments.map(experiment => (
                                <div key={experiment.id} className="experiment-block" onClick={() => handleExperimentClick(experiment.id)}>
                                    <h3>{experiment.name}</h3>
                                    <p>Description: {experiment.description}</p>
                                    <p>Versions: {experiment.versions_num}</p>
                                </div>
                            ))
                        ) : (
                            <p>No experiments found.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ExperimentsPage;
