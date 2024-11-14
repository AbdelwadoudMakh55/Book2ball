import { Link, useLocation } from 'react-router-dom';
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
        <li>
          {useLocation().pathname === "/" ? (
            <a href="#features">Features</a>
          ) : (
            <Link to="/#features">Features</Link>
          )}
        </li>
        <li>
          {user ? (
            <Link to="/dashboard">Fields</Link>
          ) : (
            <Link to="/login">Fields</Link>
          )}
        </li>
        <li>
          {user ? (
            <Link to="/reservations">Reservations</Link>
          ) : (
            <Link to="/login">Reservations</Link>
          )}
        </li>
        <li>
        {useLocation().pathname === "/" ? (
            <a href="#pricing">Pricing</a>
          ) : (
            <Link to="/#pricing">Pricing</Link>
          )}
        </li>
        <li>
          {useLocation().pathname === "/" ? (
            <a href="#about">About</a>
          ) : (
            <Link to="/#about">About</Link>
          )}
        </li>
        <li>
          {useLocation().pathname === "/" ? (
            <a href="#contact">Contact</a>
          ) : (
            <Link to="/#contact">Contact</Link>
          )}
        </li>
          {user ? (
            <UserMenu />
          ) : (
            <Link to="/login" className="login-btn">Login</Link>
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