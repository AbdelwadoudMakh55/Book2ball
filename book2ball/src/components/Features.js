import './features.css';

function Features() {
  const features = [
    {
      id: 1,
      title: 'Easy Booking',
      description: 'Book your football pitch in just a few clicks.',
      icon: 'fas fa-calendar-check',
    },
    {
      id: 2,
      title: 'Variety of Pitches',
      description: 'Choose from a wide range of football pitches.',
      icon: 'fas fa-futbol',
    },
    {
      id: 3,
      title: 'User-Friendly Interface',
      description: 'Enjoy a seamless and intuitive booking experience.',
      icon: 'fas fa-laptop',
    },
  ];

  return (
    <section className="features" id="features">
      <h2>Our Features</h2>
      <div className="features-grid">
        {features.map((feature) => (
          <div className="feature-card" key={feature.id}>
            <i className={feature.icon}></i>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Features;