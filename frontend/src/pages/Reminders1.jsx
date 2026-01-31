import { useState, useEffect } from "react";


export default function Reminders({ token }) {
  const [reminders, setReminders] = useState([]);
  const [scholarships, setScholarships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token) return;
    fetchData();
  }, [token]);

  if (!token) {
    return (
      <div className="container" style={{ textAlign: "center", marginTop: "4rem" }}>
        <h2>🔒 Login Required</h2>
        <p>Please login to view and set reminder alerts.</p>
      </div>
    );
  }

  const fetchData = async () => {
    setLoading(true);
    const API_URL = import.meta.env.VITE_API_URL ||
      ((window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
        ? "http://localhost:8000"
        : "https://fundmystudy-1.onrender.com");

    try {
      // 1. Fetch My Reminders
      const remindersRes = await fetch(`${API_URL}/reminders/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const remindersData = await remindersRes.json();
      setReminders(remindersData.reminders || []);

      // 2. Fetch Scholarship Suggestions (Fast mode)
      const schRes = await fetch(`${API_URL}/scholarships/eligible-fast`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const schData = await schRes.json();
      setScholarships(schData.scholarships || []);

    } catch (err) {
      console.error("Error fetching data:", err);
      setError("Failed to load reminders. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = async (scholarshipId) => {
    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

    try {
      const response = await fetch(`${API_URL}/reminders/subscribe`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ scholarshipId })
      });

      const data = await response.json();

      if (!response.ok) {
        alert(`Error: ${data.detail || "Failed to subscribe"}`);
        return;
      }

      alert(`✅ Email Reminder set! Status: ${data.email_status.status}`);
      fetchData(); // Refresh list

    } catch (err) {
      console.error(err);
      alert("Failed to connect to server.");
    }
  };

  const handleTestEmail = async () => {
    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
    const msg = prompt("Enter test message:", "Hello from FundMyStudy!");
    if (!msg) return;

    try {
      const response = await fetch(`${API_URL}/reminders/test-email`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ message: msg })
      });
      const data = await response.json();
      alert(`Test Result: ${JSON.stringify(data.result)}`);
    } catch (err) {
      alert("Test failed");
    }
  };

  const isSubscribed = (schId) => {
    return reminders.some(r => r.scholarshipId === schId);
  };

  return (
    <div className="container">
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2>📅 Deadline Reminders</h2>
          <button onClick={handleTestEmail} className="test-email-btn">
            📧 Test Email
          </button>
        </div>

        <p style={{ marginBottom: '2rem', color: 'var(--text-muted)' }}>
          Get Email alerts 7 days before application deadlines.
        </p>

        {/* SECTION 1: ACTIVE REMINDERS */}
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3>🔔 Your Active Reminders</h3>
          {loading ? (
            <p>Loading...</p>
          ) : reminders.length === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>No active reminders set.</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {reminders.map(reminder => (
                <div style={{ padding: '1rem', borderBottom: '1px solid var(--input-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <strong style={{ display: 'block', fontSize: '1.2rem', color: 'var(--text-main)' }}>{reminder.scholarshipName}</strong>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>Deadline: {reminder.deadline}</span>
                    <div style={{ fontSize: '0.85rem', color: 'var(--primary)', marginTop: '8px', fontWeight: '500' }}>
                      ✓ Email Active for {reminder.email}
                    </div>
                  </div>
                </div>
              ))}
            </ul>
          )}
        </div>

        {/* SECTION 2: SUGGESTIONS */}
        <h3 style={{ marginBottom: '1rem' }}>📌 Recommended for You</h3>
        <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
          {scholarships.map(sch => (
            <div key={sch.scholarshipId} className="card scholarship-suggestion-card">
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '8px' }}>
                  <span className="amount-tag">
                    {sch.amount}
                  </span>
                  <span className="deadline-tag">
                    ⏳ {sch.deadline}
                  </span>
                </div>
                <h4 className="scholarship-name">{sch.name}</h4>
                <p className="scholarship-provider">
                  By {sch.provider}
                </p>

                {isSubscribed(sch.scholarshipId) ? (
                  <button disabled className="subscribed-btn">
                    ✓ Reminding You
                  </button>
                ) : (
                  <button
                    onClick={() => handleSubscribe(sch.scholarshipId)}
                    className="subscribe-btn"
                  >
                    📧 Email Me
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
