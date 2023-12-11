import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/axios'; // Import your API client

import {
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBBtn
} from 'mdb-react-ui-kit';

const SignUpForm = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const navigate = useNavigate();

  const handleSignUp = async (e) => {
    e.preventDefault();
    if (password !== repeatPassword) {
      alert("Passwords do not match");
      return;
    }

    try {
      await apiClient.post('/user/sign-up', {
        username,
        email,
        password1: password,
        password2: repeatPassword,
        name: username, // Assuming username as name for simplicity
        surname: "" // If you have a surname field, you should use it here
      });

      // Redirect to login page after successful registration
      navigate('/login');
    } catch (error) {
      console.error('Registration error:', error);
      // Handle errors (e.g., show error message)
    }
  };

  const cardStyle = {
    backgroundColor: '#2A2A2A', // Dark background color for the card
    color: '#fff', // White text color
    borderRadius: '15px' // Rounded corners for the card
  };

  const buttonStyle = {
    backgroundColor: '#3c5920', // Green background for the button
    borderColor: '#4CAF50',
    color: '#fff' // White text color for the button
};

  return (
    <MDBContainer className='my-5 d-flex justify-content-center align-items-center' style={{ minHeight: '100vh' }}>
      <MDBCard style={cardStyle}>
        <MDBCardBody className="p-5">
          <h2 className="text-uppercase text-center mb-5">Create an account</h2>
          <form onSubmit={handleSignUp}>

            {/* Name Input */}
            <div className="form-outline mb-4">
              <MDBInput label='Your Username' id='form3Example1cg' type='text' onChange={(e) => setUsername(e.target.value)} />
            </div>

            {/* Email Input */}
            <div className="form-outline mb-4">
              <MDBInput label='Your Email' id='form3Example3cg' type='email' onChange={(e) => setEmail(e.target.value)} />
            </div>

            {/* Password Input */}
            <div className="form-outline mb-4">
              <MDBInput label='Password' id='form3Example4cg' type='password' onChange={(e) => setPassword(e.target.value)} />
            </div>

            {/* Repeat Password Input */}
            <div className="form-outline mb-4">
              <MDBInput label='Repeat your password' id='form3Example4cdg' type='password' onChange={(e) => setRepeatPassword(e.target.value)} />
            </div>

            {/* Register Button */}
            <MDBBtn type="submit" style={buttonStyle} className="btn-block btn-lg">Register</MDBBtn>

            <p className="text-center mt-5 mb-0">
                Have already an account? <a href="#!" onClick={() => navigate('/login')} className="login-link"><u>Login here</u></a>
            </p>

          </form>
        </MDBCardBody>
      </MDBCard>
    </MDBContainer>
  );
};

export default SignUpForm;