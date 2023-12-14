import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';
import { MDBCard, MDBCardBody } from 'mdb-react-ui-kit';
import apiClient from '../api/axios';

const TestResultPage = () => {
  const { resultId } = useParams();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [imageOne, setImageOne] = useState('');
  const [imageTwo, setImageTwo] = useState('');
  const [downloadLink, setDownloadLink] = useState('');

  useEffect(() => {
    const fetchImageData = async (imageUrl) => {
      try {
        const response = await apiClient.get(imageUrl, { responseType: 'blob' });
        return URL.createObjectURL(response.data);
      } catch (error) {
        console.error('Error fetching image:', error);
        throw error;
      }
    };

    const getResult = async () => {
      try {
        await apiClient.post(`/result/${resultId}/getResult`);
        const imageUrlOne = `/result/${resultId}/getPval`;
        const imageUrlTwo = `/result/${resultId}/getCustom`;
        const downloadUrl = `/result/${resultId}/download.txt`;

        // Fetch and set image URLs
        const localImageUrlOne = await fetchImageData(imageUrlOne);
        const localImageUrlTwo = await fetchImageData(imageUrlTwo);
        setImageOne(localImageUrlOne);
        setImageTwo(localImageUrlTwo);
        setDownloadLink(downloadUrl);

        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching test result details:', error);
        navigate('/error');
      }
    };

    getResult();
  }, [resultId, navigate]);

  const handleDownload = () => {
    window.open(downloadLink, '_blank');
  };

  if (isLoading) {
    return <div>Loading...</div>; // Or use a spinner component
  }

  return (
    <div className="container mt-4">
      <MDBCard>
        <MDBCardBody>
          <img src={imageOne} alt="P-Value Image" style={{ width: '100%', marginBottom: '20px' }} />
          <img src={imageTwo} alt="Custom Plot Image" style={{ width: '100%', marginBottom: '20px' }} />
          <Button onClick={handleDownload} variant="contained" color="primary">
            Download Results
          </Button>
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default TestResultPage;
