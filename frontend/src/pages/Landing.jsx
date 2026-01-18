export default function Landing() {
  return (
    <div className="container">
      <div className="hero-section" style={{ textAlign: 'center', marginBottom: '4rem' }}>
        <h1 style={{ fontSize: '4rem', lineHeight: '1.1' }}>
          Discover Government Scholarships 
          <span style={{ display: 'block', fontSize: '3rem', color: '#4f46e5' }}>
            You Are Eligible For
          </span>
        </h1>
        <p style={{ fontSize: '1.25rem', maxWidth: '800px', margin: '2rem auto' }}>
          FundMyStudy helps Indian students from rural areas find verified government scholarships
          using secure authentication and intelligent eligibility matching.
        </p>
        
        <div style={{ 
          display: 'flex', 
          gap: '1rem', 
          justifyContent: 'center',
          marginTop: '3rem'
        }}>
          <button style={{ padding: '1rem 3rem', fontSize: '1.1rem' }}>
            Get Started for Free →
          </button>
          <button style={{ 
            background: 'white', 
            color: '#4f46e5',
            border: '2px solid #4f46e5'
          }}>
            Learn More
          </button>
        </div>
      </div>

      <div className="features-grid" style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '2rem',
        margin: '4rem 0'
      }}>
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
        <h2 style={{ textAlign: 'center', marginBottom: '3rem' }}>How It Works</h2>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '2rem'
        }}>
          <div style={{ flex: 1, minWidth: '250px' }}>
            <div style={{
              background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
              color: 'white',
              width: '50px',
              height: '50px',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
              fontWeight: 'bold',
              marginBottom: '1rem'
            }}>1</div>
            <h3>Create Profile</h3>
            <p>Sign up and enter your academic details, income, category, and other required information.</p>
          </div>
          
          <div style={{ flex: 1, minWidth: '250px' }}>
            <div style={{
              background: 'linear-gradient(135deg, #7c3aed, #a855f7)',
              color: 'white',
              width: '50px',
              height: '50px',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
              fontWeight: 'bold',
              marginBottom: '1rem'
            }}>2</div>
            <h3>Automatic Eligibility Check</h3>
            <p>Our system matches your profile with all government scholarship criteria in real-time.</p>
          </div>
          
          <div style={{ flex: 1, minWidth: '250px' }}>
            <div style={{
              background: 'linear-gradient(135deg, #a855f7, #d946ef)',
              color: 'white',
              width: '50px',
              height: '50px',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
              fontWeight: 'bold',
              marginBottom: '1rem'
            }}>3</div>
            <h3>Apply & Track</h3>
            <p>Get direct links to apply and receive deadline reminders for your eligible scholarships.</p>
          </div>
        </div>
      </div>

      <div className="why-us" style={{ marginTop: '4rem' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Why Choose FundMyStudy?</h2>
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