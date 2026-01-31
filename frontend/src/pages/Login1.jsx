import { signInWithEmailAndPassword, signOut } from "firebase/auth";
import { auth } from "../firebase";
import { useState } from "react";

export default function Login({ onLogin, setPage }) {
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
          <p style={{ color: 'var(--text-muted)' }}>Sign in to access your personalized scholarship recommendations</p>
        </div>

        <div className="card" style={{ textAlign: 'left' }}>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '600',
              color: 'var(--text-muted)'
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
              color: 'var(--text-muted)'
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
            color: 'var(--text-muted)'
          }}>
            <p>Don't have an account? <a
              href="#"
              onClick={(e) => { e.preventDefault(); setPage("signup"); }}
              style={{
                color: '#4f46e5',
                cursor: 'pointer',
                fontWeight: '600',
                textDecoration: 'none',
                marginLeft: '0.25rem'
              }}
            >
              Sign up
            </a></p>
          </div>
        </div>
      </div>
    </div>
  );
}