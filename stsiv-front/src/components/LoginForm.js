import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/authService';
import {
  MDBBtn,
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBCardImage,
  MDBRow,
  MDBCol,
  MDBInput
} from 'mdb-react-ui-kit';

import { TypeAnimation } from 'react-type-animation';

const LoginForm = () => {
    const [token, setToken] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            await login(token, password); // Call the login function
            navigate('/experiments'); // Navigate to the experiments page on successful login
        } catch (error) {
            console.error('Login error', error);
            // Optionally handle login errors (e.g., show an error message)
        }
    };

    const cardStyle = {
        backgroundColor: '#2A2A2A', // Dark background color for the card
        color: '#fff', // White text color
        borderRadius: '15px' // Optional: if you want rounded corners
    };

    const formContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center', // Center the form vertically
        height: '100%', // Take full height of the column
        marginTop: '-100px'
    };

    const buttonStyle = {
        backgroundColor: '#3c5920', // Green background for the button
        borderColor: '#4CAF50',
        color: '#fff', // White text color for the button
        maxWidth: '200px',
        margin: '0 auto'
    };

    const overlayStyle = {
        position: 'absolute',
        top: 0,
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.1)', // Semi-transparent overlay
        borderRadius: '15px 0 0 15px' // Match the border radius of the card
    };

    return (
        <MDBContainer className='my-5 d-flex justify-content-center align-items-center' style={{ minHeight: '100vh' }}>
            <MDBCard style={cardStyle}>
                <MDBRow className='g-0'>
                    <MDBCol md='6' className='position-relative'>
                        <MDBCardImage src='/images/login_imagev2.png' alt='Custom Image' fluid style={{ borderRadius: '15px 0 0 15px' }} />
                        <div style={overlayStyle}></div> {/* Overlay to reduce contrast */}
                    </MDBCol>

                    <MDBCol md='6'>
                        <TypeAnimation
                            sequence={[
                                'Test your data using \
                                Approximate Entropy',
                                1000,
                                'Test your data using \
                                Block Frequency',
                                1000,
                                'Test your data using \
                                Cumulative Sums',
                                1000,
                                'Test your data using \
                                DFT',
                                1000,
                                'Test your data using \
                                Frequency',
                                1000,
                                'Test your data using \
                                Linear Complexity',
                                1000,
                                'Test your data using \
                                Longest Run',
                                1000,
                                'Test your data using       \
                                Non Overlapping Template',
                                1000,
                                'Test your data using \
                                Random Excursions',
                                1000,
                            ]}
                            wrapper="span"
                            speed={50}
                            style={{ fontSize: '2em', display: 'inline-block', marginTop: '80px'}}
                            repeat={Infinity}
                        />
                        <MDBCardBody style={formContainerStyle}>
                            <h2 className="text-white mb-4">Login</h2> {/* Header */}
                            <form onSubmit={handleLogin}>
                                <MDBInput 
                                    wrapperClass='mb-4' 
                                    labelClass='text-white' // White label text
                                    label='Email/Username' 
                                    id='form1' 
                                    type='text'
                                    value={token}
                                    onChange={(e) => setToken(e.target.value)}
                                />
                                <MDBInput 
                                    wrapperClass='mb-4' 
                                    labelClass='text-white' // White label text
                                    label='Password' 
                                    id='form2' 
                                    type='password'
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                                <MDBBtn type="submit" style={buttonStyle} className="mb-4 w-100">Sign in</MDBBtn>
                                <p className="text-center mt-5 mb-0">
                                    Do not have account yet? <a href="#!" onClick={() => navigate('/register')} className="login-link"><u>Sign-up here</u></a>
                                </p>
                            </form>
                        </MDBCardBody>
                    </MDBCol>
                </MDBRow>
            </MDBCard>
        </MDBContainer>
    );
};

export default LoginForm;