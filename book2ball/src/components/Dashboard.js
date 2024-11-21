import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';
import './dashboard.css';

const Dashboard = () => {
  const [pitches, setPitches] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const pitchesPerPage = 5;
  const { user, getToken } = useAuth();
  const userId = user.uid;
  const cityIdRef = useRef(0);
  const cityName = useRef('');

  useEffect(() => {
    const fetchPitches = async () => {
      try {
        const token = getToken(); // Retrieve the JWT
        const config = {
          headers: { Authorization: `Bearer ${token}` }
        };

        const userResponse = await axios.get(`https://book2ball.azurewebsites.net/api/users/${userId}`, config);
        cityIdRef.current = userResponse.data.city_id;

        const cityResponse = await axios.get(`https://book2ball.azurewebsites.net/api/cities/${cityIdRef.current}`, config);
        cityName.current = cityResponse.data.name;

        const pitchesResponse = await axios.get(`https://book2ball.azurewebsites.net/api/cities/${cityIdRef.current}/pitches`, config);
        console.log(pitchesResponse.data);
        setPitches(pitchesResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchPitches();
  }, [userId, getToken]);

  // Pagination logic
  const indexOfLastPitch = currentPage * pitchesPerPage;
  const indexOfFirstPitch = indexOfLastPitch - pitchesPerPage;
  const currentPitches = pitches.slice(indexOfFirstPitch, indexOfLastPitch);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="dashboard">
      <h2>Pitches in {cityName.current}</h2>
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
        {[...Array(Math.ceil(pitches.length / pitchesPerPage)).keys()].map(number => (
          <button key={number + 1} onClick={() => paginate(number + 1)}>
            {number + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;