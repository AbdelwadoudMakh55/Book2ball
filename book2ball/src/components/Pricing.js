import './pricing.css';

function Pricing() {
  const pricingPlans = [
    {
      id: 1,
      title: 'Basic Plan',
      price: '$20/hour',
      features: ['1 Pitch', 'Up to 10 Players', 'Basic Amenities'],
    },
    {
      id: 2,
      title: 'Standard Plan',
      price: '$35/hour',
      features: ['2 Pitches', 'Up to 20 Players', 'Standard Amenities'],
    },
    {
      id: 3,
      title: 'Premium Plan',
      price: '$50/hour',
      features: ['3 Pitches', 'Up to 30 Players', 'Premium Amenities'],
    },
  ];

  return (
    <section className="pricing" id="pricing">
      <h2>Pricing Plans</h2>
      <div className="pricing-grid">
        {pricingPlans.map((plan) => (
          <div className="pricing-card" key={plan.id}>
            <h3>{plan.title}</h3>
            <p className="price">{plan.price}</p>
            <ul className="features-list">
              {plan.features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Pricing;