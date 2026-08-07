# Installation & Operations Guide

## Prerequisites
- **Operating System:** Windows 10/11, macOS, or Linux
- **Python:** Version 3.10+ (Python 3.10, 3.11, or 3.12 recommended)
- **Node.js (Optional):** Version 18+ (required for React Vite dev server)

---

## Quick Start (1-Click Launch on Windows)
Double-click `run_app.bat` or run in PowerShell:
```cmd
.\run_app.bat
```
This automatically installs dependencies, verifies/trains ML models, and launches the server at `http://localhost:8000`.

---

## Manual Installation Steps

### Step 1: Clone & Navigate to Project
```bash
git clone https://github.com/your-username/Disease-Prediction-from-Symptoms.git
cd Disease-Prediction-from-Symptoms
```

### Step 2: Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Train ML Classifiers (Optional if pre-trained binaries exist)
```bash
python -m ml.train
```

### Step 4: Launch FastAPI Server
```bash
python main.py
```
or
```bash
uvicorn backend.app.main:app --reload --port 8000
```

### Step 5: Launch React Frontend (Optional when Node.js is installed)
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.
