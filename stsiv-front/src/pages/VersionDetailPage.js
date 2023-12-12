import React, { useEffect, useState } from 'react';
import apiClient from '../api/axios';
import { useParams } from 'react-router-dom';
import { MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBRow, MDBCol, MDBBtn } from 'mdb-react-ui-kit';
import CreateVersionUpdateModal from '../components/CreateVersionUpdateModal';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import LoadingSpinner from '../components/LoadingSpinner';
import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';

const VersionDetailPage = () => {
    const [versionDetails, setVersionDetails] = useState(null);
    const [results, setResults] = useState([]);
    const [selectedParam, setSelectedParam] = useState('');
    const { versionId } = useParams();
    const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
    const [parsedParameters, setParsedParameters] = useState(null);
    const [isPageLoading, setIsPageLoading] = useState(false); // Initially set to true
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isTestRunning, setIsTestRunning] = useState(false);

    useEffect(() => {
        const fetchVersionDetails = async () => {
            try {
                setIsPageLoading(true);
                const versionInfoResponse = await apiClient.get(`/version/${versionId}/info`);
                let versionData = versionInfoResponse.data;
            
                // Check if 'params' is a string and parse it if so
                if (typeof versionData.params === 'string') {
                    versionData = {
                        ...versionData,
                        params: convertEscapedJsonString(versionData.params),
                    };
                }
                setVersionDetails(versionData);
                setIsPageLoading(false);

                const resultsResponse = await apiClient.get(`/result/${versionId}/list`);
                setResults(resultsResponse.data);
            } catch (error) {
                console.error('Error fetching version details:', error);
                // Handle error
            }
        };

        fetchVersionDetails();
    }, [versionId]);

    useEffect(() => {
    if (versionDetails && versionDetails.params) {
        const parsed = parseParams(versionDetails.params);
        setParsedParameters(parsed);
    }
}, [versionDetails]);

    const handleStartTest = async () => {
        setIsTestRunning(true); // Start the test and show spinner

        try {
            await apiClient.post(`/version/${versionId}/run`);
            // Handle successful test initiation here, e.g., show a message
        } catch (error) {
            // Handle error here, e.g., show an error message
            console.error('Error starting the test:', error);
        }

        setIsTestRunning(false); // Test has started, stop showing spinner
    };

    const parseParams = (paramsString) => {
        try {
            // Replace escaped backslashes followed by quotes
            const unescapedString = paramsString.replace(/\\\\"/g, '"');
            // Parse the unescaped string as JSON
            const parsedParams = JSON.parse(unescapedString);
            // Check the result of parsing
            console.log('Parsed Params:', parsedParams);
            return parsedParams;
        } catch (e) {
            console.error("Error parsing params:", e);
            return {}; // Return an empty object in case of error
        }
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

    const convertEscapedJsonString = (escapedJsonString) => {
        try {
            return JSON.parse(escapedJsonString);
        } catch (error) {
            console.error('Error parsing escaped JSON string:', error);
            return null; // Return null or an appropriate error handling
        }
    };

    const renderParameterValues = (parameters) => {
        return Object.entries(parameters).map(([key, value]) => {
            if (typeof value === 'object' && value !== null && value.hasOwnProperty('value')) {
                return <p key={key}>{key}: {JSON.stringify(value.value)}</p>;
            }
            return null; // For safety, in case the structure is not as expected
        });
    };

    const handleUpdateParameters = async (updatedParams, file) => {
        setIsSubmitting(true);
        try {
          await apiClient.put(`/version/${versionId}/params`, updatedParams);
          if (file) {
            const formData = new FormData();
            formData.append('file', file);
            await apiClient.post(`/version/${versionId}/upload`, formData);
            setIsSubmitting(false);
          }
        } catch (error) {
          console.error('Error updating version:', error);
          setIsSubmitting(false);
        }
      };

    const handleChange = (event) => {
        setSelectedParam(event.target.value);
    };

    const formatParameters = (params) => {
        return JSON.stringify(params, null, 2); // Pretty print the parameters
    };


    if (isPageLoading || isSubmitting) {
        return (
            <LoadingSpinner />
        )
    } else {

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
                                <FormControl fullWidth variant="outlined" sx={{ 
                                    '& .MuiOutlinedInput-root': {
                                        '& fieldset': {
                                            borderColor: '#fff', // White border
                                        },
                                        '&:hover fieldset': {
                                            borderColor: '#fff', // White border on hover
                                        },
                                        '&.Mui-focused fieldset': {
                                            borderColor: '#fff', // White border on focus
                                        }
                                    },
                                    '& .MuiInputLabel-root': {
                                        color: '#fff', // White label text
                                    }
                                }}>
                                    <InputLabel id="param-select-label">Select attribute</InputLabel>
                                    <Select
                                        labelId="param-select-label"
                                        id="param-select"
                                        value={selectedParam}
                                        label="Select attribute"
                                        onChange={handleChange}
                                        sx={{
                                            color: '#fff', // Set text color to white
                                            '& .MuiSvgIcon-root': { color: '#fff' }, // Set dropdown icon color to white
                                        }}
                                    >
                                        {Object.keys(versionDetails.params).map((paramKey) => (
                                            <MenuItem key={paramKey} value={paramKey} sx={{ color: '#000' }}>
                                                {paramKey}
                                            </MenuItem>
                                        ))}
                                    </Select>
                        </FormControl>
                        <pre>
                            {selectedParam && JSON.stringify(versionDetails.params[selectedParam], null, 2)}
                        </pre>
                                {/* {renderParameterValues(versionDetails.params)} */}
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
                                    <MDBCardText>{result.name}</MDBCardText>
                                </MDBCardBody>
                            </MDBCard>
                        )) : (
                            <p className="text-white">No results found.</p>
                        )}
                        <MDBBtn type="button" style={buttonStyle} className="my-4" onClick={() => setIsUpdateModalOpen(true)}>Update Parameters</MDBBtn>
                        <CreateVersionUpdateModal
                            isOpen={isUpdateModalOpen}
                            toggle={() => setIsUpdateModalOpen(false)}
                            onUpdate={handleUpdateParameters}
                        />
                        <Button
                            variant="contained"
                            onClick={handleStartTest}
                            disabled={isTestRunning}
                            startIcon={isTestRunning && <CircularProgress size={20} />}
                        >
                            {isTestRunning ? 'Starting Test...' : 'Start Test'}
                        </Button>
                    </div>
                </MDBCol>
            </MDBRow>
        </div>
    );
   }
};

export default VersionDetailPage;
