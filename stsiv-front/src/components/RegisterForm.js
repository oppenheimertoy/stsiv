import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import {
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBBtn,
  MDBCheckbox,
  MDBIcon
} from 'mdb-react-ui-kit';

const SignUpForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const navigate = useNavigate();

  const handleSignUp = async (e) => {
    e.preventDefault();
    // Sign-up logic here
  };

  // Replace this with the path to your actual background image
  // const backgroundStyle = {
  //   backgroundImage: "url('/path-to-your-background-image.jpg')",
  //   backgroundSize: 'cover',
  //   backgroundRepeat: 'no-repeat',
  //   backgroundPosition: 'center center'
  // };

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
              <MDBInput label='Your Username' id='form3Example1cg' type='text' onChange={(e) => setName(e.target.value)} />
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