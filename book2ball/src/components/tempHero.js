import { Link } from 'react-router-dom';
import './hero.css';

function Hero() {
  return (
    <section className="hero">
      <h1>Welcome To Book2Ball</h1>
      <p>Reserve your Field, Play your Game</p>
      <Link to="/signup" className="ctaButton">Get Started</Link>
    </section>
  );
}

export default Hero;