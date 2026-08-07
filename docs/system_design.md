# System Design Document - Disease Prediction System

## 1. Requirements

### Functional Requirements
- **FR1 (Symptom Lookup):** Retrieve a structured catalog of 130+ medical symptoms categorized by domain with search support.
- **FR2 (Multi-Symptom Selection):** Allow selection of multiple binary symptoms.
- **FR3 (ML Inference):** Infer disease prognosis using trained scikit-learn models.
- **FR4 (Differential Diagnosis):** Return top-3 ranked disease predictions with confidence percentages.
- **FR5 (Clinical Guidance):** Provide descriptions, 4-step precautionary steps, and specialist medical doctor recommendations.

### Non-Functional Requirements
- **NFR1 (Performance):** Latency under 100ms for prediction requests.
- **NFR2 (Reliability):** 99.9% uptime with graceful exception handling and fallback models.
- **NFR3 (Maintainability):** Modular code structure separating API routes, ML pipeline, and React components.
- **NFR4 (Usability):** Responsive glassmorphism interface supporting mobile and desktop viewports.

---

## 2. API Endpoints Specification

### `GET /api/health`
- **Description:** Health check status.
- **Response:** `{ "status": "healthy", "app_name": "Disease Prediction System", "version": "2.0.0", "model_loaded": true }`

### `GET /api/symptoms`
- **Description:** Returns list of 132 symptoms grouped by domain.
- **Response:** `{ "total_symptoms": 132, "categories": [...], "symptoms": [...] }`

### `POST /api/predict`
- **Request Body:** `{ "symptoms": ["itching", "skin_rash"], "model_name": "random_forest" }`
- **Response Body:**
```json
{
  "primary_prediction": "Fungal infection",
  "confidence_percentage": 60.0,
  "confidence_score": 0.6,
  "severity": "Low to Moderate",
  "recommended_doctor": "Dermatologist",
  "description": "A skin disease caused by a fungus...",
  "precautions": [
    "Keep the affected area clean and dry",
    "Use antifungal creams as prescribed",
    "Avoid sharing personal items like towels and clothing",
    "Wear breathable cotton clothing"
  ],
  "top_3_predictions": [ ... ],
  "matched_symptoms_count": 2,
  "model_used": "random_forest"
}
```

---

## 3. Data Directory & Model Storage
- `dataset/training_data.csv`: 4,920 records x 133 columns
- `dataset/test_data.csv`: 42 records x 133 columns
- `saved_model/random_forest.joblib`: Serialized Random Forest classifier binary
- `saved_model/model_metadata.json`: Feature column names & target classes
