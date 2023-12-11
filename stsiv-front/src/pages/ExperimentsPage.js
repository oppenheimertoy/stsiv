import React, { useEffect, useState } from 'react';
import apiClient from '../api/axios';
import { useNavigate } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';
import { MDBBtn, MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBRow, MDBCol } from 'mdb-react-ui-kit';
import CreateExperimentModal from '../components/CreateExperimentModal';

const ExperimentsPage = () => {
    const [experiments, setExperiments] = useState([]);
    const [userData, setUserData] = useState(null);
    const [isPageLoading, setIsPageLoading] =  useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false); // State for modal visibility
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
        navigate('/login'); // Redirect to the landing page
    };

    const toggleModal = () => {
        setIsModalOpen(!isModalOpen);
    };

    const handleCreateExperiment = async (name, description) => {
        try {
            const response = await apiClient.post('/experiment/create', { name, description });
            const newExperimentId = response.data.id;
            navigate(`/experiment/${newExperimentId}`);
        } catch (error) {
            console.error('Error creating experiment:', error);
            // Handle errors (e.g., show error message)
        }
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

    const buttonStyle = {
        backgroundColor: '#3c5920', // Green background for the button
        borderColor: '#4CAF50',
        color: '#fff', // White text color for the button
        maxWidth: '200px',
        margin: '0 auto',
        height: 38
    };

    if (isPageLoading) {
        return (
            <LoadingSpinner />
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
                        <CreateExperimentModal isOpen={isModalOpen} toggle={toggleModal} onCreate={handleCreateExperiment} />
                        <MDBBtn type="button" style={buttonStyle} className="my-4" onClick={toggleModal}>Create New Experiment</MDBBtn>
                    </MDBCol>
                </MDBRow>
            </div>
        );
    }
};

export default ExperimentsPage;