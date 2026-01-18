import { useEffect, useState } from "react";
import "../styles/cards.css";

export default function Scholarships({ token }) {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("🎯 Scholarships component mounted");
    console.log("🔑 Token exists:", !!token);
    
    fetchScholarships();
  }, []);

  const fetchScholarships = async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log("🔄 Fetching scholarships...");
      console.log("📡 URL: http://127.0.0.1:8000/scholarships/eligible");
      console.log("🔐 Token:", token ? `${token.substring(0, 30)}...` : "No token");
      
      // Use dev token if no real token
      const authToken = token || "dev_token_123";
      
      const response = await fetch("http://127.0.0.1:8000/scholarships/eligible", {
        headers: { 
          "Authorization": `Bearer ${authToken}`,
          "Content-Type": "application/json"
        }
      });
      
      console.log("📥 Response status:", response.status);
      console.log("📥 Response headers:", Object.fromEntries(response.headers.entries()));
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Error response:", errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }
      
      const data = await response.json();
      console.log("✅ Data received:", data);
      
      // Check if data has scholarships array
      if (data.scholarships) {
        setList(data.scholarships);
        console.log(`✅ Found ${data.scholarships.length} scholarships`);
      } else if (data.error) {
        setError(data.error);
        console.log("⚠️  Error in response:", data.error);
      } else {
        console.log("⚠️  Unexpected response format:", data);
        setList([]);
      }
      
    } catch (err) {
      console.error("💥 Error fetching scholarships:", err);
      setError(err.message);
      setList([]);
    } finally {
      setLoading(false);
    }
  };

  const loadMockData = () => {
    console.log("🔄 Loading mock data for testing...");
    const mockScholarships = [
      {
        scholarshipId: "mock_1",
        name: "Post Matric Scholarship for Minorities",
        provider: "Ministry of Minority Affairs",
        score: 1.0,
        apply_link: "https://scholarships.gov.in",
        deadline: "2024-12-31",
        amount: "Up to ₹20,000 per annum",
        description: "For minority community students"
      },
      {
        scholarshipId: "mock_2",
        name: "National Merit Scholarship",
        provider: "Department of Higher Education",
        score: 0.8,
        apply_link: "https://education.gov.in",
        deadline: "2024-11-30",
        amount: "₹12,000 per annum",
        description: "For meritorious students"
      }
    ];
    setList(mockScholarships);
    setLoading(false);
  };

  const checkBackend = async () => {
    try {
      console.log("🔍 Checking backend connectivity...");
      const response = await fetch("http://127.0.0.1:8000/");
      const data = await response.json();
      console.log("✅ Backend is running:", data);
      alert(`Backend is running: ${data.message}`);
    } catch (err) {
      console.error("❌ Backend is not reachable:", err);
      alert("Backend is not reachable. Make sure it's running on port 8000.");
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
          }}>🔄</div>
          <p>Loading scholarships...</p>
          <div style={{
            width: '200px',
            height: '4px',
            background: 'linear-gradient(90deg, #e2e8f0, #4f46e5, #e2e8f0)',
            margin: '2rem auto',
            borderRadius: '2px',
            animation: 'shimmer 2s infinite'
          }}></div>
          <button 
            onClick={loadMockData}
            style={{ margin: '1rem', background: '#f59e0b' }}
          >
            Load Mock Data (Testing)
          </button>
          <button 
            onClick={checkBackend}
            style={{ margin: '1rem', background: '#10b981' }}
          >
            Check Backend
          </button>
          <div style={{ marginTop: '2rem', color: '#666', fontSize: '0.9rem' }}>
            <p>Debug Info:</p>
            <p>Token: {token ? "Present" : "Missing"}</p>
            <p>Backend: http://127.0.0.1:8000</p>
          </div>
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
          <h3>❌ Error: {error}</h3>
          <p>Please try the following:</p>
          <ul>
            <li>1. Make sure backend is running (port 8000)</li>
            <li>2. Complete your profile first</li>
            <li>3. Check browser console for details</li>
          </ul>
          <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
            <button onClick={fetchScholarships}>
              Retry
            </button>
            <button onClick={loadMockData} style={{ background: '#f59e0b' }}>
              Use Mock Data
            </button>
            <button onClick={checkBackend} style={{ background: '#10b981' }}>
              Check Backend
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>Your Eligible Scholarships</h2>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button onClick={fetchScholarships} style={{ background: '#10b981' }}>
            🔄 Refresh
          </button>
          <button onClick={checkBackend} style={{ background: '#3b82f6' }}>
            🔍 Check Backend
          </button>
        </div>
      </div>

      {list.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
          <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>📭</div>
          <h3 style={{ color: '#64748b' }}>No Eligible Scholarships Found</h3>
          <p>This could be because:</p>
          <ul style={{ textAlign: 'left', maxWidth: '500px', margin: '1rem auto' }}>
            <li>• Your profile doesn't match any scholarship criteria</li>
            <li>• No scholarships are in the database</li>
            <li>• There's an issue with the backend</li>
          </ul>
          <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <button onClick={loadMockData} style={{ background: '#f59e0b' }}>
              Load Mock Data for Testing
            </button>
            <button onClick={() => window.location.hash = "#profile"} style={{ background: '#8b5cf6' }}>
              Update Profile
            </button>
          </div>
        </div>
      ) : (
        <>
          <p style={{ marginBottom: '2rem' }}>
            Found <strong>{list.length}</strong> scholarships matching your profile
          </p>
          
          <div className="scholarship-grid">
            {list.map(s => (
              <div className="card" key={s.scholarshipId || s.id || s.name}>
                {s.score && (
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
                )}
                
                <h3>{s.name || "Unnamed Scholarship"}</h3>
                <p><b>🏛️ Provider:</b> {s.provider || "Unknown"}</p>
                <p><b>💰 Amount:</b> {s.amount || "Not specified"}</p>
                <p><b>📅 Deadline:</b> {s.deadline || "Not specified"}</p>
                {s.description && <p><b>📝 Description:</b> {s.description}</p>}
                
                <div style={{ 
                  marginTop: '1.5rem',
                  display: 'flex',
                  gap: '1rem',
                  alignItems: 'center'
                }}>
                  <a 
                    href={s.apply_link || s.source_url || "#"} 
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
                      <b>Why you qualify:</b> {s.reasons.join(", ")}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
      
      {/* Debug panel (visible in development) */}
      {process.env.NODE_ENV === 'development' && (
        <div className="card" style={{ 
          marginTop: '3rem',
          background: '#f1f5f9',
          fontSize: '0.8rem'
        }}>
          <h4>🛠️ Debug Information</h4>
          <p><b>Scholarships loaded:</b> {list.length}</p>
          <p><b>Token present:</b> {token ? "Yes" : "No"}</p>
          <p><b>Backend URL:</b> http://127.0.0.1:8000</p>
          <button 
            onClick={() => {
              console.log("Current list:", list);
              console.log("Token:", token);
            }}
            style={{ marginTop: '1rem', fontSize: '0.8rem', padding: '0.5rem 1rem' }}
          >
            Log Debug Info to Console
          </button>
        </div>
      )}
    </div>
  );
}