import React, { useState, useEffect } from 'react';

const STEPS = [
  "Analyzing Selected Patient Symptoms...",
  "Running ML Ensemble Models (Random Forest / Gradient Boost)...",
  "Calculating Calibrated Confidence Scores & Top 3 Ranking...",
  "Enriching Clinical Precautions & Specialist Guidance..."
];

export default function LoadingModal({ isOpen }) {
  const [currentStepIdx, setCurrentStepIdx] = useState(0);

  useEffect(() => {
    if (!isOpen) {
      setCurrentStepIdx(0);
      return;
    }

    const interval = setInterval(() => {
      setCurrentStepIdx(prev => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 450);

    return () => clearInterval(interval);
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="loading-overlay">
      <div className="loading-modal">
        <div className="pulse-spinner">
          🩺
        </div>
        
        <h3 style={{ fontSize: '1.4rem', fontWeight: '800', marginBottom: '0.5rem', color: 'var(--text-main)' }}>
          DiagnoWise AI Engine
        </h3>
        
        <p style={{ color: 'var(--primary)', fontWeight: '700', fontSize: '0.95rem', minHeight: '28px', marginBottom: '1.5rem' }}>
          {STEPS[currentStepIdx]}
        </p>

        <div className="progress-bar-bg" style={{ height: '8px' }}>
          <div 
            className="progress-bar-fill"
            style={{ width: `${((currentStepIdx + 1) / STEPS.length) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
}
