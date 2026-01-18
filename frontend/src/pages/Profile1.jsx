import { useState } from "react";

export default function Profile({ token }) {
  const [profile, setProfile] = useState({
    name: "",
    income: "",
    caste: "",
    category: "",
    state: "",
    course: "",
    marks: ""
  });
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleChange = (field, value) => {
    setProfile(prev => ({ ...prev, [field]: value }));
    setSaveSuccess(false); // Reset success message on change
  };

const saveProfile = async () => {
  // Validate required fields
  if (!profile.name || !profile.state || !profile.course) {
    alert("Please fill in required fields: Name, State, and Course");
    return;
  }

  // Validate marks if provided
  if (profile.marks && (parseFloat(profile.marks) < 0 || parseFloat(profile.marks) > 100)) {
    alert("Please enter a valid percentage between 0 and 100");
    return;
  }

  setSaving(true);
  setSaveSuccess(false);

  try {
    // For testing - use dev token if no real token
    const authToken = token || "dev_token_123";
    
    console.log("Saving profile with token:", authToken ? "Token exists" : "No token");
    
    const response = await fetch("http://127.0.0.1:8000/profiles", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authToken}`
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

    console.log("Response status:", response.status);
    console.log("Response headers:", response.headers);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Error response:", errorText);
      throw new Error(`Server responded with ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    console.log("Profile saved successfully:", data);
    setSaveSuccess(true);
    
    // Show success message
    setTimeout(() => {
      alert("Profile saved successfully! You can now check scholarships.");
      // Don't auto-navigate for now
      // window.location.hash = "#scholarships";
    }, 500);

  } catch (error) {
    console.error("Error saving profile:", error);
    alert(`Failed to save profile: ${error.message}\n\nBackend URL: http://127.0.0.1:8000`);
  } finally {
    setSaving(false);
  }
};

  const loadSampleData = () => {
    setProfile({
      name: "Rohit Sharma",
      income: "180000",
      caste: "SC",
      category: "Minority",
      state: "Uttar Pradesh",
      course: "B.Sc",
      marks: "82.5"
    });
    setSaveSuccess(false);
  };

  return (
    <div className="container">
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h2>Complete Your Profile</h2>
        <p style={{ marginBottom: '2rem' }}>
          Fill in your details to get personalized scholarship recommendations.
          <br />
          <span style={{ color: '#ef4444', fontWeight: '600' }}>*</span> Required fields
        </p>
        
        {saveSuccess && (
          <div style={{
            background: 'linear-gradient(135deg, #10b981, #34d399)',
            color: 'white',
            padding: '1rem 1.5rem',
            borderRadius: '12px',
            marginBottom: '2rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            animation: 'fadeIn 0.3s ease'
          }}>
            <span style={{ fontSize: '1.5rem' }}>✅</span>
            <div>
              <strong>Profile saved successfully!</strong>
              <p style={{ margin: '0.25rem 0 0', opacity: 0.9, fontSize: '0.95rem' }}>
                Redirecting to scholarships page...
              </p>
            </div>
          </div>
        )}
        
        <div className="card">
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '1.5rem',
            marginBottom: '2rem'
          }}>
            {/* Name Field */}
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
            
            {/* Income Field */}
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
            
            {/* Caste Field */}
            <div>
              <label style={labelStyle}>Caste Category</label>
              <select 
                value={profile.caste}
                onChange={e => handleChange('caste', e.target.value)}
                style={inputStyle}
              >
                <option value="">Select Category</option>
                <option value="General">General</option>
                <option value="OBC">OBC (Other Backward Class)</option>
                <option value="SC">SC (Scheduled Caste)</option>
                <option value="ST">ST (Scheduled Tribe)</option>
              </select>
            </div>
            
            {/* Minority Field */}
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
            
            {/* State Field */}
            <div>
              <label style={labelStyle}>
                State <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input 
                placeholder="e.g., Maharashtra, Uttar Pradesh"
                value={profile.state}
                onChange={e => handleChange('state', e.target.value)}
                style={inputStyle}
              />
            </div>
            
            {/* Course Field */}
            <div>
              <label style={labelStyle}>
                Course <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input 
                placeholder="e.g., B.Tech, B.Sc, MBBS, BA, etc."
                value={profile.course}
                onChange={e => handleChange('course', e.target.value)}
                style={inputStyle}
              />
            </div>
            
            {/* Marks Field */}
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
            justifyContent: 'space-between',
            alignItems: 'center',
            borderTop: '1px solid #e2e8f0',
            paddingTop: '2rem',
            flexWrap: 'wrap'
          }}>
            <div>
              {saving && (
                <span style={{ color: '#6366f1', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ animation: 'spin 1s linear infinite' }}>⟳</span>
                  Saving your profile...
                </span>
              )}
            </div>
            
            <div style={{ display: 'flex', gap: '1rem' }}>
              <button 
                onClick={loadSampleData}
                style={{ 
                  background: '#f1f5f9', 
                  color: '#475569',
                  padding: '0.75rem 1.5rem'
                }}
              >
                Load Sample Data
              </button>
              <button 
                onClick={saveProfile} 
                disabled={saving || !profile.name || !profile.state || !profile.course}
                style={{ 
                  padding: '0.875rem 2.5rem',
                  opacity: (!profile.name || !profile.state || !profile.course) ? 0.6 : 1
                }}
              >
                {saving ? 'Saving...' : '💾 Save Profile & Continue'}
              </button>
            </div>
          </div>
        </div>
        
        <div style={{ 
          marginTop: '2rem',
          padding: '1.5rem',
          background: 'linear-gradient(135deg, #f0fdf4, #dcfce7)',
          borderRadius: '12px',
          border: '2px solid #bbf7d0'
        }}>
          <h4 style={{ color: '#166534', marginBottom: '0.75rem' }}>📝 Profile Tips</h4>
          <ul style={{ 
            listStyle: 'none', 
            padding: 0,
            fontSize: '0.95rem',
            color: '#166534'
          }}>
            <li style={{ marginBottom: '0.5rem' }}>✅ <strong>Required fields</strong> are marked with *</li>
            <li style={{ marginBottom: '0.5rem' }}>✅ Enter <strong>accurate income</strong> for correct eligibility</li>
            <li style={{ marginBottom: '0.5rem' }}>✅ Select your <strong>correct caste category</strong> for reserved scholarships</li>
            <li style={{ marginBottom: '0.5rem' }}>✅ Your data is <strong>encrypted and secure</strong></li>
            <li>✅ You can <strong>update your profile</strong> anytime</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

const labelStyle = {
  display: 'block',
  marginBottom: '0.5rem',
  fontWeight: '600',
  color: '#334155',
  fontSize: '0.95rem'
};

const inputStyle = {
  width: '100%',
  padding: '0.875rem 1rem',
  border: '2px solid #e2e8f0',
  borderRadius: '10px',
  fontSize: '1rem',
  transition: 'all 0.3s ease',
  background: 'white'
};