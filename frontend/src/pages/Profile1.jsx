import { useState, useEffect } from "react";

export default function Profile({ token }) {
  const [profile, setProfile] = useState({
    name: "",
    income: "",
    caste: "",
    category: "",
    state: "",
    course: "", // Stores the final value
    marks: ""
  });

  // Logic to determine if "Other" is active
  const COURSE_OPTIONS = [
    "B.Tech", "MBBS", "B.Sc", "B.Com", "B.A.", "BBA", "BCA",
    "LLB", "B.Arch", "B.Pharm", "Diploma", "Class 11",
    "Class 12", "Vocational"
  ];

  const [isOtherCourse, setIsOtherCourse] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProfile();
  }, [token]);

  const fetchProfile = async () => {
    try {
      setError(null);
      const API_URL = import.meta.env.VITE_API_URL ||
        ((window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
          ? "http://localhost:8000"
          : "https://fundmystudy-1.onrender.com");
      const response = await fetch(`${API_URL}/profiles/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error("Session expired. Please login again.");
        }
        throw new Error(`Failed to load profile: ${response.status}`);
      }

      const data = await response.json();
      const loadedCourse = data.course || "";

      // Determine if loaded course is "Other"
      const isCustom = loadedCourse && !COURSE_OPTIONS.includes(loadedCourse);
      setIsOtherCourse(isCustom);

      setProfile({
        name: data.name || "",
        income: data.income || "",
        caste: data.caste || "",
        category: data.category || "",
        state: data.state || "",
        course: loadedCourse,
        marks: data.marks || ""
      });
    } catch (error) {
      console.error("Error fetching profile:", error);
      setError(error.message);
      if (error.message.includes("Session expired")) {
        // Optional: Trigger logout potentially or let user see the error
        // For now, showing the error is better than silent fail
      }
    }
  };

  const handleChange = (field, value) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  const handleCourseSelect = (value) => {
    if (value === "Other") {
      setIsOtherCourse(true);
      // Don't clear course immediately if user mis-clicks, but typically "Other" starts empty or previous custom
      if (COURSE_OPTIONS.includes(profile.course)) {
        setProfile(prev => ({ ...prev, course: "" }));
      }
    } else {
      setIsOtherCourse(false);
      setProfile(prev => ({ ...prev, course: value }));
    }
  };

  const saveProfile = async () => {
    const API_URL = import.meta.env.VITE_API_URL ||
      ((window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
        ? "http://localhost:8000"
        : "https://fundmystudy-1.onrender.com");

    if (!profile.name || !profile.state || !profile.course) {
      alert("Please fill in required fields: Name, State, and Course");
      return;
    }

    setSaving(true);

    try {
      const response = await fetch(`${API_URL}/profiles`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          name: profile.name,
          income: parseFloat(profile.income) || 0,
          caste: profile.caste || "General",
          category: profile.category || "Not Minority",
          state: profile.state,
          course: profile.course,
          marks: parseFloat(profile.marks) || 0
        })
      });

      if (!response.ok) {
        throw new Error(`Failed to save profile: ${response.status}`);
      }

      alert("Profile saved successfully!");

    } catch (error) {
      alert(`Failed to save profile: ${error.message}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="container">
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h2>Complete Your Profile</h2>
        {error && (
          <div style={{
            background: '#fee2e2',
            color: '#dc2626',
            padding: '1rem',
            borderRadius: '8px',
            marginBottom: '1rem',
            border: '1px solid #fecaca'
          }}>
            ⚠️ {error}
            <button
              onClick={fetchProfile}
              style={{
                marginLeft: '1rem',
                padding: '0.25rem 0.75rem',
                fontSize: '0.9rem',
                cursor: 'pointer'
              }}>
              Retry
            </button>
          </div>
        )}
        <p style={{ marginBottom: '2rem', color: 'var(--text-muted)' }}>
          Fill in your details to get personalized scholarship recommendations.
          <br />
          <span style={{ color: '#ef4444' }}>*</span> Required fields
        </p>

        <div className="card">
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '1.5rem',
            marginBottom: '2rem'
          }}>
            <div>
              <label style={labelStyle}>
                Full Name <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input
                placeholder="Enter your full name"
                value={profile.name}
                onChange={e => handleChange('name', e.target.value)}
                style={inputStyle}
              />
            </div>

            <div>
              <label style={labelStyle}>Annual Family Income (₹)</label>
              <input
                type="number"
                placeholder="e.g., 250000"
                value={profile.income}
                onChange={e => handleChange('income', e.target.value)}
                style={inputStyle}
                min="0"
              />
            </div>

            <div>
              <label style={labelStyle}>Caste Category</label>
              <select
                value={profile.caste}
                onChange={e => handleChange('caste', e.target.value)}
                style={inputStyle}
              >
                <option value="">Select Category</option>
                <option value="General">General</option>
                <option value="OBC">OBC</option>
                <option value="SC">SC</option>
                <option value="ST">ST</option>
              </select>
            </div>

            <div>
              <label style={labelStyle}>Minority Category</label>
              <select
                value={profile.category}
                onChange={e => handleChange('category', e.target.value)}
                style={inputStyle}
              >
                <option value="">Select if applicable</option>
                <option value="Minority">Minority</option>
                <option value="Not Minority">Not Minority</option>
              </select>
            </div>

            <div>
              <label style={labelStyle}>
                State <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input
                placeholder="e.g., Maharashtra"
                value={profile.state}
                onChange={e => handleChange('state', e.target.value)}
                style={inputStyle}
              />
            </div>

            <div>
              <label style={labelStyle}>
                Course <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <select
                value={isOtherCourse ? "Other" : profile.course}
                onChange={e => handleCourseSelect(e.target.value)}
                style={inputStyle}
              >
                <option value="">Select Course</option>
                {COURSE_OPTIONS.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
                <option value="Other">Other (Add your own)</option>
              </select>

              {isOtherCourse && (
                <input
                  placeholder="Type your course name..."
                  value={profile.course}
                  onChange={e => handleChange('course', e.target.value)}
                  style={{ ...inputStyle, marginTop: '0.5rem', borderColor: '#6366f1' }}
                  autoFocus
                />
              )}
            </div>

            <div>
              <label style={labelStyle}>Percentage/CGPA</label>
              <input
                type="number"
                step="0.01"
                placeholder="e.g., 87.5"
                value={profile.marks}
                onChange={e => handleChange('marks', e.target.value)}
                style={inputStyle}
                min="0"
                max="100"
              />
            </div>
          </div>

          <div style={{
            display: 'flex',
            gap: '1rem',
            justifyContent: 'flex-end',
            borderTop: '1px solid #e2e8f0',
            paddingTop: '2rem'
          }}>
            <button
              onClick={saveProfile}
              disabled={saving || !profile.name || !profile.state || !profile.course}
              style={{
                padding: '0.875rem 2.5rem',
                opacity: (!profile.name || !profile.state || !profile.course) ? 0.6 : 1
              }}
            >
              {saving ? 'Saving...' : '💾 Save Profile'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

const labelStyle = {
  display: 'block',
  marginBottom: '0.5rem',
  fontWeight: '600',
  color: 'var(--text-muted)',
  fontSize: '0.95rem'
};

const inputStyle = {
  width: '100%',
  padding: '0.875rem 1rem',
  border: '2px solid #e2e8f0',
  borderRadius: '10px',
  fontSize: '1rem',
  transition: 'all 0.3s ease',
  color: 'var(--text-main)',
  background: 'var(--input-bg)',
  borderColor: 'var(--input-border)'
};