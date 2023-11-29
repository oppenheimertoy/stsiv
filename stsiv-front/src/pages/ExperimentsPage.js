import React, { useEffect, useState } from 'react';
import apiClient from '../api/axios';
import { useNavigate } from 'react-router-dom';
import { MDBBtn, MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBRow, MDBCol } from 'mdb-react-ui-kit';

const ExperimentsPage = () => {
    const [experiments, setExperiments] = useState([]);
    const [userData, setUserData] = useState(null);
    const [isPageLoading, setIsPageLoading] =  useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsPageLoading(true);
                const expResponse = await apiClient.get('/experiment/list');
                setExperiments(expResponse.data);

                const userResponse = await apiClient.get('/user/me'); // Adjust the endpoint as necessary
                setUserData(userResponse.data);
                setIsPageLoading(false);
            } catch (error) {
                console.error('Failed to fetch data:', error);
            }
        };

        fetchData();
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        navigate('/'); // Redirect to the landing page
    };

    const handleCreateNewExperiment = () => {
        navigate('/create-experiment'); // Redirect to the experiment creation page (adjust the path as needed)
    }; 

    const handleExperimentClick = (experimentId) => {
        navigate(`/experiment/${experimentId}`);
    };

    const cardStyle = {
        backgroundColor: '#2A2A2A', // Dark background color for the card
        color: '#fff', // White text color
        borderRadius: '15px', // Rounded corners for the card
    };

    if (isPageLoading) {
        return (
            <div>Loading page...</div>
        )
    } else {
        return (
            <div className="container mt-4">
                <MDBRow>
                    {/* User Info Section */}
                    {userData && (
                        <MDBCol md="4">
                            <MDBCard style={cardStyle}>
                                <MDBCardBody>
                                    <MDBCardTitle>User Information</MDBCardTitle>
                                    <MDBCardText>Email: {userData.email}</MDBCardText>
                                    <MDBCardText>Username: {userData.username}</MDBCardText>
                                    <MDBBtn color="danger" onClick={handleLogout}>Logout</MDBBtn>
                                </MDBCardBody>
                            </MDBCard>
                        </MDBCol>
                    )}
    
                    {/* Experiments List and New Experiment Button */}
                    <MDBCol md="8">
                        <h2 className="text-white">Experiments</h2>
                        <div className="experiments-list">
                            {experiments.length > 0 ? (
                                    <div className="d-flex flex-column">
                                        {experiments.map((experiment, index) => (
                                            <MDBCard key={experiment.id} style={cardStyle} onClick={() => handleExperimentClick(experiment.id)} className={index !== 0 ? "mt-3" : ""}>
                                                <MDBCardBody>
                                                    <MDBCardTitle>{experiment.name}</MDBCardTitle>
                                                    <MDBCardText>Description: {experiment.description}</MDBCardText>
                                                    <MDBCardText>Versions: {experiment.versions_num}</MDBCardText>
                                                </MDBCardBody>
                                            </MDBCard>
                                        ))}
                                    </div>
                                ) : (
                                    <p className="text-white">No experiments found.</p>
                                )}
                            {/* ... experiments map ... */}
                        </div>
                        {/* Create New Experiment Button */}
                        <MDBBtn color="info" onClick={handleCreateNewExperiment} className="my-4">Create New Experiment</MDBBtn>
                    </MDBCol>
                </MDBRow>
            </div>
        );
    }
};

export default ExperimentsPage;