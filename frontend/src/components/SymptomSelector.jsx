import React, { useState, useMemo } from 'react';

export default function SymptomSelector({ 
  symptomsList = [], 
  categories = [], 
  selectedSymptoms = [], 
  onToggleSymptom, 
  onClearAll,
  onPredict, 
  isLoading,
  selectedModel,
  setSelectedModel
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');

  const filteredSymptoms = useMemo(() => {
    return symptomsList.filter(symptom => {
      const q = searchQuery.toLowerCase().trim();
      const matchesSearch = !q || 
                            symptom.label.toLowerCase().includes(q) ||
                            symptom.key.toLowerCase().includes(q) ||
                            symptom.category.toLowerCase().includes(q);
      const matchesCategory = activeCategory === 'All' || symptom.category === activeCategory;
      return matchesSearch && matchesCategory;
    });
  }, [symptomsList, searchQuery, activeCategory]);

  return (
    <div className="glass-panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: '800' }}>Patient Symptom Intelligence</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
            Select all present symptoms to run AI diagnostic inference.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '700' }}>ML Engine:</label>
          <select 
            value={selectedModel} 
            onChange={(e) => setSelectedModel(e.target.value)}
            style={{
              background: 'var(--bg-input)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-main)',
              padding: '0.5rem 0.9rem',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.9rem',
              outline: 'none',
              fontWeight: '600'
            }}
          >
            <option value="random_forest">Random Forest Classifier (Default)</option>
            <option value="gradient_boost">Gradient Boosting</option>
            <option value="decision_tree">Decision Tree</option>
            <option value="mnb">Multinomial Naive Bayes</option>
          </select>
        </div>
      </div>

      {/* Persistent Selected Symptoms Panel */}
      <div className="selected-tray" style={{ marginBottom: '1.75rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h4 style={{ fontWeight: '800', fontSize: '1.05rem', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span>📋</span> Selected Symptoms ({selectedSymptoms.length})
            </h4>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.75rem' }}>
              {selectedSymptoms.length === 0 ? (
                <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                  No symptoms selected yet. Click symptom chips below or use search.
                </span>
              ) : (
                selectedSymptoms.map(key => {
                  const item = symptomsList.find(s => s.key === key);
                  const label = item ? item.label : key;
                  return (
                    <span key={key} className="selected-badge-item">
                      ✓ {label}
                      <button 
                        onClick={() => onToggleSymptom(key)}
                        title="Remove symptom"
                      >
                        ✕
                      </button>
                    </span>
                  );
                })
              )}
            </div>
          </div>

          {selectedSymptoms.length > 0 && (
            <button 
              className="btn-danger-outline"
              onClick={onClearAll}
              disabled={isLoading}
            >
              Clear All Symptoms ({selectedSymptoms.length})
            </button>
          )}
        </div>
      </div>

      {/* Search Box */}
      <div className="search-box">
        <span className="search-icon-left">🔍</span>
        <input 
          type="text"
          className="search-input"
          placeholder="Search symptoms by keyword (e.g. fever, skin rash, headache, joint pain)..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        {searchQuery && (
          <button 
            onClick={() => setSearchQuery('')}
            style={{
              position: 'absolute',
              right: '1.2rem',
              top: '50%',
              transform: 'translateY(-50%)',
              background: 'none',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              fontSize: '1rem'
            }}
          >
            ✕
          </button>
        )}
      </div>

      {/* Category Pills */}
      <div className="category-tabs">
        <button 
          className={`category-tab ${activeCategory === 'All' ? 'active' : ''}`}
          onClick={() => setActiveCategory('All')}
        >
          All Symptoms ({symptomsList.length})
        </button>
        {categories.map(cat => {
          const count = symptomsList.filter(s => s.category === cat).length;
          return (
            <button 
              key={cat}
              className={`category-tab ${activeCategory === cat ? 'active' : ''}`}
              onClick={() => setActiveCategory(cat)}
            >
              {cat} ({count})
            </button>
          );
        })}
      </div>

      {/* Symptom Chips Catalog */}
      <div className="chips-container">
        {filteredSymptoms.length === 0 ? (
          <div style={{ padding: '2.5rem', textAlign: 'center', width: '100%', color: 'var(--text-muted)' }}>
            No matching symptoms found for "{searchQuery}".
          </div>
        ) : (
          filteredSymptoms.map(item => {
            const isSelected = selectedSymptoms.includes(item.key);
            return (
              <div 
                key={item.key}
                className={`symptom-chip ${isSelected ? 'selected' : ''}`}
                onClick={() => onToggleSymptom(item.key)}
              >
                {isSelected ? '✓ ' : '+ '} {item.label}
              </div>
            );
          })
        )}
      </div>

      {/* Action Footer */}
      <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end' }}>
        <button 
          className="btn btn-primary"
          onClick={onPredict}
          disabled={selectedSymptoms.length === 0 || isLoading}
          style={{
            opacity: (selectedSymptoms.length === 0 || isLoading) ? 0.6 : 1,
            cursor: (selectedSymptoms.length === 0 || isLoading) ? 'not-allowed' : 'pointer',
            padding: '1rem 2.25rem',
            fontSize: '1.05rem'
          }}
        >
          {isLoading ? 'Analyzing Symptoms...' : `Run AI Health Risk Assessment (${selectedSymptoms.length} Selected) →`}
        </button>
      </div>
    </div>
  );
}
