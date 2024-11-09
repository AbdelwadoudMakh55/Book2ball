import './Testimonials.css';

function Testimonials() {
  const testimonials = [
    {
      id: 1,
      name: 'John Doe',
      text: 'Book2Ball made it so easy to find and book a football pitch. Highly recommended!',
    },
    {
      id: 2,
      name: 'Jane Smith',
      text: 'Great platform with a variety of pitches to choose from. The booking process was seamless.',
    },
    {
      id: 3,
      name: 'Mike Johnson',
      text: 'I love using Book2Ball for our weekly football games. The interface is user-friendly and efficient.',
    },
  ];

  return (
    <section className="testimonials" id="testimonials">
      <h2>What Our Users Say</h2>
      <div className="testimonials-grid">
        {testimonials.map((testimonial) => (
          <div className="testimonial-card" key={testimonial.id}>
            <p className="testimonial-text">"{testimonial.text}"</p>
            <p className="testimonial-name">- {testimonial.name}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Testimonials;