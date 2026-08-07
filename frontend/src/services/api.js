const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function fetchSymptoms() {
  const response = await fetch(`${API_BASE_URL}/symptoms`);
  if (!response.ok) {
    throw new Error('Failed to load symptom list from server.');
  }
  return await response.json();
}

export async function predictDisease(symptomsList, modelName = 'random_forest') {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      symptoms: symptomsList,
      model_name: modelName,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Disease prediction failed.');
  }

  return await response.json();
}

export async function fetchHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return await response.json();
}

export async function fetchDiseases() {
  const response = await fetch(`${API_BASE_URL}/diseases`);
  if (!response.ok) {
    throw new Error('Failed to load disease catalog.');
  }
  return await response.json();
}
