import { useEffect, useState } from "react";
import "../styles/navbar.css";

const NavLink = ({ page, label, setPage, currentPage }) => (
  <span
    onClick={() => setPage(page)}
    className={currentPage === page ? 'active' : ''}
  >
    {label}
  </span>
);

export default function Navbar({ loggedIn, setPage, currentPage, onLogout, theme, toggleTheme }) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);



  const handleLogout = () => {
    if (onLogout) {
      onLogout();
    } else {
      // Fallback if onLogout is not provided
      setPage("landing");
      window.location.reload();
    }
  };

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="logo" onClick={() => setPage("landing")} style={{ cursor: 'pointer' }}>
        FundMyStudy
      </div>
      <div className="links">
        <NavLink page="landing" label="Home" setPage={setPage} currentPage={currentPage} />
        {!loggedIn ? (
          <>
            <NavLink page="login" label="Login" setPage={setPage} currentPage={currentPage} />
            <span
              onClick={() => setPage("signup")}
              className={currentPage === "signup" ? 'active' : ''}
              style={{
                background: '#4f46e5',
                color: 'white',
                padding: '0.5rem 1rem',
                borderRadius: '8px',
                marginLeft: '0.5rem',
                cursor: 'pointer'
              }}
            >
              Sign Up
            </span>
          </>
        ) : (
          <>
            <NavLink page="profile" label="Profile" setPage={setPage} currentPage={currentPage} />
            <NavLink page="scholarships" label="Scholarships" setPage={setPage} currentPage={currentPage} />
            <span
              onClick={handleLogout}
              style={{
                color: '#ef4444',
                background: 'rgba(239, 68, 68, 0.1)',
                padding: '0.5rem 1rem',
                borderRadius: '10px'
              }}
            >
              Logout
            </span>
          </>
        )}
        <NavLink page="reminders" label="Reminders" setPage={setPage} currentPage={currentPage} />

        <div
          onClick={toggleTheme}
          style={{
            position: 'relative',
            width: '56px',
            height: '28px',
            background: theme === 'dark' ? '#334155' : '#e2e8f0',
            borderRadius: '50px',
            marginLeft: '1rem',
            cursor: 'pointer',
            transition: 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)',
            display: 'flex',
            alignItems: 'center',
            padding: '2px',
            boxShadow: 'inner 0 2px 4px rgba(0,0,0,0.1)'
          }}
          title="Toggle Theme"
        >
          <div style={{
            width: '24px',
            height: '24px',
            background: 'white',
            borderRadius: '50%',
            transform: theme === 'dark' ? 'translateX(28px)' : 'translateX(0)',
            transition: 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
          }}>
            {theme === 'dark' ? '🌙' : '☀️'}
          </div>
        </div>
      </div>
    </nav>
  );
}