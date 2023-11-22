import React, { useState, useEffect } from 'react';
import axios from '../api/axios';

const ExperimentsPage = () => {
    const [experiments, setExperiments] = useState([]);

    useEffect(() => {
        const fetchExperiments = async () => {
            try {
                const response = await axios.get('/experiment/list');
                setExperiments(response.data);
            } catch (error) {
                console.error('Error fetching experiments', error);
            }
        };

        fetchExperiments();
    }, []);

    return (
        <div>
            <h1>Your Experiments</h1>
            <ul>
                {experiments.map(exp => (
                    <li key={exp.id}>{exp.name} - {exp.description}</li>
                ))}
            </ul>
        </div>
    );
};

export default ExperimentsPage;