import React from 'react';

export default function HomePage({ onStartClick }) {
  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-badge">
          <span>✨</span> DiagnoWise Clinical AI SaaS Platform v2.0
        </div>
        
        <h1 className="hero-title">
          DiagnoWise <br />
          <span>AI-Powered Health Risk Assessment & Disease Prediction</span>
        </h1>

        <p className="hero-subtitle">
          Analyze symptoms using machine learning and receive intelligent disease predictions, confidence scores, specialist recommendations, and health guidance.
        </p>

        <div style={{ display: 'flex', gap: '1.25rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button className="btn btn-primary" onClick={onStartClick} style={{ padding: '1rem 2.25rem', fontSize: '1.1rem' }}>
            Start Diagnosis →
          </button>
          <a href="#how-it-works" className="btn btn-secondary" style={{ padding: '1rem 2.25rem', fontSize: '1.1rem' }}>
            Learn More
          </a>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="stats-grid">
        <div className="stat-card">
          <div className="stat-number">132</div>
          <div className="stat-label">Supported Symptoms</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">41</div>
          <div className="stat-label">Target Diagnoses</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">4</div>
          <div className="stat-label">ML Ensemble Models</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">97.6%+</div>
          <div className="stat-label">Benchmark Test Accuracy</div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" style={{ margin: '4rem 0' }}>
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <h2 style={{ fontSize: '2.2rem', fontWeight: '800' }}>How DiagnoWise Works</h2>
          <p style={{ color: 'var(--text-muted)' }}>3 simple steps to receive intelligent medical risk assessment</p>
        </div>

        <div className="workflow-grid">
          <div className="step-card">
            <div className="step-number">1</div>
            <h3 style={{ fontSize: '1.3rem', fontWeight: '700', marginBottom: '0.6rem' }}>Select Symptoms</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Choose observed symptoms from our 132-symptom catalog or use instant autocomplete search.
            </p>
          </div>

          <div className="step-card">
            <div className="step-number">2</div>
            <h3 style={{ fontSize: '1.3rem', fontWeight: '700', marginBottom: '0.6rem' }}>AI Machine Learning Analysis</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Our Random Forest & Gradient Boost ensemble models process binary feature vectors in real time.
            </p>
          </div>

          <div className="step-card">
            <div className="step-number">3</div>
            <h3 style={{ fontSize: '1.3rem', fontWeight: '700', marginBottom: '0.6rem' }}>Receive Diagnostic Report</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              View confidence scores, top-3 differential predictions, specialist doctor advice, and export PDF reports.
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ margin: '4rem 0' }}>
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <h2 style={{ fontSize: '2.2rem', fontWeight: '800' }}>Platform Capabilities</h2>
          <p style={{ color: 'var(--text-muted)' }}>Advanced clinical AI features engineered for decision support</p>
        </div>

        <div className="grid-3">
          <div className="glass-panel">
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🩺</div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.5rem' }}>Disease Prediction</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Predicts primary prognosis from multi-symptom feature matrices with high clinical precision.
            </p>
          </div>

          <div className="glass-panel">
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>📊</div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.5rem' }}>Top 3 Diagnoses</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Calculates calibrated probability distributions to display top 3 differential disease rankings.
            </p>
          </div>

          <div className="glass-panel">
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🎯</div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.5rem' }}>Confidence Analysis</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Visualizes confidence percentages and risk indicator badges (Low, Medium, High Risk).
            </p>
          </div>

          <div className="glass-panel">
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>👨‍⚕️</div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.5rem' }}>Specialist Recommendation</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Directly maps predicted conditions to qualified medical specialists for targeted care.
            </p>
          </div>

          <div className="glass-panel">
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>📄</div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.5rem' }}>Health Reports (PDF)</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Generates downloadable clinical health reports formatted for printing and doctor consultations.
            </p>
          </div>

          <div className="glass-panel">
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🧠</div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.5rem' }}>Symptom Intelligence</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Domain-categorized symptom catalog supporting instant fuzzy autocomplete search.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="glass-panel" style={{ textTransform: 'center', padding: '3.5rem 2rem', background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(99, 102, 241, 0.15))', textAlign: 'center' }}>
        <h2 style={{ fontSize: '2.4rem', fontWeight: '800', marginBottom: '1rem' }}>Ready to Assess Your Health Risk?</h2>
        <p style={{ color: 'var(--text-muted)', max-width: '600px', margin: '0 auto 2rem', fontSize: '1.1rem' }}>
          Select your symptoms now and run instant machine learning inference.
        </p>
        <button className="btn btn-primary" onClick={onStartClick} style={{ padding: '1rem 2.5rem', fontSize: '1.1rem' }}>
          Launch DiagnoWise Symptom Checker →
        </button>
      </section>
    </div>
  );
}
