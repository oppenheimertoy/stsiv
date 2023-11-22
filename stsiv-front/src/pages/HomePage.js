import React from 'react';

const HomePage = () => {
    return (
        <div>
            <h1>NIST Statistical Test Suite</h1>
            <p>This project is a considerably improved version of the NIST Statistical Test Suite (STS), a collection of tests used in the evaluation of the randomness of bitstreams of data.</p>
            
            <h2>Purpose</h2>
            <p>STS can be useful in:</p>
            <ul>
                <li>Evaluating the randomness of bitstreams produced by hardware and software key generators for cryptographic applications.</li>
                <li>Evaluating the quality of pseudo random number generators used in simulation and modeling applications.</li>
            </ul>

            <h2>License</h2>
            <p>The original software was developed at the National Institute of Standards and Technology by employees of the Federal Government in the course of their official duties. Pursuant to title 17 Section 105 of the United States Code this software is not subject to copyright protection and is in the public domain. Furthermore, Cisco's contribution is also placed in the public domain. The NIST Statistical Test Suite is an experimental system. Neither NIST nor Cisco assume any responsibility whatsoever for its use by other parties, and makes no guarantees, expressed or implied, about its quality, reliability, or any other characteristic. We would appreciate acknowledgment if the software is used.</p>
        </div>
    );
};

export default HomePage;