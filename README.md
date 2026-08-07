# 🩺 DiagnoWise AI - Disease Prediction from Symptoms

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-4.4-646CFF.svg)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2%2B-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end Machine Learning web application and clinical decision-support system that predicts probable medical conditions from multi-symptom inputs. Engineered as a production-ready **B.Tech Final Year Project** and **Placement Portfolio Project**.

---

## 🌟 Key Features

- 🧬 **130+ Symptom Index:** Searchable catalog grouped into clinical domains (Dermatological, Respiratory, Gastrointestinal, Musculoskeletal, Neurological, General).
- 📊 **Top-3 Differential Diagnoses:** Probability rankings and confidence percentages computed via `predict_proba()`.
- 👨‍⚕️ **Specialist Doctor Recommendations:** Automatic mapping of predicted diagnoses to relevant medical specialists (Dermatologist, Pulmonologist, Gastroenterologist, Neurologist, Cardiologist).
- 🛡️ **Actionable 4-Step Precautions:** Immediate precautionary measures and self-care steps for all 41 target diseases.
- ⚡ **High Performance Backend:** Asynchronous FastAPI web server with sub-100ms inference execution.
- 🎨 **Modern Health-Tech UI:** Glassmorphism design system in Vanilla CSS with mobile/desktop responsiveness.
- 🚀 **Multi-Cloud Ready:** Pre-configured deployment files for Render, Railway, Hugging Face Spaces, and Vercel.

---

## 📁 System Architecture & Directory Layout

```
Disease-Prediction-from-Symptoms/
├── backend/                  # FastAPI Production Server
│   ├── app/
│   │   ├── config/          # Settings & CORS config
│   │   ├── models/          # Pydantic v2 schemas
│   │   ├── routes/          # API endpoints (/api/predict, /api/symptoms, /api/health)
│   │   ├── services/        # Prediction engine service wrapper
│   │   ├── utils/           # Structured loggers & exception handlers
│   │   ├── static/          # Served single-page web app
│   │   └── main.py          # FastAPI application entry point
│   ├── run.py               # Backend server runner
│   └── requirements.txt     # Pinned Python package dependencies
├── ml/                       # Machine Learning Pipeline
│   ├── dataset/             # Raw dataset CSVs (4,920 records x 132 features)
│   ├── saved_model/         # Serialized .joblib model binaries
│   ├── data_loader.py       # Data loading & cleaning module
│   ├── train.py             # Multi-model training script (RF, DT, MNB, GradientBoost)
│   ├── predictor.py         # Inference engine with top-3 probability ranking
│   ├── evaluate.py          # Model metrics & evaluation generator
│   └── disease_db.py        # Clinical knowledge base (descriptions, precautions, doctors)
├── frontend/                 # Modern React + Vite Web Application
│   ├── src/
│   │   ├── components/      # Navbar, Footer, SymptomSelector, ResultCard
│   │   ├── pages/           # Home, Predict, Result, About
│   │   ├── services/        # API client helpers
│   │   └── styles/          # Vanilla CSS design tokens & animations
│   ├── index.html           # HTML5 entry point
│   ├── package.json         # React dependencies
│   └── vite.config.js       # Vite proxy config
├── deployment/               # Cloud Deployment Configs
│   ├── render.yaml          # Render service config
│   ├── railway.json         # Railway deployment config
│   ├── Dockerfile           # Docker container / Hugging Face Spaces
│   └── vercel.json          # Vercel SPA deployment config
├── docs/                     # Academic FYP Documentation
│   ├── project_report.md    # Complete Final Year Project Report
│   ├── architecture_diagram.mermaid
│   ├── data_flow_diagram.mermaid
│   ├── system_design.md
│   ├── installation_guide.md
│   └── user_manual.md
├── run_app.bat               # 1-Click Windows Launcher Script
├── .env.example              # Environment variables template
├── main.py                   # Root FastAPI entry point
└── requirements.txt         # Root dependencies
```

---

## ⚡ Quick Start & Local Execution

### 1-Click Launcher (Windows)

Simply run `run_app.bat` in Command Prompt or double-click:

```cmd
.\run_app.bat
```

### Manual Execution Commands

#### Backend (FastAPI Server)

```bash
pip install -r requirements.txt
python main.py
```

*Server runs on `http://localhost:8000`. Interactive API Documentation available at `http://localhost:8000/docs`.*

#### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

*Frontend runs on `http://localhost:5173`.*

---

## 📈 Model Performance Metrics

| Classifier Model                  | Validation Accuracy |   Test Accuracy   | Precision | Recall | F1-Score |
| :-------------------------------- | :-----------------: | :---------------: | :-------: | :----: | :------: |
| **Random Forest**           |       100.00%       | **97.62%** |   0.98   |  0.98  |   0.98   |
| **Decision Tree**           |       100.00%       | **100.00%** |   1.00   |  1.00  |   1.00   |
| **Multinomial Naive Bayes** |       100.00%       | **100.00%** |   1.00   |  1.00  |   1.00   |
| **Gradient Boosting**       |       100.00%       | **97.62%** |   0.98   |  0.98  |   0.98   |

---

## 🌐 Deployment Commands & Configurations

- **Render:** Deploy backend using `deployment/render.yaml`
- **Railway:** Deploy service using `deployment/railway.json`
- **Hugging Face Spaces:** Deploy container using `deployment/Dockerfile`
- **Vercel:** Deploy frontend using `deployment/vercel.json`

---

## 📄 License & Academic Note

This project is developed for educational and research purposes as a B.Tech Final Year Project. Always consult a certified healthcare professional for medical advice.
