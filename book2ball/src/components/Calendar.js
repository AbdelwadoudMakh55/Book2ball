import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const localizer = momentLocalizer(moment);

const CalendarComponent = ({ pitchId }) => {
  const [events, setEvents] = useState([]);
  const { user, getToken } = useAuth();

  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const token = getToken();
        const config = {
          headers: { Authorization: `Bearer ${token}` }
        };
        const response = await axios.get(
          `https://book2ball.azurewebsites.net/api/reservations/${pitchId}`,
          config
        );
        const today = moment().startOf('day');
        const reservations = response.data
          .filter(reservation => moment(reservation.start_time).isSameOrAfter(today))
          .map(reservation => ({
            start: new Date(reservation.start_time),
            end: new Date(reservation.end_time),
            title: 'Booked',
            status: reservation.status // Assuming the reservation has a status field
          }));
        setEvents(reservations);
      } catch (error) {
        console.error('Error fetching reservations:', error);
      }
    };

    fetchReservations();
  }, [pitchId, getToken]);

  const handleSelectSlot = async ({ start, end }) => {
    const isBooked = events.some(event => 
      (start >= event.start && start < event.end) || 
      (end > event.start && end <= event.end)
    );

    if (!isBooked) {
      try {
        const token = getToken();
        const config = {
          headers: { Authorization: `Bearer ${token}` }
        };
        const response = await axios.post(
          `https://book2ball.azurewebsites.net/api/reservations/${pitchId}`,
          {
            user_id: user.uid,
            start_time: moment(start).format('YYYY-MM-DD HH:mm:ss'),
            end_time: moment(end).format('YYYY-MM-DD HH:mm:ss')
          },
          config
        );
        setEvents([...events, { start, end, title: 'Booked', status: 'confirmed' }]);
        alert('Reservation successful');
      } catch (error) {
        console.error('Error creating reservation:', error);
        alert('Failed to create reservation');
      }
    } else {
      alert('This time slot is already booked.');
    }
  };

  const eventStyleGetter = (event) => {
    let backgroundColor = '#3174ad'; // Default color
    if (event.status === 'confirmed') {
      backgroundColor = '#27ae60'; // Green for confirmed
    } else if (event.status === 'pending') {
      backgroundColor = '#f39c12'; // Yellow for pending
    } else if (event.status === 'cancelled') {
      backgroundColor = '#e74c3c'; // Red for cancelled
    }
    const style = {
      backgroundColor,
      borderRadius: '0px',
      opacity: 0.8,
      color: 'white',
      border: '0px',
      display: 'block'
    };
    return {
      style
    };
  };

  return (
    <div style={{ height: '400px' }}>
      <Calendar
        localizer={localizer}
        events={events}
        defaultView="day"
        views={['day']}
        step={60}
        timeslots={1}
        min={new Date(1970, 1, 1, 7, 0, 0)}
        max={new Date(1970, 1, 1, 23, 59, 59)}
        selectable
        onSelectSlot={handleSelectSlot}
        eventPropGetter={eventStyleGetter}
        validRange={{
          start: new Date(),
          end: new Date(9999, 11, 31)
        }}
      />
    </div>
  );
};

export default CalendarComponent;