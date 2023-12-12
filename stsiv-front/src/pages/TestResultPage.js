import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';
import { MDBCard, MDBCardBody, MDBCardImage } from 'mdb-react-ui-kit';

const TestResultPage = () => {
  const { resultId } = useParams();
  const navigate = useNavigate();
  const [imageOne, setImageOne] = useState('');
  const [imageTwo, setImageTwo] = useState('');
  const [downloadLink, setDownloadLink] = useState('');

  useEffect(() => {
    // Replace with actual API calls
    const fetchImages = async () => {
      const imageUrlOne = `/result/${resultId}/image1.png`;
      const imageUrlTwo = `/result/${resultId}/image2.png`;
      setImageOne(imageUrlOne);
      setImageTwo(imageUrlTwo);
    };

    const fetchDownloadLink = async () => {
      const downloadUrl = `/result/${resultId}/download.txt`;
      setDownloadLink(downloadUrl);
    };

    fetchImages();
    fetchDownloadLink();
  }, [resultId]);

  const handleDownload = () => {
    // Trigger the download
    window.open(downloadLink, '_blank');
  };

  return (
    <div className="container mt-4">
      <MDBCard>
        <MDBCardBody>
          <MDBCardImage src={imageOne} alt="Image One" fluid />
          <MDBCardImage src={imageTwo} alt="Image Two" fluid />
          <Button onClick={handleDownload} variant="contained" color="primary">
            Download Results
          </Button>
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default TestResultPage;
