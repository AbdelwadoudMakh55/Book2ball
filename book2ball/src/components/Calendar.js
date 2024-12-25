import React, { useState } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const localizer = momentLocalizer(moment);

const CalendarComponent = ({ pitchId }) => {
  const [events, setEvents] = useState([]);
  const { user, getToken } = useAuth();

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
            start_time: moment(start).format('YYYY-MM-DD HH:mm:ss')
          },
        );
        setEvents([...events, { start, end, title: 'Booked' }]);
        console.log(response)
        alert('Reservation successful');
      } catch (error) {
        console.error('Error creating reservation:', error);
        alert('Failed to create reservation');
      }
    } else {
      alert('This time slot is already booked.');
    }
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
      />
    </div>
  );
};

export default CalendarComponent;