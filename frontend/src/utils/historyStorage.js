/**
 * LocalStorage prediction history helper
 */

const HISTORY_KEY = 'diagnowise_prediction_history';

export function savePredictionToHistory(result, symptoms) {
  try {
    const history = getPredictionHistory();
    const newItem = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      primary_prediction: result.primary_prediction,
      confidence_percentage: result.confidence_percentage,
      severity: result.severity,
      recommended_doctor: result.recommended_doctor,
      matched_symptoms_count: result.matched_symptoms_count,
      symptoms: symptoms,
      result: result
    };
    
    // Keep last 15 reports
    const updated = [newItem, ...history].slice(0, 15);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(updated));
    return updated;
  } catch (err) {
    console.error('Failed to save to history:', err);
    return [];
  }
}

export function getPredictionHistory() {
  try {
    const data = localStorage.getItem(HISTORY_KEY);
    return data ? JSON.parse(data) : [];
  } catch (err) {
    console.error('Failed to read history:', err);
    return [];
  }
}

export function clearPredictionHistory() {
  try {
    localStorage.removeItem(HISTORY_KEY);
    return [];
  } catch (err) {
    console.error('Failed to clear history:', err);
    return [];
  }
}
