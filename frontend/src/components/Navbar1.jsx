import { useEffect, useState } from "react";
import "../styles/navbar.css";

export default function Navbar({ loggedIn, setPage, currentPage, onLogout }) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const NavLink = ({ page, label }) => (
    <span 
      onClick={() => setPage(page)}
      className={currentPage === page ? 'active' : ''}
    >
      {label}
    </span>
  );

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
        <NavLink page="landing" label="Home" />
        {!loggedIn ? (
          <NavLink page="login" label="Login" />
        ) : (
          <>
            <NavLink page="profile" label="Profile" />
            <NavLink page="scholarships" label="Scholarships" />
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
        <NavLink page="reminders" label="Reminders" />
      </div>
    </nav>
  );
}