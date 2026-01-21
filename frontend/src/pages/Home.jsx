export default function Home() {
  return (
    <div className="container">
      <div style={{
        background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
        borderRadius: '24px',
        padding: '4rem 2rem',
        textAlign: 'center',
        color: 'white',
        marginBottom: '3rem',
        boxShadow: '0 20px 40px rgba(79, 70, 229, 0.3)'
      }}>
        <h1 style={{ color: 'white', fontSize: '3.5rem', marginBottom: '1rem' }}>
          Welcome to FundMyStudy
        </h1>
        <p style={{ 
          fontSize: '1.25rem', 
          opacity: 0.9,
          maxWidth: '800px',
          margin: '0 auto 2rem'
        }}>
          FundMyStudy helps Indian students discover scholarships
          they are eligible for using verified data and intelligent eligibility matching.
        </p>
        <button style={{ 
          background: 'white', 
          color: '#4f46e5',
          fontSize: '1.1rem',
          padding: '1rem 2.5rem'
        }}>
          Start Your Journey →
        </button>
      </div>

      <div className="card" style={{ textAlign: 'center' }}>
        <h2>Why Trust FundMyStudy?</h2>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '2rem',
          marginTop: '2rem'
        }}>
          <div style={{ padding: '1.5rem' }}>
            <div style={{
              fontSize: '2.5rem',
              marginBottom: '1rem',
              color: '#4f46e5'
            }}>🔒</div>
            <h3>Government Only</h3>
            <p>Verified government scholarships, no private or fake listings</p>
          </div>
          
          <div style={{ padding: '1.5rem' }}>
            <div style={{
              fontSize: '2.5rem',
              marginBottom: '1rem',
              color: '#4f46e5'
            }}>🤖</div>
            <h3>Smart Matching</h3>
            <p>AI-powered eligibility checking based on your profile</p>
          </div>
          
          <div style={{ padding: '1.5rem' }}>
            <div style={{
              fontSize: '2.5rem',
              marginBottom: '1rem',
              color: '#4f46e5'
            }}>🎯</div>
            <h3>Personalized</h3>
            <p>Scholarships matched specifically to your background and needs</p>
          </div>
        </div>
      </div>

      <div style={{
        marginTop: '4rem',
        padding: '3rem',
        background: 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
        borderRadius: '20px',
        textAlign: 'center'
      }}>
        <h2 style={{ color: '#0369a1' }}>For Rural & Underprivileged Students</h2>
        <p style={{ maxWidth: '800px', margin: '1rem auto 2rem', color: '#0c4a6e' }}>
          We provide special support for students from rural areas including 
          offline application assistance, local language support, and school-level guidance.
        </p>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '1rem',
          flexWrap: 'wrap'
        }}>
          <button style={{ 
            background: '#0369a1',
            padding: '0.875rem 2rem'
          }}>
            Learn About Rural Support
          </button>
          <button style={{ 
            background: 'transparent',
            color: '#0369a1',
            border: '2px solid #0369a1'
          }}>
            Contact Support Team
          </button>
        </div>
      </div>
    </div>
  );
}