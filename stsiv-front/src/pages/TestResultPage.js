import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { MDBCard, MDBCardBody } from 'mdb-react-ui-kit';
import apiClient from '../api/axios';

const TestResultPage = () => {
  const { resultId } = useParams();
  const [isLoading, setIsLoading] = useState(true);
  const [imageOne, setImageOne] = useState('');
  const [imageTwo, setImageTwo] = useState('');
  const [statsDownloadUrl, setStatsDownloadUrl] = useState('');

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

    const fetchStatsFile = async () => {
      try {
        const response = await apiClient.get(`/result/${resultId}/getStats`, { responseType: 'blob' });
        return URL.createObjectURL(response.data);
      } catch (error) {
        console.error('Error fetching stats file:', error);
        throw error;
      }
    };

    const getResult = async () => {
      try {
        await apiClient.post(`/result/${resultId}/getResult`);
        const imageUrlOne = `/result/${resultId}/getPval`;
        const imageUrlTwo = `/result/${resultId}/getCustom`;

        // Fetch and set image URLs
        const localImageUrlOne = await fetchImageData(imageUrlOne);
        const localImageUrlTwo = await fetchImageData(imageUrlTwo);
        setImageOne(localImageUrlOne);
        setImageTwo(localImageUrlTwo);

        // Fetch and set stats file URL
        const localStatsUrl = await fetchStatsFile();
        setStatsDownloadUrl(localStatsUrl);

        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching test result details:', error);
      }
    };

    getResult();
  }, [resultId]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mt-4">
      <MDBCard>
        <MDBCardBody>
          <img src={imageOne} alt="P-Value Image" style={{ width: '100%', marginBottom: '20px' }} />
          <img src={imageTwo} alt="Custom Plot Image" style={{ width: '100%', marginBottom: '20px' }} />
          <a href={statsDownloadUrl} download="stats.txt">
            <button className="btn btn-primary">Download Statistics</button>
          </a>
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default TestResultPage;
