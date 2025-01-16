import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import './userReservations.css';
import moment from 'moment';

const UserReservations = () => {
  const [reservations, setReservations] = useState([]);
  const [nextReservation, setNextReservation] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [reservationsPerPage] = useState(5);
  const [pitchNames, setPitchNames] = useState({});
  const { user, getToken } = useAuth();

  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const token = await getToken();
        const config = {
          headers: { Authorization: `Bearer ${token}` }
        };
        const response = await axios.get(`https://book2ball.azurewebsites.net/api/users/${user.uid}/reservations`, config);
        const sortedReservations = response.data.sort((a, b) => new Date(a.start_time) - new Date(b.start_time));
        const upcomingReservation = sortedReservations.find(reservation => new Date(reservation.start_time) > new Date());
        setNextReservation(upcomingReservation);
        setReservations(sortedReservations.filter(reservation => reservation !== upcomingReservation));

        // Fetch pitch names
        const pitchIds = sortedReservations.map(reservation => reservation.pitch_id);
        const uniquePitchIds = [...new Set(pitchIds)];
        const pitchNamesResponse = await Promise.all(uniquePitchIds.map(async (pitchId) => {
          const pitchResponse = await axios.get(`https://book2ball.azurewebsites.net/api/pitches/${pitchId}`, config);
          return { pitchId, name: pitchResponse.data.name };
        }));
        const pitchNamesMap = pitchNamesResponse.reduce((acc, { pitchId, name }) => {
          acc[pitchId] = name;
          return acc;
        }, {});
        setPitchNames(pitchNamesMap);
      } catch (error) {
        console.error('Error fetching reservations or pitch names:', error);
      }
    };

    fetchReservations();
  }, [user.uid, getToken]);

  const indexOfLastReservation = currentPage * reservationsPerPage;
  const indexOfFirstReservation = indexOfLastReservation - reservationsPerPage;
  const currentReservations = reservations.slice(indexOfFirstReservation, indexOfLastReservation);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const renderCountdown = (startTime) => {
    const now = moment();
    const start = moment(startTime);
    const duration = moment.duration(start.diff(now));
    return `${duration.days()}d ${duration.hours()}h ${duration.minutes()}m ${duration.seconds()}s`;
  };

  return (
    <div className="user-reservations-container">
      <div className="next-reservation">
        <h2>Next Reservation</h2>
        {nextReservation ? (
          <>
            <p><span className="label">Pitch:</span> <span className="value">{pitchNames[nextReservation.pitch_id]}</span></p>
            <p><span className="label">Time:</span> <span className="value">{moment(nextReservation.start_time).format('MMMM Do YYYY, h:mm:ss a')}</span></p>
            <p><span className="label">Countdown:</span> <span className="value">{renderCountdown(nextReservation.start_time)}</span></p>
          </>
        ) : (
          <p>You have no upcoming reservations.</p>
        )}
      </div>
      <div className="previous-reservations">
        <h2>Previous Reservations</h2>
        {currentReservations.length > 0 ? (
          currentReservations.map(reservation => (
            <div key={reservation.id} className="reservation">
              <p><span className="label">Pitch:</span> <span className="value">{pitchNames[reservation.pitch_id]}</span></p>
              <p><span className="label">Time:</span> <span className="value">{moment(reservation.start_time).format('MMMM Do YYYY, h:mm:ss a')}</span></p>
            </div>
          ))
        ) : (
          <p>You have no previous reservations.</p>
        )}
        <div className="pagination">
          {Array.from({ length: Math.ceil(reservations.length / reservationsPerPage) }, (_, index) => (
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
    </div>
  );
};

export default UserReservations;