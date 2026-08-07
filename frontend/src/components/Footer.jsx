import React from 'react';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div>
          <h4 style={{ color: '#f8fafc', marginBottom: '0.4rem', fontWeight: '700' }}>DiagnoWise AI Diagnostic Engine</h4>
          <p>B.Tech Final Year Project & Placement Portfolio Project</p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <p style={{ color: '#64748b', fontSize: '0.85rem' }}>
            Powered by FastAPI, Random Forest ML, & React (Vite)
          </p>
          <p style={{ color: '#475569', fontSize: '0.8rem', marginTop: '0.2rem' }}>
            © {new Date().getFullYear()} DiagnoWise Health Tech. Educational & Diagnostic Support Tool.
          </p>
        </div>
      </div>
    </footer>
  );
}
