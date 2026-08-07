import React from 'react';
import SymptomSelector from '../components/SymptomSelector';

export default function PredictPage({
  symptomsList,
  categories,
  selectedSymptoms,
  onToggleSymptom,
  onClearAll,
  onPredict,
  isLoading,
  error,
  selectedModel,
  setSelectedModel,
  history = [],
  onLoadHistoryItem,
  onClearHistory
}) {
  return (
    <div style={{ animation: 'fadeIn 0.3s ease' }}>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.4rem', fontWeight: '800' }}>Symptom Checker & Clinical Assessment</h1>
        <p style={{ color: 'var(--text-muted)' }}>
          Select patient symptoms to evaluate health risk and predict probable diagnoses.
        </p>
      </div>

      {error && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.15)',
          border: '1px solid rgba(239, 68, 68, 0.4)',
          color: '#fca5a5',
          padding: '1rem 1.5rem',
          borderRadius: 'var(--radius-md)',
          marginBottom: '1.5rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <span>⚠️ {error}</span>
        </div>
      )}

      <SymptomSelector 
        symptomsList={symptomsList}
        categories={categories}
        selectedSymptoms={selectedSymptoms}
        onToggleSymptom={onToggleSymptom}
        onClearAll={onClearAll}
        onPredict={onPredict}
        isLoading={isLoading}
        selectedModel={selectedModel}
        setSelectedModel={setSelectedModel}
      />

      {/* Local Prediction History Drawer */}
      {history.length > 0 && (
        <div className="glass-panel" style={{ marginTop: '2.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span>🕒</span> Recent Predictions History ({history.length})
            </h3>
            <button className="btn-danger-outline" onClick={onClearHistory}>
              Clear History
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
            {history.map(item => (
              <div 
                key={item.id}
                onClick={() => onLoadHistoryItem(item)}
                style={{
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border-color)',
                  padding: '1.1rem',
                  borderRadius: 'var(--radius-sm)',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--border-highlight)'}
                onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--border-color)'}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                  <strong style={{ color: 'var(--text-main)', fontSize: '1rem' }}>{item.primary_prediction}</strong>
                  <span style={{ color: 'var(--primary)', fontWeight: '800', fontSize: '0.9rem' }}>{item.confidence_percentage}%</span>
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {new Date(item.timestamp).toLocaleDateString()} • {item.matched_symptoms_count} Symptoms • {item.recommended_doctor}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
