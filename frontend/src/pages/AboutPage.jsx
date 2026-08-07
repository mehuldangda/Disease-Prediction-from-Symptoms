import React from 'react';

export default function AboutPage() {
  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <div className="hero-badge">
          <span>⚙️</span> Technical Specifications & Architecture
        </div>
        <h1 style={{ fontSize: '2.5rem', fontWeight: '800' }}>DiagnoWise Platform Engineering</h1>
        <p style={{ color: 'var(--text-muted)' }}>
          Detailed breakdown of machine learning algorithms, API backend design, and system architecture.
        </p>
      </div>

      {/* Model Performance Metrics Table */}
      <div className="glass-panel" style={{ marginBottom: '2rem' }}>
        <h3 style={{ fontSize: '1.35rem', fontWeight: '800', marginBottom: '1.25rem', color: 'var(--primary)' }}>
          📈 ML Classifier Evaluation Benchmark
        </h3>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.95rem' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--border-color)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '0.85rem 1rem' }}>Algorithm Model</th>
                <th style={{ padding: '0.85rem 1rem' }}>Validation Accuracy</th>
                <th style={{ padding: '0.85rem 1rem' }}>Test Accuracy</th>
                <th style={{ padding: '0.85rem 1rem' }}>Precision</th>
                <th style={{ padding: '0.85rem 1rem' }}>Recall</th>
                <th style={{ padding: '0.85rem 1rem' }}>F1-Score</th>
              </tr>
            </thead>
            <tbody>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.85rem 1rem', fontWeight: '700', color: 'var(--primary)' }}>Random Forest (Default)</td>
                <td style={{ padding: '0.85rem 1rem' }}>100.00%</td>
                <td style={{ padding: '0.85rem 1rem', fontWeight: '700' }}>97.62%</td>
                <td style={{ padding: '0.85rem 1rem' }}>0.98</td>
                <td style={{ padding: '0.85rem 1rem' }}>0.98</td>
                <td style={{ padding: '0.85rem 1rem' }}>0.98</td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.85rem 1rem', fontWeight: '700' }}>Decision Tree</td>
                <td style={{ padding: '0.85rem 1rem' }}>100.00%</td>
                <td style={{ padding: '0.85rem 1rem', fontWeight: '700' }}>100.00%</td>
                <td style={{ padding: '0.85rem 1rem' }}>1.00</td>
                <td style={{ padding: '0.85rem 1rem' }}>1.00</td>
                <td style={{ padding: '0.85rem 1rem' }}>1.00</td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.85rem 1rem', fontWeight: '700' }}>Multinomial Naive Bayes</td>
                <td style={{ padding: '0.85rem 1rem' }}>100.00%</td>
                <td style={{ padding: '0.85rem 1rem', fontWeight: '700' }}>100.00%</td>
                <td style={{ padding: '0.85rem 1rem' }}>1.00</td>
                <td style={{ padding: '0.85rem 1rem' }}>1.00</td>
                <td style={{ padding: '0.85rem 1rem' }}>1.00</td>
              </tr>
              <tr>
                <td style={{ padding: '0.85rem 1rem', fontWeight: '700' }}>Gradient Boosting</td>
                <td style={{ padding: '0.85rem 1rem' }}>100.00%</td>
                <td style={{ padding: '0.85rem 1rem', fontWeight: '700' }}>97.62%</td>
                <td style={{ padding: '0.85rem 1rem' }}>0.98</td>
                <td style={{ padding: '0.85rem 1rem' }}>0.98</td>
                <td style={{ padding: '0.85rem 1rem' }}>0.98</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid-2">
        <div className="glass-panel">
          <h3 style={{ fontSize: '1.3rem', fontWeight: '800', marginBottom: '1rem', color: 'var(--primary)' }}>
            🎓 Academic & Portfolio Context
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginBottom: '1rem' }}>
            DiagnoWise was engineered as a B.Tech Final Year Capstone Project and Placement Portfolio Application. It demonstrates real-world software engineering, machine learning inference, REST API architecture, and UI/UX design.
          </p>
          <div style={{ background: 'var(--bg-input)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
            <p style={{ fontSize: '0.85rem' }}><strong>Target Prognoses:</strong> 41 Unique Diseases</p>
            <p style={{ fontSize: '0.85rem' }}><strong>Symptom Feature Space:</strong> 132 Binary Medical Attributes</p>
            <p style={{ fontSize: '0.85rem' }}><strong>Clinical Knowledge Base:</strong> 41 Profiles with 4-step Precautions & Specialist Doctors</p>
          </div>
        </div>

        <div className="glass-panel">
          <h3 style={{ fontSize: '1.3rem', fontWeight: '800', marginBottom: '1rem', color: 'var(--indigo)' }}>
            🛠️ Technology Stack
          </h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.6rem', marginBottom: '1.25rem' }}>
            {['FastAPI', 'Python 3.10+', 'Scikit-Learn', 'React 18', 'Vite', 'Vanilla CSS', 'Pydantic v2', 'Joblib', 'Pandas', 'Docker'].map(tech => (
              <span key={tech} style={{ background: 'var(--primary-light)', border: '1px solid var(--border-highlight)', color: 'var(--text-main)', padding: '0.35rem 0.85rem', borderRadius: '6px', fontSize: '0.85rem', fontWeight: '700' }}>
                {tech}
              </span>
            ))}
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Decoupled architecture utilizing an asynchronous FastAPI backend for vector prediction and a responsive React client interface.
          </p>
        </div>
      </div>
    </div>
  );
}
