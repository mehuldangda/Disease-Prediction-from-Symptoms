import React from 'react';

export default function Navbar({ currentPage, setCurrentPage, theme, toggleTheme }) {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <a 
          href="#home" 
          className="brand-logo"
          onClick={(e) => { e.preventDefault(); setCurrentPage('home'); }}
        >
          <div className="brand-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M19 3H5c-1.1 0-1.99.9-1.99 2L3 19c0 1.1.89 2 1.99 2H19c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-1 11h-4v4h-4v-4H6v-4h4V6h4v4h4v4z"/>
            </svg>
          </div>
          Diagno<span style={{ color: 'var(--primary)', fontWeight: '400', fontSize: '1.2rem', marginLeft: '2px' }}>Wise</span>
        </a>

        <ul className="nav-links">
          <li>
            <button 
              className={`nav-link ${currentPage === 'home' ? 'active' : ''}`}
              onClick={() => setCurrentPage('home')}
            >
              Home
            </button>
          </li>
          <li>
            <button 
              className={`nav-link ${currentPage === 'predict' ? 'active' : ''}`}
              onClick={() => setCurrentPage('predict')}
            >
              Symptom Checker
            </button>
          </li>
          <li>
            <button 
              className={`nav-link ${currentPage === 'about' ? 'active' : ''}`}
              onClick={() => setCurrentPage('about')}
            >
              Architecture & Tech
            </button>
          </li>

          <li>
            <button className="theme-toggle-btn" onClick={toggleTheme} title="Toggle Dark/Light Mode">
              {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
            </button>
          </li>

          <li>
            <button 
              className="btn btn-primary"
              onClick={() => setCurrentPage('predict')}
            >
              Start Diagnosis →
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}
