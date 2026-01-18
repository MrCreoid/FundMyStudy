import { useEffect, useState } from "react";
import "../styles/cards.css";

export default function Scholarships({ token }) {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchScholarships();
  }, []);

  const fetchScholarships = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch("http://127.0.0.1:8000/scholarships/eligible", {
        headers: { 
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch scholarships: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setList(data.scholarships || []);
      }
      
    } catch (err) {
      setError(err.message);
      setList([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <h2>Finding Eligible Scholarships</h2>
        <div style={{ textAlign: 'center', padding: '4rem' }}>
          <div style={{
            fontSize: '3rem',
            marginBottom: '1rem',
            animation: 'spin 2s linear infinite'
          }}>🔍</div>
          <p>Scanning through government scholarship databases...</p>
          <div style={{
            width: '200px',
            height: '4px',
            background: 'linear-gradient(90deg, #e2e8f0, #4f46e5, #e2e8f0)',
            margin: '2rem auto',
            borderRadius: '2px',
            animation: 'shimmer 2s infinite'
          }}></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <h2>Error Loading Scholarships</h2>
        <div className="card" style={{ 
          background: '#fef2f2',
          border: '2px solid #fecaca',
          color: '#dc2626'
        }}>
          <h3>❌ Error</h3>
          <p>{error}</p>
          <button onClick={fetchScholarships} style={{ marginTop: '1rem' }}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>Your Eligible Scholarships</h2>
        <button onClick={fetchScholarships}>
          🔄 Refresh
        </button>
      </div>

      {list.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
          <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>📭</div>
          <h3 style={{ color: '#64748b' }}>No Eligible Scholarships Found</h3>
          <p>Complete your profile or update your information to see matching scholarships.</p>
          <button 
            onClick={() => window.location.hash = "#profile"} 
            style={{ marginTop: '1rem' }}
          >
            Update Profile
          </button>
        </div>
      ) : (
        <>
          <p style={{ marginBottom: '2rem' }}>
            Found <strong>{list.length}</strong> scholarships matching your profile
          </p>
          
          <div className="scholarship-grid">
            {list.map(s => (
              <div className="card" key={s.scholarshipId}>
                <div style={{
                  position: 'absolute',
                  top: '1rem',
                  right: '1rem',
                  background: s.score > 0.8 ? '#10b981' : s.score > 0.6 ? '#f59e0b' : '#ef4444',
                  color: 'white',
                  padding: '0.25rem 0.75rem',
                  borderRadius: '20px',
                  fontSize: '0.875rem',
                  fontWeight: '600'
                }}>
                  {Math.round(s.score * 100)}% Match
                </div>
                
                <h3>{s.name}</h3>
                <p><b>🏛️ Provider:</b> {s.provider}</p>
                <p><b>💰 Amount:</b> {s.amount}</p>
                <p><b>📅 Deadline:</b> {s.deadline}</p>
                {s.description && <p style={{ marginTop: '0.5rem' }}>{s.description}</p>}
                
                <div style={{ 
                  marginTop: '1.5rem',
                  display: 'flex',
                  gap: '1rem',
                  alignItems: 'center'
                }}>
                  <a 
                    href={s.apply_link} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    style={{ textDecoration: 'none' }}
                  >
                    <button>
                      🌐 Apply Now
                    </button>
                  </a>
                </div>
                
                {s.reasons && s.reasons.length > 0 && (
                  <div style={{ 
                    marginTop: '1.5rem',
                    padding: '1rem',
                    background: '#f8fafc',
                    borderRadius: '8px',
                    borderLeft: '4px solid #4f46e5'
                  }}>
                    <p style={{ fontSize: '0.9rem', margin: 0 }}>
                      <b>Eligibility:</b> {s.reasons.join(", ")}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}