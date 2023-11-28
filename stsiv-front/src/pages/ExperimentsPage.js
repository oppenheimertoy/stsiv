import React, { useEffect, useState } from 'react';
import apiClient from '../api/axios';
import { useNavigate } from 'react-router-dom';
import { MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBCol } from 'mdb-react-ui-kit';

const ExperimentsPage = () => {
    const [experiments, setExperiments] = useState([]);
    const [userData, setUserData] = useState(null);
    const navigate = useNavigate();

    const userInfo = {
        name: "User Name",
        email: "user@example.com"
    };

    useEffect(() => {
        const fetchExperiments = async () => {
            try {
                const response = await apiClient.get('/experiment/list');
                setExperiments(response.data);
                const userResponse = await apiClient.get('/user/me'); // Adjust the endpoint as necessary
                setUserData(userResponse.data);
            } catch (error) {
                console.error('Failed to fetch experiments:', error);
            }
        };

        fetchExperiments();
    }, []);

    const handleExperimentClick = (experimentId) => {
        navigate(`/experiment/${experimentId}`);
    };

    return (
        <div className="container mt-4">
            <div className="row">
                {/* User Info Section */}
                <div className="col-md-4">
                    {userData && (
                        <MDBCard className="mb-4">
                            <MDBCardBody>
                                <MDBCardTitle>User Information</MDBCardTitle>
                                <MDBCardText>Email: {userData.email}</MDBCardText>
                                <MDBCardText>Username: {userData.username}</MDBCardText>
                            </MDBCardBody>
                        </MDBCard>
                    )}
                </div>

                <div className="col-md-8">
                    <h2>Experiments</h2>
                    <div className="experiments-list">
                        {experiments.length > 0 ? experiments.map(experiment => (
                            <MDBCol key={experiment.id} className="mb-4">
                                <MDBCard style={{ cursor: 'pointer' }} onClick={() => handleExperimentClick(experiment.id)}>
                                    <MDBCardBody>
                                        <MDBCardTitle>{experiment.name}</MDBCardTitle>
                                        <MDBCardText>Description: {experiment.description}</MDBCardText>
                                        <MDBCardText>Versions: {experiment.versions_num}</MDBCardText>
                                    </MDBCardBody>
                                </MDBCard>
                            </MDBCol>
                        )) : (
                            <p>No experiments found.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ExperimentsPage;
