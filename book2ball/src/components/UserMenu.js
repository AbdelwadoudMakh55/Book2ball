import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { FaUserCircle } from 'react-icons/fa';
import './userMenu.css';

function UserMenu() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const menuRef = useRef(null);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const handleClickOutside = (event) => {
    if (menuRef.current && !menuRef.current.contains(event.target)) {
      setDropdownOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="user-menu" ref={menuRef}>
      <FaUserCircle className="user-icon" onClick={toggleDropdown} />
      {dropdownOpen && (
        <div className="dropdown-menu">
          <div className="dropdown-header">
            <FaUserCircle className="dropdown-icon" />
            <span className="dropdown-email">{user?.email}</span>
          </div>
          <button onClick={handleLogout} className="dropdown-item">Logout</button>
          <button onClick={() => navigate('/reservations')} className="dropdown-item">Reservations</button>
        </div>
      )}
    </div>
  );
}

export default UserMenu;