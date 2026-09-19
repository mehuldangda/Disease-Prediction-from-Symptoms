# System Design Document - DiagnoWise AI Disease Prediction System

## 1. Requirements

### Functional Requirements
- **FR1 (Symptom Lookup):** Retrieve a structured catalog of 132 medical symptoms categorized by domain with instant search and autocomplete support.
- **FR2 (Multi-Symptom Selection):** Allow interactive selection of multiple binary symptoms with visual state management.
- **FR3 (ML Inference):** Infer disease prognosis directly using trained scikit-learn ensemble and probabilistic models.
- **FR4 (Differential Diagnosis):** Return top-3 ranked disease predictions with calibrated probability distributions and confidence percentages.
- **FR5 (Clinical Guidance):** Provide disease descriptions, 4-step precautionary measures, and specialist medical doctor recommendations.
- **FR6 (Report Generation):** Generate and download customized clinical PDF health reports using FPDF2.

### Non-Functional Requirements
- **NFR1 (Performance):** Zero-HTTP latency; sub-50ms in-memory ML inference utilizing `@st.cache_resource`.
- **NFR2 (Reliability):** Graceful exception handling, input validation, and automatic model loader fallback.
- **NFR3 (Maintainability):** Clean modular Python architecture separating ML logic (`ml/`), utilities (`utils/`), and UI presentation (`app.py`).
- **NFR4 (Usability):** Modern glassmorphism UI with Dark/Light theme toggle, responsive grid layouts, and mobile/desktop support.

---

## 2. Component Architecture

### Streamlit Application (`app.py`)
- Single-command reactive web application.
- Direct invocation of Python ML pipeline (`DiseasePredictor`).
- Session state management for selected symptoms, active category filters, model selection, prediction history, and active views.

### ML Pipeline (`ml/`)
- `DataLoader`: Loads dataset CSVs, extracts 132 symptom features, formats labels, and assigns clinical domain tags.
- `DiseasePredictor`: Constructs 132-dimensional binary feature vector, runs classifier `predict_proba()`, sorts top 3 predictions, and maps clinical metadata.
- `disease_db.py`: Clinical knowledge base containing descriptions, severity ratings, 4-step precautions, and specialist doctor recommendations for all 41 target diseases.
- `train.py`: Model training suite for Random Forest, Decision Tree, Multinomial Naive Bayes, and Gradient Boosting.

### Utility Services (`utils/`)
- `streamlit_pdf.py`: Formatted clinical PDF generator using FPDF2 for exporting printable diagnostic summaries.

---

## 3. Data Directory & Model Storage
- `dataset/training_data.csv`: 4,920 records x 133 columns
- `dataset/test_data.csv`: 42 records x 133 columns
- `saved_model/*.joblib`: Serialized classifier binaries (Random Forest, Gradient Boosting, Decision Tree, Multinomial Naive Bayes)
- `saved_model/model_metadata.json`: Feature column names & target classes
