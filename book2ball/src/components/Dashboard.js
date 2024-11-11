import { useState, useEffect } from 'react';
import './dashboard.css';

const fakePitches = [
  { id: 1, name: 'Pitch 1', location: 'Location 1' },
  { id: 2, name: 'Pitch 2', location: 'Location 2' },
  { id: 3, name: 'Pitch 3', location: 'Location 3' },
  { id: 4, name: 'Pitch 4', location: 'Location 4' },
  { id: 5, name: 'Pitch 5', location: 'Location 5' },
  { id: 6, name: 'Pitch 6', location: 'Location 6' },
  { id: 7, name: 'Pitch 7', location: 'Location 7' },
  { id: 8, name: 'Pitch 8', location: 'Location 8' },
  { id: 9, name: 'Pitch 9', location: 'Location 9' },
  { id: 10, name: 'Pitch 10', location: 'Location 10' },
  { id: 11, name: 'Pitch 11', location: 'Location 11' },
];

function Dashboard() {
  const [pitches, setPitches] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const pitchesPerPage = 10;

  useEffect(() => {
    // Directly set the fake data to the pitches state
    setPitches(fakePitches);
  }, []);

  // Pagination logic
  const indexOfLastPitch = currentPage * pitchesPerPage;
  const indexOfFirstPitch = indexOfLastPitch - pitchesPerPage;
  const currentPitches = pitches.slice(indexOfFirstPitch, indexOfLastPitch);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="dashboard">
      <h2>Pitches</h2>
      <div className="pitches">
        {currentPitches.map(pitch => (
          <div key={pitch.id} className="pitch">
            <h3>{pitch.name}</h3>
            <p>{pitch.location}</p>
          </div>
        ))}
      </div>
      <div className="pagination">
        {Array.from({ length: Math.ceil(pitches.length / pitchesPerPage) }, (_, i) => (
          <button key={i + 1} onClick={() => paginate(i + 1)} className={currentPage === i + 1 ? 'active' : ''}>
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;