import React from 'react';
import { generateHealthReportPDF } from '../utils/pdfGenerator';

export default function ResultCard({ result, onReset }) {
  if (!result) return null;

  const primary = result.primary_prediction;
  const confidence = result.confidence_percentage;
  const top3 = result.top_3_predictions || [];

  // Determine Risk Category Badge
  const severityStr = (result.severity || 'Moderate').toLowerCase();
  let riskClass = 'risk-medium';
  let riskLabel = 'Medium Risk';

  if (severityStr.includes('high') || severityStr.includes('critical')) {
    riskClass = 'risk-high';
    riskLabel = 'High Risk';
  } else if (severityStr.includes('low')) {
    riskClass = 'risk-low';
    riskLabel = 'Low Risk';
  }

  return (
    <div style={{ animation: 'fadeIn 0.35s ease' }}>
      {/* Action Bar Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <button className="btn btn-secondary" onClick={onReset}>
          ← Test Different Symptoms
        </button>

        <button 
          className="btn btn-primary"
          onClick={() => generateHealthReportPDF(result)}
          style={{ background: 'linear-gradient(135deg, #10b981, #06b6d4)' }}
        >
          📄 Download Clinical PDF Health Report
        </button>
      </div>

      {/* Main Prediction Highlight Card */}
      <div className="glass-panel" style={{ textAlign: 'center', position: 'relative', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
          <span className="hero-badge" style={{ marginBottom: 0 }}>
            <span>🩺</span> Diagnostic Inference Result
          </span>
          <span className={`risk-badge ${riskClass}`}>
            ● {riskLabel}
          </span>
        </div>

        <h1 style={{ fontSize: '2.8rem', fontWeight: '800', margin: '0.4rem 0' }}>
          {primary}
        </h1>

        <div className="confidence-gauge" style={{ '--percentage': confidence }}>
          <div className="gauge-inner">
            <span style={{ fontSize: '1.5rem', color: 'var(--primary)' }}>{confidence}%</span>
            <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Confidence</span>
          </div>
        </div>

        <p style={{ color: 'var(--text-muted)', maxWidth: '720px', margin: '0 auto 1.5rem', fontSize: '1.1rem' }}>
          {result.description}
        </p>

        <div style={{ display: 'inline-flex', gap: '1.5rem', background: 'var(--bg-input)', padding: '0.8rem 1.75rem', borderRadius: '999px', border: '1px solid var(--border-color)', flexWrap: 'wrap', justifyContent: 'center' }}>
          <div>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Clinical Severity: </span>
            <strong style={{ color: 'var(--text-main)' }}>{result.severity}</strong>
          </div>
          <div style={{ borderLeft: '1px solid var(--border-color)', paddingLeft: '1.5rem' }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Evaluated Symptoms: </span>
            <strong style={{ color: 'var(--primary)' }}>{result.matched_symptoms_count}</strong>
          </div>
          <div style={{ borderLeft: '1px solid var(--border-color)', paddingLeft: '1.5rem' }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>ML Classifier: </span>
            <strong style={{ color: 'var(--indigo)', textTransform: 'capitalize' }}>{result.model_used.replace('_', ' ')}</strong>
          </div>
        </div>
      </div>

      <div className="grid-2">
        {/* Top 3 Differential Diagnoses */}
        <div className="glass-panel">
          <h3 style={{ fontSize: '1.3rem', fontWeight: '800', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>📊</span> Top 3 Differential Diagnoses
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            {top3.map((item, idx) => (
              <div key={idx} style={{ background: 'var(--bg-input)', padding: '1.1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                  <span style={{ fontWeight: '700', color: idx === 0 ? 'var(--primary)' : 'var(--text-main)', fontSize: '1rem' }}>
                    #{idx + 1} {item.disease}
                  </span>
                  <span style={{ fontWeight: '800', color: idx === 0 ? 'var(--primary)' : 'var(--text-muted)' }}>
                    {item.probability}%
                  </span>
                </div>
                <div className="progress-bar-bg">
                  <div 
                    className="progress-bar-fill"
                    style={{ 
                      width: `${item.probability}%`,
                      background: idx === 0 
                        ? 'linear-gradient(90deg, #10b981, #06b6d4)' 
                        : 'linear-gradient(90deg, #64748b, #94a3b8)'
                    }}
                  />
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.6rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  <span>Specialist: <strong style={{ color: 'var(--text-main)' }}>{item.doctor}</strong></span>
                  <span>Confidence: <strong>{item.confidence_score}</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Actionable Precautions & Specialist Recommendation */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h3 style={{ fontSize: '1.3rem', fontWeight: '800', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span>🛡️</span> Health Guidance & Precautions
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {result.precautions.map((step, idx) => (
                <div key={idx} style={{ background: 'var(--bg-input)', borderLeft: '4px solid var(--primary)', padding: '0.9rem 1.1rem', borderRadius: '0 var(--radius-sm) var(--radius-sm) 0', fontSize: '0.95rem' }}>
                  <strong style={{ color: 'var(--primary)', marginRight: '0.4rem' }}>Step {idx + 1}:</strong> {step}
                </div>
              ))}
            </div>
          </div>

          <div style={{ marginTop: '2rem' }}>
            <div style={{ background: 'var(--primary-light)', border: '1px solid var(--border-highlight)', padding: '1.5rem', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
              <div style={{ fontSize: '2.5rem' }}>👨‍⚕️</div>
              <div>
                <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '1px', color: 'var(--primary)', fontWeight: '800' }}>
                  Recommended Medical Specialist
                </span>
                <h4 style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--text-main)', marginTop: '0.2rem' }}>
                  {result.recommended_doctor}
                </h4>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                  Schedule a clinical consultation with a certified {result.recommended_doctor} for comprehensive diagnosis.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
