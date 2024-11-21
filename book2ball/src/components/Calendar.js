import React, { useState } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const localizer = momentLocalizer(moment);

const CalendarComponent = () => {
  const [events, setEvents] = useState([]);

  const handleSelectSlot = ({ start, end }) => {
    const isBooked = events.some(event => 
      (start >= event.start && start < event.end) || 
      (end > event.start && end <= event.end)
    );

    if (!isBooked) {
      // Handle booking logic here
      console.log('Selected slot:', start, end);
      setEvents([...events, { start, end, title: 'Booked' }]);
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