import React from 'react';
import ResultCard from '../components/ResultCard';

export default function ResultPage({ result, onReset }) {
  if (!result) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 1rem' }}>
        <h2>No prediction results found.</h2>
        <p style={{ color: 'var(--text-muted)', margin: '1rem 0' }}>Please select symptoms on the prediction page first.</p>
        <button className="btn btn-primary" onClick={onReset}>
          ← Go to Symptom Checker
        </button>
      </div>
    );
  }

  return (
    <div>
      <ResultCard result={result} onReset={onReset} />
    </div>
  );
}
