import { useState, useEffect } from "react";
import Navbar from "./components/Navbar1";
import Landing from "./pages/Landing";
import Login from "./pages/Login1";
import Signup from "./pages/Signup1";
import Profile from "./pages/Profile1";
import Scholarships from "./pages/Scholarships";
import Reminders from "./pages/Reminders1";

import { signOut } from "firebase/auth";
import { auth } from "./firebase";

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('authToken') || null);
  const [page, setPage] = useState(() => localStorage.getItem('lastPage') || "landing");
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || "light");

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === "light" ? "dark" : "light");
  };

  useEffect(() => {
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  }, [token]);

  useEffect(() => {
    localStorage.setItem('lastPage', page);
  }, [page]);

  const handleLogin = (newToken) => {
    setToken(newToken);
    setPage("profile");
  };

  const handleLogout = () => {
    setToken(null);
    setPage("landing");
    localStorage.removeItem('authToken');
    localStorage.removeItem('lastPage');

    // Clear Firebase session
    signOut(auth).catch(console.error);
  };

  return (
    <div className="app">
      <Navbar
        loggedIn={!!token}
        setPage={setPage}
        currentPage={page}
        onLogout={handleLogout}
        theme={theme}
        toggleTheme={toggleTheme}
      />

      <main>
        {page === "landing" && <Landing setPage={setPage} />}
        {page === "login" && <Login onLogin={handleLogin} setPage={setPage} />}
        {page === "signup" && <Signup onLogin={handleLogin} />}
        {page === "profile" && token && <Profile token={token} />}
        {page === "scholarships" && token && <Scholarships token={token} />}
        {page === "reminders" && <Reminders />}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '2rem',
        marginTop: '4rem',
        color: '#64748b',
        fontSize: '0.9rem',
        borderTop: '1px solid #e2e8f0'
      }}>
        <p>FundMyStudy - Empowering Rural Students Through Education</p>
        <p>© 2026 FundMyStudy. All rights reserved. | Made with ❤️ for India</p>
        <p style={{ fontSize: '0.8rem', marginTop: '1rem' }}>
          Contact: support@fundmystudy.in | Helpline: 1800-XXX-XXXX
        </p>
      </footer>
    </div>
  );
}

export default App;