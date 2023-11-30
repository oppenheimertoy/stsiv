import React from 'react';
import { MDBSpinner } from 'mdb-react-ui-kit';

const LoadingSpinner = () => {
  return (
    <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
      <MDBSpinner role="status">
        <span className="visually-hidden">Loading...</span>
      </MDBSpinner>
    </div>
  );
};

export default LoadingSpinner;