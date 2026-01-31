import "../styles/landing.css";

export default function Landing({ setPage }) {
  return (
    <div className="container">
      <div className="hero-section">
        <h1 className="hero-title">
          Discover Government Scholarships{" "}
          <span className="hero-highlight">
            You Are Eligible For
          </span>
        </h1>
        <p className="hero-subtitle">
          FundMyStudy helps Indian students from rural areas find verified government scholarships
          using secure authentication and intelligent eligibility matching.
        </p>

        <div className="hero-cta">
          <button
            onClick={() => setPage('signup')}
            className="primary-cta"
          >
            Get Started for Free →
          </button>
          <button
            onClick={() => {
              const element = document.querySelector('.how-it-works');
              if (element) element.scrollIntoView({ behavior: 'smooth' });
            }}
            className="secondary-cta"
          >
            Learn More
          </button>
        </div>
      </div>

      <div className="features-grid">
        <div className="card">
          <h3>📋 Create Profile</h3>
          <p>Fill in your academic and personal details once. We keep your data secure and private.</p>
        </div>
        <div className="card">
          <h3>🤖 Smart Matching</h3>
          <p>Our system automatically checks your eligibility against all government scholarship criteria.</p>
        </div>
        <div className="card">
          <h3>🚀 Direct Application</h3>
          <p>Apply directly on official government portals with guided assistance.</p>
        </div>
      </div>

      <div className="how-it-works">
        <h2 className="section-title">How It Works</h2>
        <div className="steps-container">
          <div className="step-item">
            <div className="step-badge">1</div>
            <h3>Create Profile</h3>
            <p>Sign up and enter your academic details, income, category, and other required information.</p>
          </div>

          <div className="step-item">
            <div className="step-badge step-badge-2">2</div>
            <h3>Automatic Eligibility Check</h3>
            <p>Our system matches your profile with all government scholarship criteria in real-time.</p>
          </div>

          <div className="step-item">
            <div className="step-badge step-badge-3">3</div>
            <h3>Apply & Track</h3>
            <p>Get direct links to apply and receive deadline reminders for your eligible scholarships.</p>
          </div>
        </div>
      </div>

      <div className="why-us">
        <h2 className="section-title">Why Choose FundMyStudy?</h2>
        <div className="card">
          <ul>
            <li><strong>Government & Verified Sources Only</strong> - No private or fake scholarships</li>
            <li><strong>Transparent Eligibility Logic</strong> - Understand exactly why you qualify</li>
            <li><strong>Secure & Private</strong> - Your data is encrypted and never shared</li>
            <li><strong>Made for Rural Students</strong> - Simple interface, works on low-bandwidth</li>
            <li><strong>Completely Free</strong> - No hidden charges, no commission</li>
            <li><strong>Regional Language Support</strong> - Available in multiple Indian languages</li>
          </ul>
        </div>
      </div>
    </div>
  );
}