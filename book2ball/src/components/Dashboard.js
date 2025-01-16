import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';
import './dashboard.css';

const Dashboard = () => {
  const [pitches, setPitches] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pitchesPerPage, setPitchesPerPage] = useState(5);
  const { user, getToken } = useAuth();
  const userId = user ? user.uid : null;

  useEffect(() => {
    const fetchPitchesByLocation = async (latitude, longitude) => {
      try {
        const token = await getToken(); // Get the token from AuthContext
        if (!token) {
          console.error('No token available');
          return;
        }
        const config = {
          headers: { Authorization: `Bearer ${token}` }
        };
        const response = await axios.get(`https://book2ball.azurewebsites.net/api/pitches?lat=${latitude}&long=${longitude}`, config);
        console.log('Response:', response);
        setPitches(response.data); // Update state with retrieved pitches
      } catch (error) {
        console.error('Error fetching pitches:', error);
        if (error.response) {
          console.error('Response data:', error.response.data);
          console.error('Response status:', error.response.status);
          console.error('Response headers:', error.response.headers);
        }
      }
    };

    const getUserLocation = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            fetchPitchesByLocation(latitude, longitude);
          },
          (error) => {
            console.error('Error getting user location:', error);
          }
        );
      } else {
        console.error('Geolocation is not supported by this browser.');
      }
    };

    getUserLocation();
  }, [getToken]);

  useEffect(() => {
    const updatePitchesPerPage = () => {
      const width = window.innerWidth;
      if (width >= 1200) {
        setPitchesPerPage(10);
      } else if (width >= 992) {
        setPitchesPerPage(8);
      } else if (width >= 768) {
        setPitchesPerPage(6);
      } else {
        setPitchesPerPage(4);
      }
    };

    updatePitchesPerPage();
    window.addEventListener('resize', updatePitchesPerPage);

    return () => window.removeEventListener('resize', updatePitchesPerPage);
  }, []);

  // Pagination logic
  const indexOfLastPitch = currentPage * pitchesPerPage;
  const indexOfFirstPitch = indexOfLastPitch - pitchesPerPage;
  const currentPitches = pitches.slice(indexOfFirstPitch, indexOfLastPitch);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="dashboard">
      <h2>Pitches near you</h2>
      <div className="pitches">
        {currentPitches.map(pitch => (
          <Link to={`/pitch/${pitch.id}`} key={pitch.id} className="pitch-link">
            <div className="pitch">
              <h3>{pitch.name}</h3>
              <img src="Terrain_6vs6_arena.jpg" alt={pitch.name} />
              <p><span className="label">Capacity:</span> <span className="value">{pitch.capacity}</span></p>
              <p><span className="label">Price:</span> <span className="value">{pitch.price} MAD</span></p>
            </div>
          </Link>
        ))}
      </div>
      <div className="pagination">
        {Array.from({ length: Math.ceil(pitches.length / pitchesPerPage) }, (_, index) => (
          <button
            key={index + 1}
            onClick={() => paginate(index + 1)}
            disabled={currentPage === index + 1}
          >
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;