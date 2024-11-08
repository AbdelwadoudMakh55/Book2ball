import './navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <img src="/book2ball_hd.png" alt="Book2Ball Logo" className="logo" />
        <h1>Book2Ball</h1>
      </div>
            
      <ul className="navbar-links">
        <li><a href="#home">Home</a></li>
        <li><a href="#fields">Fields</a></li>
        <li><a href="#reservations">Reservations</a></li>
        <li><a href="#pricing">Pricing</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
        <li><button className="login-btn">Login</button></li>
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