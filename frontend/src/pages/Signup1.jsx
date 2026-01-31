import { useState } from "react";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "../firebase";

export default function Signup({ onLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [profile, setProfile] = useState({
        name: "",
        phone: "",
        income: "",
        caste: "",
        category: "",
        state: "",
        course: "",
        marks: ""
    });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [isOtherCourse, setIsOtherCourse] = useState(false);

    const COURSE_OPTIONS = [
        "B.Tech", "MBBS", "B.Sc", "B.Com", "B.A.", "BBA", "BCA",
        "LLB", "B.Arch", "B.Pharm", "Diploma", "Class 11",
        "Class 12", "Vocational"
    ];

    const handleProfileChange = (field, value) => {
        setProfile(prev => ({ ...prev, [field]: value }));
    };

    const handleCourseSelect = (value) => {
        if (value === "Other") {
            setIsOtherCourse(true);
            setProfile(prev => ({ ...prev, course: "" }));
        } else {
            setIsOtherCourse(false);
            setProfile(prev => ({ ...prev, course: value }));
        }
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        if (!email || !password || !profile.name || !profile.state || !profile.course || !profile.phone) {
            setError("Please fill in all required fields (marked *)");
            setLoading(false);
            return;
        }

        try {
            // 1. Create User in Firebase
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            const token = await user.getIdToken();

            // 2. Create Profile in Backend
            const API_URL = import.meta.env.VITE_API_URL ||
                ((window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
                    ? "http://localhost:8000"
                    : "https://fundmystudy-1.onrender.com");
            const response = await fetch(`${API_URL}/profiles`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    name: profile.name,
                    phone: profile.phone,
                    income: parseFloat(profile.income) || 0,
                    caste: profile.caste || "General",
                    category: profile.category || "Not Minority",
                    state: profile.state,
                    course: profile.course,
                    marks: parseFloat(profile.marks) || 0
                })
            });

            if (!response.ok) {
                throw new Error("Account created but failed to save profile. Please update profile later.");
            }

            // 3. Login
            onLogin(token);

        } catch (err) {
            console.error(err);
            if (err.code === 'auth/email-already-in-use') {
                setError("Email already in use. Please login instead.");
            } else {
                setError(err.message || "Failed to create account");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
            <div className="card" style={{ width: '100%', maxWidth: '800px' }}>
                <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Create Account</h2>

                {error && (
                    <div style={{
                        background: '#fee2e2',
                        color: '#dc2626',
                        padding: '1rem',
                        borderRadius: '8px',
                        marginBottom: '1rem',
                        textAlign: 'center'
                    }}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSignup}>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>

                        {/* Account Details */}
                        <div>
                            <h3 style={{ marginBottom: '1rem', color: '#64748b' }}>Login Details</h3>
                            <div style={formGroup}>
                                <label style={labelStyle}>Email <span style={{ color: '#ef4444' }}>*</span></label>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    style={inputStyle}
                                    placeholder="name@example.com"
                                />
                            </div>

                            <div style={formGroup}>
                                <label style={labelStyle}>Password <span style={{ color: '#ef4444' }}>*</span></label>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    style={inputStyle}
                                    placeholder="Create a strong password"
                                />
                            </div>
                        </div>

                        {/* Profile Details */}
                        <div>
                            <h3 style={{ marginBottom: '1rem', color: '#64748b' }}>Student Profile</h3>

                            <div style={formGroup}>
                                <label style={labelStyle}>Full Name <span style={{ color: '#ef4444' }}>*</span></label>
                                <input
                                    value={profile.name}
                                    onChange={e => handleProfileChange('name', e.target.value)}
                                    style={inputStyle}
                                    placeholder="Student Name"
                                />
                            </div>

                            <div style={formGroup}>
                                <label style={labelStyle}>Phone Number <span style={{ color: '#ef4444' }}>*</span></label>
                                <input
                                    type="tel"
                                    value={profile.phone}
                                    onChange={e => handleProfileChange('phone', e.target.value)}
                                    style={inputStyle}
                                    placeholder="9876543210"
                                    maxLength="10"
                                />
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                <div style={formGroup}>
                                    <label style={labelStyle}>State <span style={{ color: '#ef4444' }}>*</span></label>
                                    <input
                                        value={profile.state}
                                        onChange={e => handleProfileChange('state', e.target.value)}
                                        style={inputStyle}
                                        placeholder="State"
                                    />
                                </div>
                                <div style={formGroup}>
                                    <label style={labelStyle}>Course <span style={{ color: '#ef4444' }}>*</span></label>
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
                                            value={profile.course}
                                            onChange={e => handleProfileChange('course', e.target.value)}
                                            style={{ ...inputStyle, marginTop: '0.5rem', borderColor: '#6366f1' }}
                                            placeholder="Type your course name..."
                                            autoFocus
                                        />
                                    )}
                                </div>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                <div style={formGroup}>
                                    <label style={labelStyle}>Income (₹)</label>
                                    <input
                                        type="number"
                                        value={profile.income}
                                        onChange={e => handleProfileChange('income', e.target.value)}
                                        style={inputStyle}
                                        placeholder="Annual Income"
                                    />
                                </div>
                                <div style={formGroup}>
                                    <label style={labelStyle}>Marks (%)</label>
                                    <input
                                        type="number"
                                        value={profile.marks}
                                        onChange={e => handleProfileChange('marks', e.target.value)}
                                        style={inputStyle}
                                        placeholder="Percentage"
                                    />
                                </div>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                <div style={formGroup}>
                                    <label style={labelStyle}>Category</label>
                                    <select
                                        value={profile.caste}
                                        onChange={e => handleProfileChange('caste', e.target.value)}
                                        style={inputStyle}
                                    >
                                        <option value="General">General</option>
                                        <option value="OBC">OBC</option>
                                        <option value="SC">SC</option>
                                        <option value="ST">ST</option>
                                    </select>
                                </div>
                                <div style={formGroup}>
                                    <label style={labelStyle}>Minority</label>
                                    <select
                                        value={profile.category}
                                        onChange={e => handleProfileChange('category', e.target.value)}
                                        style={inputStyle}
                                    >
                                        <option value="Not Minority">No</option>
                                        <option value="Minority">Yes</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            width: '100%',
                            padding: '1rem',
                            marginTop: '2rem',
                            fontSize: '1.1rem',
                            fontWeight: 'bold',
                            background: 'linear-gradient(to right, #4f46e5, #7c3aed)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '10px',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            opacity: loading ? 0.7 : 1
                        }}
                    >
                        {loading ? 'Creating Account...' : '✨ Create Account & Profile'}
                    </button>
                </form>
            </div>
        </div>
    );
}

const formGroup = {
    marginBottom: '1rem'
};

const labelStyle = {
    display: 'block',
    marginBottom: '0.5rem',
    fontWeight: '600',
    color: '#334155',
    fontSize: '0.9rem'
};

const inputStyle = {
    width: '100%',
    padding: '0.75rem',
    border: '2px solid #e2e8f0',
    borderRadius: '8px',
    fontSize: '1rem'
};
