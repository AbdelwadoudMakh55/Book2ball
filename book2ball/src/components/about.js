import './about.css';

function About() {
  return (
    <section className="about" id="about">
      <div className="about-text">
        <h2>About Us</h2>
        <p>
          Welcome to Book2Ball! Our mission is to make it easy for you to find and book the best football pitches in your area. Whether you're looking for a casual game with friends or a competitive match, we've got you covered. Our platform offers a wide range of pitches to suit all your needs. Join us and be part of the growing community of football enthusiasts!
        </p>
      </div>
      <img src="/book2ball_hd.png" alt="Book2Ball Logo" className="about-logo" />
    </section>
  );
}

export default About;