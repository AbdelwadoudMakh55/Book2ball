import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import MapComponent from './MapComponent';
import CalendarComponent from './Calendar';
import { useAuth } from '../contexts/AuthContext';
import './pitchDetail.css';

const PitchDetail = () => {
  const { pitchId } = useParams();
  const [pitch, setPitch] = useState(null);
  const { user, getToken } = useAuth();
  const userId = user.uid;

  useEffect(() => {
    const config = {
      headers: { Authorization: `Bearer ${getToken()}` }
    };
    const fetchPitch = async () => {
      try {
        const response = await axios.get(`https://book2ball.azurewebsites.net/api/pitches/${pitchId}`, config);
        setPitch(response.data);
      } catch (error) {
        console.error('Error fetching pitch:', error);
      }
    };

    fetchPitch();
  }, [pitchId]);

  if (!pitch) {
    return <div>Loading...</div>;
  }

  // TODO: Replace location in database with latitude and longitude
  const latitude = 33.4870476;
  const longitude = -7.5779506;

  return (
    <div className="pitch-detail-container">
      <div className="pitch-detail">
        <h2>{pitch.name}</h2>
        <img src="/Terrain_6vs6_arena.jpg" alt={pitch.name} />
        <p><span className="label">Capacity:</span> <span className="value">{pitch.capacity}</span></p>
        <p><span className="label">Price:</span> <span className="value">{pitch.price} MAD</span></p>
        {/* Add more details as needed */}
      </div>
      <div className="map-container">
        <h2 className="map-title">Location</h2>
        <MapComponent latitude={latitude} longitude={longitude} />
      </div>
      <div className="calendar-container">
        <h2 className="calendar-title">Book a Time Slot</h2>
        <CalendarComponent pitchId={pitchId} />
      </div>
    </div>
  );
};

export default PitchDetail;