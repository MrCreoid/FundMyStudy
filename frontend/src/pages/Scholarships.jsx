import { useEffect, useState } from "react";
import "../styles/cards.css";
import { auth } from '../firebase'; // Adjust path if needed

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
      
      console.log("🔄 Fetching scholarships...");
      
      // Get current user and token
      const user = auth.currentUser;
      if (!user) {
        setError("Not logged in. Please login first.");
        setLoading(false);
        window.location.href = '/login';
        return;
      }
      
      const token = await user.getIdToken(); // Get Firebase token
      
      // Add timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
      
      const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const response = await fetch(`${API_URL}/scholarships/eligible`, {
        signal: controller.signal,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      clearTimeout(timeoutId);
      
      console.log("📥 Response received:", response.status);
      
      if (!response.ok) {
        if (response.status === 401) {
          // Token expired, redirect to login
          setError("Session expired. Please login again.");
          window.location.href = '/login';
          return;
        }
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      console.log("✅ Data received:", data);
      
      setList(data.scholarships || data || []); // Handle different response formats
      
    } catch (err) {
      console.error("💥 Error:", err);
      
      if (err.name === 'AbortError') {
        setError("Request timed out. The server is taking too long to respond.");
      } else if (err.message.includes("Failed to fetch")) {
        setError("Cannot connect to server. Please check your internet connection.");
      } else {
        setError(err.message);
      }
      
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
            width: '300px',
            height: '4px',
            background: '#e2e8f0',
            margin: '2rem auto',
            borderRadius: '2px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: '60%',
              height: '100%',
              background: 'linear-gradient(90deg, #4f46e5, #7c3aed)',
              animation: 'loading 2s infinite'
            }}></div>
          </div>
          
          <div style={{ marginTop: '2rem' }}>
            <button 
              onClick={() => {
                const mockData = [
                  {
                    scholarshipId: "mock_1",
                    name: "Post Matric Scholarship for Minorities",
                    provider: "Ministry of Minority Affairs",
                    deadline: "2024-12-31",
                    amount: "₹20,000 per annum",
                    score: 1.0,
                    reasons: ["Income ≤ ₹250,000", "Minority category"],
                    apply_link: "https://scholarships.gov.in",
                    description: "For minority community students"
                  },
                  {
                    scholarshipId: "mock_2", 
                    name: "Maharashtra Government Scholarship",
                    provider: "Government of Maharashtra",
                    deadline: "2024-10-31",
                    amount: "Full tuition fee",
                    score: 0.8,
                    reasons: ["State = Maharashtra", "OBC category"],
                    apply_link: "https://mahadbt.maharashtra.gov.in",
                    description: "State scholarship for OBC students"
                  }
                ];
                setList(mockData);
                setLoading(false);
              }}
              style={{ 
                margin: '0.5rem',
                background: '#f59e0b',
                fontSize: '0.9rem'
              }}
            >
              Use Demo Data (For Presentation)
            </button>
            
            <button 
              onClick={fetchScholarships}
              style={{ 
                margin: '0.5rem',
                background: '#10b981',
                fontSize: '0.9rem'
              }}
            >
              Retry Loading
            </button>
          </div>
          
          <p style={{ marginTop: '2rem', color: '#64748b', fontSize: '0.9rem' }}>
            This may take a moment as we match your profile against 100+ scholarships...
          </p>
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