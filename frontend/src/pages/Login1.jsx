import { signInWithEmailAndPassword, signOut } from "firebase/auth";
import { auth } from "../firebase";
import { useState } from "react";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  // Clear any existing sessions on mount
  useState(() => {
    signOut(auth).catch(() => {
      // Ignore errors if no user is signed in
    });
  }, []);

  const login = async () => {
    if (!email || !password) {
      alert("Please fill in all fields");
      return;
    }

    setLoading(true);
    try {
      const cred = await signInWithEmailAndPassword(auth, email, password);
      const token = await cred.user.getIdToken();
      onLogin(token);
    } catch (error) {
      alert(error.message || "Invalid credentials. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      login();
    }
  };

  return (
    <div className="container">
      <div style={{ 
        maxWidth: '500px', 
        margin: '0 auto',
        textAlign: 'center'
      }}>
        <div style={{ marginBottom: '2rem' }}>
          <h2>Welcome Back</h2>
          <p style={{ color: '#64748b' }}>Sign in to access your personalized scholarship recommendations</p>
        </div>
        
        <div className="card" style={{ textAlign: 'left' }}>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '0.5rem',
              fontWeight: '600',
              color: '#334155'
            }}>
              Email Address
            </label>
            <input 
              type="email" 
              placeholder="student@example.com" 
              value={email}
              onChange={e => setEmail(e.target.value)}
              onKeyPress={handleKeyPress}
              style={{ padding: '1rem', fontSize: '1rem' }}
            />
          </div>
          
          <div style={{ marginBottom: '2rem' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '0.5rem',
              fontWeight: '600',
              color: '#334155'
            }}>
              Password
            </label>
            <input 
              type="password" 
              placeholder="Enter your password" 
              value={password}
              onChange={e => setPassword(e.target.value)}
              onKeyPress={handleKeyPress}
              style={{ padding: '1rem', fontSize: '1rem' }}
            />
          </div>
          
          <button 
            onClick={login} 
            disabled={loading}
            style={{ width: '100%', padding: '1rem' }}
          >
            {loading ? (
              <>
                <span style={{ 
                  display: 'inline-block', 
                  animation: 'spin 1s linear infinite',
                  marginRight: '0.5rem'
                }}>⟳</span>
                Signing In...
              </>
            ) : 'Sign In'}
          </button>
          
          <div style={{ 
            marginTop: '1.5rem', 
            textAlign: 'center',
            color: '#64748b'
          }}>
            <p>Don't have an account? <span style={{ 
              color: '#4f46e5', 
              cursor: 'pointer', 
              fontWeight: '600',
              textDecoration: 'underline'
            }} onClick={() => alert('Please contact your school administrator to create an account.')}>
              Contact your school
            </span></p>
          </div>
        </div>
        
        <div style={{ 
          marginTop: '2rem',
          padding: '1.5rem',
          background: 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
          borderRadius: '12px',
          border: '2px solid #bae6fd'
        }}>
          <h4 style={{ color: '#0369a1', marginBottom: '0.5rem' }}>For Rural Students</h4>
          <p style={{ fontSize: '0.95rem', color: '#0c4a6e' }}>
            Having trouble logging in? Contact your school's computer lab or email support@fundmystudy.in
          </p>
        </div>
      </div>
    </div>
  );
}