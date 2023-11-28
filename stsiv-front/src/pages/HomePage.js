import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MDBBtn } from 'mdb-react-ui-kit';

const HomePage = () => {
    const navigate = useNavigate();
    
    const buttonStyle = {
        backgroundColor: '#4CAF50', // Green background color for the button
        borderColor: '#4CAF50',
        color: '#fff', // White text color
        margin: '10px', // Margin for spacing between buttons
    };

    const textStyle = {
        color: '#fff', // White text color
    };

    return (
        <div className="container my-5" style={textStyle}>
            <h1 className="text-center mb-4">STSIV</h1>
            <p>This project is a considerably improved version of the NIST Statistical Test Suite (STS), a collection of tests used in the evaluation of the randomness of bitstreams of data.</p>
            
            <h2 className="mt-4">Purpose</h2>
            <p>STS can be useful in:</p>
            <ul>
                <li>Evaluating the randomness of bitstreams produced by hardware and software key generators for cryptographic applications.</li>
                <li>Evaluating the quality of pseudo random number generators used in simulation and modeling applications.</li>
            </ul>

            <div className="text-center mt-5">
                <MDBBtn style={buttonStyle} onClick={() => navigate('/login')}>Sign In</MDBBtn>
                <MDBBtn style={buttonStyle} onClick={() => navigate('/register')}>Sign Up</MDBBtn>
            </div>
        </div>
    );
};

export default HomePage;
