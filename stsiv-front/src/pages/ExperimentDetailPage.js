// ExperimentDetailPage.js
import React, { useEffect, useState } from 'react';
import apiClient from '../api/axios';
import { useNavigate, useParams } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';
import { MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBRow, MDBCol, MDBBtn } from 'mdb-react-ui-kit';

const ExperimentDetailPage = () => {
    const [experiment, setExperiment] = useState(null);
    const [versions, setVersions] = useState([]);
    const { experimentId } = useParams(); // This assumes you're using URL params
    const [isPageLoading, setIsPageLoading] =  useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchExperimentDetails = async () => {
            try {
                setIsPageLoading(true);
                const experimentResponse = await apiClient.get(`/experiment/${experimentId}/info`);
                setExperiment(experimentResponse.data);

                // Assuming your API expects a POST request for version list
                const versionsResponse = await apiClient.get(`/version/${experimentId}/list`); 
                setVersions(versionsResponse.data);
                setIsPageLoading(false);
            } catch (error) {
                console.error('Failed to fetch experiment details:', error);
                navigate('/experiments');
            }
        };

        fetchExperimentDetails();
    }, [experimentId, navigate]);

    const handleVersionClick = (versionId) => {
        navigate(`/experiment/${experimentId}/version/${versionId}`);
    };

    const handleGoBack = () => {
        navigate(-1); // Go back to the previous page
    };

    const handleCreateVersion = () => {
        navigate(`/experiment/${experimentId}/create-version`); // Adjust the route as necessary
    };

    const cardStyle = {
        backgroundColor: '#2A2A2A', // Dark background color for the card
        color: '#fff', // White text color
        borderRadius: '15px', // Rounded corners for the card
        margin: '10px' // Margin for spacing
    };

    if (isPageLoading) {
        return (
            <LoadingSpinner />
        )
    } else {

    return (
        <div className="container mt-4">
            <MDBRow>
                {/* Experiment Info Section */}
                {experiment && (
                    <MDBCol md="4">
                        <MDBCard style={cardStyle}>
                            <MDBCardBody>
                                <MDBCardTitle>Experiment Information</MDBCardTitle>
                                <MDBCardText>Name: {experiment.name}</MDBCardText>
                                <MDBCardText>Description: {experiment.description}</MDBCardText>
                                {/* Add more experiment details here */}
                                <MDBBtn color="secondary" onClick={handleGoBack}>Go Back</MDBBtn>
                            </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                )}

                {/* Versions List Section */}
                <MDBCol md="8">
                    <h2 className="text-white">Versions</h2>
                    <div className="versions-list" style={{ maxHeight: 'calc(100vh - 200px)', overflowY: 'auto' }}>
                        {versions.length > 0 ? versions.map(version => (
                            <MDBCard key={version.id} style={cardStyle} onClick={() => handleVersionClick(version.id)}>
                                <MDBCardBody>
                                    <MDBCardTitle>{version.name}</MDBCardTitle>
                                    <MDBCardText>Description: {version.description}</MDBCardText>
                                    {/* Add more version details here */}
                                </MDBCardBody>
                            </MDBCard>
                        )) : (
                            <p className="text-white">No versions found.</p>
                        )}
                    </div>
                </MDBCol>
            </MDBRow>
        </div>
    );
  }
};

export default ExperimentDetailPage;
