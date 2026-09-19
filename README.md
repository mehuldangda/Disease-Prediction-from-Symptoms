# 🩺 DiagnoWise AI - Disease Prediction from Symptoms

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2%2B-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end Machine Learning clinical decision-support web application that predicts probable medical conditions from multi-symptom inputs. Built with **Streamlit** and **Scikit-Learn**, engineered as a production-ready **B.Tech Final Year Capstone Project** and **Placement Portfolio Project**.

---

## 🌟 Key Features

- 🧬 **130+ Symptom Index:** Searchable catalog categorized into clinical domains (*Dermatological & Skin*, *Respiratory & ENT*, *Gastrointestinal*, *Musculoskeletal*, *General & Systemic*, *Urinary & Renal*, *Neurological & Mental Health*).
- 📊 **Top-3 Differential Diagnoses:** Calibrated probability distributions and confidence percentages computed via `predict_proba()`.
- 👨‍⚕️ **Specialist Doctor Recommendations:** Automatic clinical mapping of predicted diagnoses to relevant medical specialists (Dermatologist, Pulmonologist, Gastroenterologist, Neurologist, Cardiologist, etc.).
- 🛡️ **Actionable 4-Step Precautions:** Immediate precautionary measures and self-care steps for all 41 target diseases.
- 📄 **Printable Clinical PDF Reports:** Formatted, downloadable medical diagnostic reports with confidence scores, precautions, and specialist details generated on the fly via FPDF2.
- 🎨 **Modern Glassmorphism UI:** Health-tech interface with Dark/Light mode toggle, animated gauges, interactive chips, and responsive grid layouts.
- ⚡ **Zero-Latency In-Memory ML:** Single-layer Python architecture with `@st.cache_resource` for sub-50ms inference.
- 🚀 **Streamlit Cloud Ready:** Instant 1-click cloud deployment on Streamlit Community Cloud, Hugging Face Spaces, Render, and Railway.

---

## 📁 System Architecture & Directory Layout

```
Disease-Prediction-from-Symptoms/
├── app.py                      # Main Streamlit application entry point
├── streamlit_app.py            # Multi-entrypoint wrapper for Streamlit Cloud
├── ml/                         # Machine Learning Pipeline
│   ├── dataset/                # Dataset CSVs (4,920 records x 132 features)
│   ├── saved_model/            # Serialized .joblib model binaries & metadata
│   ├── data_loader.py          # Data loading, cleaning & symptom metadata
│   ├── train.py                # Multi-model training script (RF, DT, MNB, GradientBoost)
│   ├── predictor.py            # Inference engine with top-3 probability ranking
│   ├── evaluate.py             # Model metrics & evaluation generator
│   └── disease_db.py           # Clinical knowledge base (41 profiles, precautions, doctors)
├── utils/                      # Helper Utilities
│   └── streamlit_pdf.py        # PDF health report generator (FPDF2)
├── deployment/                 # Cloud Deployment Configs
│   ├── Dockerfile              # Container config (Hugging Face Spaces / Cloud)
│   ├── render.yaml             # Render deployment config
│   └── railway.json            # Railway deployment config
├── docs/                       # Academic FYP Documentation
│   ├── project_report.md       # Complete Final Year Project Report
│   ├── architecture_diagram.mermaid
│   ├── data_flow_diagram.mermaid
│   ├── system_design.md
│   ├── installation_guide.md
│   └── user_manual.md
├── run_app.bat                 # 1-Click Windows Launcher Script
├── requirements.txt            # Streamlit & ML dependencies
├── config.yaml                 # Configuration parameters
└── README.md                   # Project documentation
```

---

## ⚡ Quick Start & Local Execution

### 1-Click Launcher (Windows)

Simply run `run_app.bat` in Command Prompt or double-click:

```cmd
.\run_app.bat
```

### Manual Execution

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch Streamlit Application
streamlit run app.py
```

*App will automatically open at `http://localhost:8501`.*

---

## 📈 Model Performance Metrics

| Classifier Model                  | Validation Accuracy |   Test Accuracy   | Precision | Recall | F1-Score |
| :-------------------------------- | :-----------------: | :---------------: | :-------: | :----: | :------: |
| **Random Forest** (Default)       |       100.00%       | **97.62%** |   0.98   |  0.98  |   0.98   |
| **Decision Tree**                 |       100.00%       | **100.00%** |   1.00   |  1.00  |   1.00   |
| **Multinomial Naive Bayes**       |       100.00%       | **100.00%** |   1.00   |  1.00  |   1.00   |
| **Gradient Boosting**             |       100.00%       | **97.62%** |   0.98   |  0.98  |   0.98   |

---

## 🌐 Cloud Deployment

- **Streamlit Community Cloud:** Deploy directly from your GitHub repository by pointing to `app.py`.
- **Hugging Face Spaces:** Deploy using `deployment/Dockerfile` (exposes port 7860).
- **Render:** Deploy web service using `deployment/render.yaml`.
- **Railway:** Deploy service using `deployment/railway.json`.

---

## 📄 License & Academic Note

This project is developed for educational and research purposes as a B.Tech Final Year Capstone Project. Always consult a certified healthcare professional for medical advice.
