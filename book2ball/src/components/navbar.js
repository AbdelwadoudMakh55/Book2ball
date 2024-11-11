import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import UserMenu from './UserMenu';
import './navbar.css';

function Navbar() {
  const { user } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">
          <img src="/book2ball_hd.png" alt="Book2Ball Logo" className="logo" />
        </Link>
        <Link to="/" className="navbar-title">
          <h1>Book2Ball</h1>
        </Link>
      </div>
            
      <ul className="navbar-links">
        <li><Link to="/">Home</Link></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#fields">Fields</a></li>
        <li><a href="#reservations">Reservations</a></li>
        <li><a href="#pricing">Pricing</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
        {user ? (
          <UserMenu />
        ) : (
          <li><Link to="/login" className="login-btn">Login</Link></li>
        )}
      </ul>
      
      <div className="menu-icon">
        <span className="menu-bar"></span>
        <span className="menu-bar"></span>
        <span className="menu-bar"></span>
      </div>
    </nav>
  );
}

export default Navbar;