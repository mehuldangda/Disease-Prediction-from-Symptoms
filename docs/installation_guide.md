# Installation & Operations Guide - DiagnoWise AI

## Prerequisites
- **Operating System:** Windows 10/11, macOS, or Linux
- **Python:** Version 3.10+ (Python 3.10, 3.11, or 3.12 recommended)
- **Web Browser:** Modern web browser (Chrome, Edge, Firefox, Safari)

---

## Quick Start (1-Click Launch on Windows)
Double-click `run_app.bat` or run in PowerShell / Command Prompt:
```cmd
.\run_app.bat
```
This automatically verifies dependencies, validates trained ML models, and launches the application in your default browser at `http://localhost:8501`.

---

## Manual Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/Disease-Prediction-from-Symptoms.git
cd Disease-Prediction-from-Symptoms
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Train ML Classifiers (Optional if pre-trained binaries exist)
```bash
python -m ml.train
```

### Step 4: Launch DiagnoWise Streamlit Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.
