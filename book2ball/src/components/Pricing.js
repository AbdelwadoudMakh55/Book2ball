import './pricing.css';

function Pricing() {
  const pricingPlans = [
    {
      id: 1,
      title: '5vs5/6vs6 Pitch',
      price: 'From 200 MAD/hour',
      features: ['Up to 12 Players'],
    },
    {
      id: 2,
      title: '7vs7/8vs8 Pitch',
      price: 'From 300 MAD/hour',
      features: ['Up to 16 Players'],
    },
    {
      id: 3,
      title: '11vs11 Pitch',
      price: 'From 1100 MAD/hour',
      features: ['Up to 22 Players'],
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