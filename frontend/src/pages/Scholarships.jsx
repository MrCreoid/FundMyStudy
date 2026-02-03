import { useState } from "react";
import { auth } from "../firebase";
import { mockScholarships } from "../data/mockData";
import "../styles/cards.css";

export default function Scholarships({ setPage }) {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedScholarship, setSelectedScholarship] = useState(null);

  // Filter States removed as per user request to rely on profile data (backend handled)

  const fetchScholarships = async () => {
    try {
      setLoading(true);
      setError(null);

      const user = auth.currentUser;
      if (!user) {
        setError("Not logged in. Please login first.");
        return;
      }

      const token = await user.getIdToken();

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000);

      const API_URL = import.meta.env.VITE_API_URL ||
        ((window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
          ? "http://localhost:8000"
          : "https://fundmystudy-1.onrender.com");
      const response = await fetch(`${API_URL}/scholarships/eligible`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        signal: controller.signal
      });

      clearTimeout(timeoutId);


      if (!response.ok) {
        if (response.status === 401) {
          setError("Session expired. Please login again.");
          window.location.href = '/login';
          return;
        }
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      setList(data.scholarships || data || []); // Handle different response formats

    } catch (err) {
      console.error("Scholarship fetch error:", err);

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

  const handleUseDemoData = () => {
    setList(mockScholarships);
    setError(null);
    setLoading(false);
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
              onClick={handleUseDemoData}
              style={{
                margin: '0.5rem',
                background: '#f59e0b',
                fontSize: '0.9rem'
              }}
            >
              Use Demo Data (Show Mock)
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
          <button onClick={handleUseDemoData} style={{ marginTop: '1rem', marginLeft: '1rem', background: '#f59e0b' }}>
            Force Demo Data
          </button>
        </div>
      </div>
    );
  }

  // Helper to determine badge color
  const getBadgeColor = (score) => {
    if (score >= 0.9) return { bg: '#10b981', label: 'Perfect Match' };
    if (score >= 0.75) return { bg: '#3b82f6', label: 'Great Match' };
    if (score >= 0.6) return { bg: '#f59e0b', label: 'Good Match' };
    return { bg: '#64748b', label: 'Potential Match' };
  };

  // Helper to format date
  const formatDeadline = (dateString) => {
    if (!dateString || dateString === "Not specified") return "Not specified";
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return dateString; // Return original if not a valid date
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch (e) {
      return dateString;
    }
  };

  return (
    <div className="container">
      <div className="scholarship-header" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '2rem',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
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
          <div style={{ marginTop: '1.5rem' }}>
            <button
              onClick={() => setPage("profile")}
              style={{ marginRight: '1rem' }}
            >
              Update Profile
            </button>
            <button
              onClick={handleUseDemoData}
              style={{ background: '#f59e0b' }}
            >
              Show Demo Data
            </button>
          </div>
        </div>
      ) : (
        <>
          <p style={{ marginBottom: '2rem', color: '#64748b' }}>
            Found <strong>{list.length}</strong> scholarships matching your profile. Click on a card to view details.
          </p>

          <div className="scholarship-grid">
            {list.map((s, index) => {
              const badge = getBadgeColor(s.score);
              return (
                <div
                  className="card"
                  key={s.scholarshipId || index}
                  onClick={() => setSelectedScholarship(s)}
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div style={{
                    position: 'absolute',
                    top: '1rem',
                    right: '1rem',
                    background: badge.bg,
                    color: 'white',
                    padding: '0.25rem 0.75rem',
                    borderRadius: '20px',
                    fontSize: '0.75rem',
                    fontWeight: '600',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                  }}>
                    {Math.round(s.score * 100)}% Match
                  </div>

                  <h3 style={{ paddingRight: '4rem', fontSize: '1.5rem', marginBottom: '1rem' }}>{s.name}</h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', color: '#64748b', fontSize: '1rem' }}>
                    <div><b>🏛️ Provider:</b> {s.provider}</div>
                    <div><b>💰 Amount:</b> {s.amount}</div>
                    <div><b>⏳ Deadline:</b> {formatDeadline(s.deadline)}</div>
                    {/* Display Criteria Tags if specific */}
                    <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
                      {s.criteria?.gender && s.criteria.gender !== "Any" && (
                        <span style={{ fontSize: '0.75rem', background: '#f3e8ff', color: '#7e22ce', padding: '0.1rem 0.5rem', borderRadius: '4px' }}>
                          {s.criteria.gender} Only
                        </span>
                      )}
                      {s.criteria?.category && s.criteria.category !== "Any" && (
                        <span style={{ fontSize: '0.75rem', background: '#ecfccb', color: '#4d7c0f', padding: '0.1rem 0.5rem', borderRadius: '4px' }}>
                          {s.criteria.category}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </>
      )}

      {/* Detail Modal */}
      {selectedScholarship && (
        <div className="modal-overlay" onClick={() => setSelectedScholarship(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedScholarship(null)}>×</button>

            <div className="modal-header-section">
              <div className="match-badge" style={{ background: getBadgeColor(selectedScholarship.score).bg }}>
                {Math.round(selectedScholarship.score * 100)}% Match
              </div>
              <h2 className="modal-title">{selectedScholarship.name}</h2>
              <p className="modal-provider">{selectedScholarship.provider}</p>
            </div>

            <div className="modal-info-grid">
              <div>
                <p className="modal-info-label">Scholarship Amount</p>
                <p className="modal-info-value">{selectedScholarship.amount}</p>
              </div>
              <div>
                <p className="modal-info-label">Application Deadline</p>
                <p className="modal-info-value">{formatDeadline(selectedScholarship.deadline)}</p>
              </div>
            </div>

            <div style={{ marginBottom: '2rem' }}>
              <h4 className="modal-section-title">About this Scholarship</h4>
              <p className="modal-text">{selectedScholarship.description || "No description available."}</p>
            </div>

            {selectedScholarship.reasons && (
              <div className="modal-criteria-section">
                <h4 className="modal-criteria-title">Eligibility Criteria</h4>
                <ul className="modal-criteria-list">
                  {selectedScholarship.reasons.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </div>
            )}

            <a
              href={selectedScholarship.apply_link && !selectedScholarship.apply_link.startsWith('http')
                ? `https://${selectedScholarship.apply_link}`
                : selectedScholarship.apply_link || "#"}
              target="_blank"
              rel="noopener noreferrer"
              style={{ textDecoration: 'none' }}
            >
              <button style={{
                width: '100%',
                padding: '1rem',
                fontSize: '1.1rem',
                background: 'linear-gradient(90deg, #4f46e5, #7c3aed)',
                borderRadius: '12px',
                boxShadow: '0 4px 6px -1px rgba(79, 70, 229, 0.2)'
              }}>
                Apply Now 🚀
              </button>
            </a>

          </div>
        </div>
      )}
    </div>
  );
}