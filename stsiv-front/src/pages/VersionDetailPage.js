import React, { useEffect, useState } from 'react';
import apiClient from '../api/axios';
import { useParams } from 'react-router-dom';
import { MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBRow, MDBCol } from 'mdb-react-ui-kit';

const VersionDetailPage = () => {
    const [versionDetails, setVersionDetails] = useState(null);
    const [results, setResults] = useState([]);
    const { versionId } = useParams();

    useEffect(() => {
        const fetchVersionDetails = async () => {
            try {
                const versionInfoResponse = await apiClient.get(`/version/${versionId}/info`);
                setVersionDetails(versionInfoResponse.data);

                const resultsResponse = await apiClient.get(`/result/${versionId}/list`);
                setResults(resultsResponse.data);
            } catch (error) {
                console.error('Error fetching version details:', error);
                // Handle error
            }
        };

        fetchVersionDetails();
    }, [versionId]);

    const cardStyle = {
        backgroundColor: '#2A2A2A', // Dark background color for the card
        color: '#fff', // White text color
        borderRadius: '15px', // Rounded corners for the card
    };

    const renderParameterValues = (parameters) => {
        return Object.entries(parameters).map(([key, value]) => {
            if (typeof value === 'object' && value !== null && value.hasOwnProperty('value')) {
                return <p key={key}>{key}: {JSON.stringify(value.value)}</p>;
            }
            return null; // For safety, in case the structure is not as expected
        });
    };

    return (
        <div className="container mt-4">
            <MDBRow>
                {/* Version Info Section */}
                {versionDetails && (
                    <MDBCol md="6">
                        <MDBCard style={cardStyle}>
                            <MDBCardBody>
                                <MDBCardTitle>Version Information</MDBCardTitle>
                                <MDBCardText>Name: {versionDetails.name}</MDBCardText>
                                <MDBCardText>Description: {versionDetails.description}</MDBCardText>
                                <MDBCardTitle>Version Parameters</MDBCardTitle>
                                {renderParameterValues(versionDetails.params)}
                            </MDBCardBody>
                        </MDBCard>
                    </MDBCol>
                )}
                <MDBCol md="6">
                    <h2 className="text-white">Results</h2>
                    <div className="results-list">
                        {results.length > 0 ? results.map(result => (
                            <MDBCard key={result.id} style={cardStyle}>
                                <MDBCardBody>
                                    {/* Display result details here */}
                                    <MDBCardText>Result ID: {result.id}</MDBCardText>
                                </MDBCardBody>
                            </MDBCard>
                        )) : (
                            <p className="text-white">No results found.</p>
                        )}
                    </div>
                </MDBCol>
            </MDBRow>
        </div>
    );
};

export default VersionDetailPage;
