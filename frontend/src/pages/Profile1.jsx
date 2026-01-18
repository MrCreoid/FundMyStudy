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
  };

  const saveProfile = async () => {
    if (!profile.name || !profile.state || !profile.course) {
      alert("Please fill in required fields: Name, State, and Course");
      return;
    }

    setSaving(true);
    setSaveSuccess(false);

    try {
      const response = await fetch("http://127.0.0.1:8000/profiles", {
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

      setSaveSuccess(true);
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
        <p style={{ marginBottom: '2rem' }}>
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
              <input 
                placeholder="e.g., B.Tech, B.Sc"
                value={profile.course}
                onChange={e => handleChange('course', e.target.value)}
                style={inputStyle}
              />
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