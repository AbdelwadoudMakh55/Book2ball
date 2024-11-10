import './Contact.css';

function Contact() {
  return (
    <section className="contact" id="contact">
      <h2>Contact Us</h2>
      <div className="contact-info">
        <p>Address: Route El Jadida Km 8, BP : 7731, Quartier Laymoune, Casablanca</p>
        <p>Phone: (+212) 656075038</p>
        <p>Email: abdelwadoudmakhlok@gmail.com</p>
      </div>
      <form className="contact-form">
        <label htmlFor="name">Name</label>
        <input type="text" id="name" name="name" required />

        <label htmlFor="email">Email</label>
        <input type="email" id="email" name="email" required />

        <label htmlFor="message">Message</label>
        <textarea id="message" name="message" rows="4" required></textarea>

        <div className="button-container">
          <button type="submit">Send Message</button>
        </div>
      </form>
    </section>
  );
}

export default Contact;