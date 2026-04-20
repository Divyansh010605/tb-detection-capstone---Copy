import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <a href="/upload" className="navbar__logo" id="nav-logo">
        🫁 <span>TB</span>-Detect
      </a>
      <div className="navbar__links">
        {user ? (
          <>
            <NavLink
              to="/upload"
              id="nav-upload"
              className={({ isActive }) => `btn btn-ghost${isActive ? ' btn-primary' : ''}`}
            >
              Upload
            </NavLink>
            <span className="navbar__user" aria-label="Current user">
              👤 {user.username}
            </span>
            <button id="nav-logout" className="btn btn-ghost" onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <NavLink to="/login" id="nav-login" className="btn btn-primary">
            Sign In
          </NavLink>
        )}
      </div>
    </nav>
  );
}
