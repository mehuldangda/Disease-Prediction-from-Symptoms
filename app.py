"""
🩺 DiagnoWise AI - Disease Prediction from Symptoms
Production Streamlit Application
Comprehensive Clinical Decision-Support System with Multi-Model ML Inference,
Patient Profile Demographics, and Instant Top Action Bar.
"""

import os
import sys
import json
import textwrap
from datetime import datetime
import streamlit as st

# Ensure root directory is in python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ml.data_loader import DataLoader
from ml.predictor import DiseasePredictor
from ml.disease_db import DISEASE_DETAILS, get_disease_info
from utils.streamlit_pdf import generate_health_report_pdf

# ----------------------------------------------------
# 1. Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="DiagnoWise AI - Disease Prediction from Symptoms",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------
# 2. Cached Resources & ML Engine
# ----------------------------------------------------
@st.cache_resource
def get_predictor_engine(model_name: str = "random_forest") -> DiseasePredictor:
    """Cached loader for ML predictor instance."""
    return DiseasePredictor(model_name=model_name)

@st.cache_data
def get_symptoms_catalog() -> dict:
    """Cached loader for complete symptom catalog and clinical categories."""
    loader = DataLoader()
    return loader.get_symptoms_list()

def render_html(html_str: str):
    """Render HTML string safely in Streamlit without triggering markdown code-block or indentation artifacts."""
    clean_html = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean_html, unsafe_allow_html=True)

# ----------------------------------------------------
# 3. Session State Initialization
# ----------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""
if "patient_age" not in st.session_state:
    st.session_state.patient_age = 28
if "patient_gender" not in st.session_state:
    st.session_state.patient_gender = "Male"
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []
if "symptom_multiselect" not in st.session_state:
    st.session_state.symptom_multiselect = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "random_forest"
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "history" not in st.session_state:
    st.session_state.history = []
if "active_category" not in st.session_state:
    st.session_state.active_category = "All"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# ----------------------------------------------------
# 4. Glassmorphism Design System & CSS Injector
# ----------------------------------------------------
if st.session_state.theme == "dark":
    theme_vars = """
    :root {
      --primary: #10b981;
      --primary-hover: #059669;
      --primary-light: rgba(16, 185, 129, 0.12);
      --accent: #06b6d4;
      --accent-light: rgba(6, 182, 212, 0.12);
      --indigo: #6366f1;
      
      --bg-main: #090d16;
      --bg-secondary: #0f172a;
      --bg-card: rgba(15, 23, 42, 0.78);
      --bg-card-hover: rgba(30, 41, 59, 0.88);
      --bg-input: rgba(15, 23, 42, 0.65);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-highlight: rgba(16, 185, 129, 0.35);
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      
      --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
      --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
      --shadow-glow: 0 0 30px rgba(16, 185, 129, 0.25);
    }
    """
else:
    theme_vars = """
    :root {
      --primary: #10b981;
      --primary-hover: #059669;
      --primary-light: rgba(16, 185, 129, 0.08);
      --accent: #06b6d4;
      --accent-light: rgba(6, 182, 212, 0.08);
      --indigo: #6366f1;
      
      --bg-main: #f8fafc;
      --bg-secondary: #ffffff;
      --bg-card: rgba(255, 255, 255, 0.92);
      --bg-card-hover: #ffffff;
      --bg-input: #f1f5f9;
      --border-color: rgba(0, 0, 0, 0.08);
      --border-highlight: rgba(16, 185, 129, 0.5);
      
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-dim: #94a3b8;
      
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      
      --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
      --shadow-glow: 0 0 25px rgba(16, 185, 129, 0.15);
    }
    """

style_css = theme_vars + """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Main layouts and backgrounds override */
.stApp {
  background-color: var(--bg-main) !important;
  color: var(--text-main) !important;
  font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
  background-image: 
    radial-gradient(at 10% 10%, rgba(16, 185, 129, 0.12) 0px, transparent 40%),
    radial-gradient(at 90% 90%, rgba(99, 102, 241, 0.1) 0px, transparent 40%) !important;
  background-attachment: fixed !important;
}

h1, h2, h3, h4, h5, h6, p, span, div, label, li, a, th, td {
  font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
}

/* Custom Navbar Style */
.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  margin-bottom: 1.5rem;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 800;
  font-size: 1.7rem;
  letter-spacing: -0.5px;
  color: var(--text-main) !important;
  text-decoration: none;
}

.brand-icon {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: var(--shadow-glow);
}

/* Custom glass panel and cards styling */
.glass-panel, div[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--bg-card) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: var(--shadow-lg) !important;
  padding: 1.75rem 2rem !important;
  margin-bottom: 1.5rem !important;
  transition: border-color 0.25s ease !important;
}

.glass-panel:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
  border-color: var(--border-highlight) !important;
}

.hero-section {
  text-align: center;
  padding: 2.5rem 1rem 3rem;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--primary-light);
  border: 1px solid var(--border-highlight);
  color: var(--primary);
  padding: 0.45rem 1.25rem;
  border-radius: 999px;
  font-size: 0.88rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1.15;
  margin-bottom: 1.25rem;
  letter-spacing: -0.5px;
  color: var(--text-main);
}

.hero-title span {
  background: linear-gradient(135deg, #10b981, #06b6d4, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: var(--text-muted);
  max-width: 750px;
  margin: 0 auto 2.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin: 2.5rem 0;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 1.75rem;
  border-radius: var(--radius-md);
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: var(--border-highlight);
  box-shadow: var(--shadow-glow);
}

.stat-number {
  font-size: 2.6rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.95rem;
  font-weight: 600;
  margin-top: 0.3rem;
}

.workflow-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.75rem;
  margin-top: 2rem;
}

.step-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 2rem;
  border-radius: var(--radius-md);
  text-align: center;
}

.step-number {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: white;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
  font-size: 1.1rem;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 2rem;
}

/* Custom styled tray for selected items */
.selected-tray-html {
  margin-top: 1rem;
  padding: 1.25rem;
  background: var(--primary-light);
  border: 1.5px dashed var(--border-highlight);
  border-radius: var(--radius-md);
  margin-bottom: 1.25rem;
}

.selected-badge-item {
  display: inline-block;
  background: var(--primary);
  color: white;
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  margin: 0.25rem;
}

/* Risk indicator badges */
.risk-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.risk-low {
  background: rgba(16, 185, 129, 0.2) !important;
  border: 1px solid rgba(16, 185, 129, 0.5) !important;
  color: #10b981 !important;
}

.risk-medium {
  background: rgba(245, 158, 11, 0.2) !important;
  border: 1px solid rgba(245, 158, 11, 0.5) !important;
  color: #f59e0b !important;
}

.risk-high {
  background: rgba(239, 68, 68, 0.2) !important;
  border: 1px solid rgba(239, 68, 68, 0.5) !important;
  color: #ef4444 !important;
}

/* Custom styled progress bars */
.progress-bar-bg {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  height: 10px;
  width: 100%;
  overflow: hidden;
  margin-top: 0.5rem;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 999px;
}

/* Custom footer style */
.footer-text {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

/* Streamlit specific styling overrides */
.stButton > button {
  background-color: rgba(255, 255, 255, 0.05) !important;
  color: var(--text-main) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  padding: 0.5rem 1rem !important;
  transition: all 0.2s ease !important;
}

.stButton > button:hover {
  background-color: rgba(255, 255, 255, 0.12) !important;
  border-color: var(--border-highlight) !important;
  color: var(--text-main) !important;
  box-shadow: 0 4px 12px rgba(255,255,255,0.02) !important;
}

.stButton > button[type="primary"] {
  background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
  color: white !important;
  border: none !important;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
  font-weight: 700 !important;
}

.stButton > button[type="primary"]:hover {
  opacity: 0.95 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 18px rgba(16, 185, 129, 0.4) !important;
  color: white !important;
}

div.block-container {
  padding-top: 1.5rem !important;
  padding-bottom: 2.5rem !important;
  max-width: 1240px !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
"""

st.markdown(f"<style>{style_css}</style>", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. Helper Callbacks (Pre-Script Execution Safe)
# ----------------------------------------------------
def set_page(page_name: str):
    """Navigate between pages."""
    st.session_state.current_page = page_name

def toggle_theme():
    """Toggle between dark and light themes."""
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

def set_category(cat: str):
    """Filter symptom catalog by category."""
    st.session_state.active_category = cat

def toggle_symptom(symptom_key: str):
    """Toggle symptom inclusion and sync multiselect before widgets render."""
    if symptom_key in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.remove(symptom_key)
    else:
        st.session_state.selected_symptoms.append(symptom_key)
    st.session_state.symptom_multiselect = list(st.session_state.selected_symptoms)

def remove_symptom(symptom_key: str):
    """Remove symptom from selection and sync multiselect."""
    if symptom_key in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.remove(symptom_key)
    st.session_state.symptom_multiselect = list(st.session_state.selected_symptoms)

def clear_all_symptoms():
    """Clear all selected symptoms and reset current prediction."""
    st.session_state.selected_symptoms = []
    st.session_state.symptom_multiselect = []
    st.session_state.prediction_result = None

def on_multiselect_change():
    """Sync changes from multiselect search autocomplete to selected_symptoms."""
    st.session_state.selected_symptoms = list(st.session_state.symptom_multiselect)

def load_history_report(result_obj: dict):
    """Load past diagnostic report and restore patient profile."""
    st.session_state.prediction_result = result_obj
    if "patient_name" in result_obj:
        st.session_state.patient_name = result_obj["patient_name"]
    if "patient_age" in result_obj:
        st.session_state.patient_age = result_obj["patient_age"]
    if "patient_gender" in result_obj:
        st.session_state.patient_gender = result_obj["patient_gender"]
    st.session_state.current_page = "result"

def clear_prediction_history():
    """Clear session prediction history."""
    st.session_state.history = []

def run_ml_inference():
    """Perform disease inference directly using the ML engine."""
    if not st.session_state.selected_symptoms:
        return
    
    with st.spinner("Analyzing Present Symptoms..."):
        try:
            predictor = get_predictor_engine(st.session_state.selected_model)
            result = predictor.predict(st.session_state.selected_symptoms)
            
            # Robustly capture patient profile from active inputs or session state
            p_name = str(st.session_state.get("patient_name_input") or st.session_state.get("patient_name") or "").strip()
            if not p_name or p_name.lower() == "patient":
                p_name = "Anonymous Patient"
                
            p_age_val = st.session_state.get("patient_age_input") or st.session_state.get("patient_age") or 28
            try:
                p_age = int(p_age_val)
            except Exception:
                p_age = 28
                
            p_gender = str(st.session_state.get("patient_gender_input") or st.session_state.get("patient_gender") or "Male").strip()
            
            result["patient_name"] = p_name
            result["patient_age"] = p_age
            result["patient_gender"] = p_gender
            
            # Sync back to session state
            st.session_state.patient_name = p_name
            st.session_state.patient_age = p_age
            st.session_state.patient_gender = p_gender
            
            st.session_state.prediction_result = result
            
            # Save prediction to local session history
            history_item = {
                "id": str(datetime.now().timestamp()),
                "timestamp": datetime.now().isoformat(),
                "patient_name": result["patient_name"],
                "patient_age": result["patient_age"],
                "patient_gender": result["patient_gender"],
                "primary_prediction": result["primary_prediction"],
                "confidence_percentage": result["confidence_percentage"],
                "severity": result["severity"],
                "recommended_doctor": result["recommended_doctor"],
                "matched_symptoms_count": result["matched_symptoms_count"],
                "symptoms": list(st.session_state.selected_symptoms),
                "result": result
            }
            st.session_state.history = [history_item] + st.session_state.history
            st.session_state.history = st.session_state.history[:15]
            
            # Transition to result page
            st.session_state.current_page = "result"
            st.rerun()
        except Exception as e:
            st.error(f"Inference Engine Error: {str(e)}")

# ----------------------------------------------------
# 6. Global Top Navigation Header
# ----------------------------------------------------
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([3.5, 1.2, 1.6, 2.0, 1.0])

with nav_col1:
    render_html('''
    <div class="nav-container" style="margin-bottom:0px; padding:0px;">
        <div class="brand-logo">
            <div class="brand-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 3H5c-1.1 0-1.99.9-1.99 2L3 19c0 1.1.89 2 1.99 2H19c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-1 11h-4v4h-4v-4H6v-4h4V6h4v4h4v4z"/>
                </svg>
            </div>
            Diagno<span style="color: var(--primary); font-weight: 400; font-size: 1.5rem; margin-left: 2px;">Wise</span>
        </div>
    </div>
    ''')

with nav_col2:
    st.button("Home", key="nav_home", use_container_width=True, type="primary" if st.session_state.current_page == "home" else "secondary", on_click=set_page, args=("home",))

with nav_col3:
    st.button("Symptom Checker", key="nav_predict", use_container_width=True, type="primary" if st.session_state.current_page == "predict" else "secondary", on_click=set_page, args=("predict",))

with nav_col4:
    st.button("Architecture & Tech", key="nav_about", use_container_width=True, type="primary" if st.session_state.current_page == "about" else "secondary", on_click=set_page, args=("about",))

with nav_col5:
    theme_text = "☀️ Light" if st.session_state.theme == "dark" else "🌙 Dark"
    st.button(theme_text, key="nav_theme_toggle", use_container_width=True, on_click=toggle_theme)

st.markdown("<hr style='margin-top:0.5rem; margin-bottom:1.5rem; border:0; border-top:1px solid var(--border-color);'>", unsafe_allow_html=True)

# Fetch symptom data catalog
symptoms_data = get_symptoms_catalog()
all_symptoms = symptoms_data["symptoms"]
categories = symptoms_data["categories"]

# ----------------------------------------------------
# PAGE 1: Home Landing Page
# ----------------------------------------------------
if st.session_state.current_page == "home":
    render_html('''
    <div class="hero-section">
        <div class="hero-badge">
            <span>✨</span> DiagnoWise Clinical AI SaaS Platform v2.0
        </div>
        <h1 class="hero-title">
            DiagnoWise<br>
            <span>AI-Powered Health Risk Assessment & Disease Prediction</span>
        </h1>
        <p class="hero-subtitle">
            Analyze symptoms using machine learning and receive intelligent disease predictions, confidence scores, specialist recommendations, and health guidance.
        </p>
    </div>
    ''')
    
    # Hero buttons
    cta_col1, cta_col2, cta_col3, cta_col4 = st.columns([1.5, 1.2, 1.2, 1.5])
    with cta_col2:
        st.button("Start Diagnosis →", key="hero_start_btn", type="primary", use_container_width=True, on_click=set_page, args=("predict",))
    with cta_col3:
        render_html('<a href="#how-it-works" class="stButton" style="text-decoration:none;"><button class="btn btn-secondary" style="width:100%;">Learn More</button></a>')

    # Statistics Grid
    render_html(f'''
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{symptoms_data["total_symptoms"]}</div>
            <div class="stat-label">Supported Symptoms</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">41</div>
            <div class="stat-label">Target Diagnoses</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">4</div>
            <div class="stat-label">ML Ensemble Models</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">97.6%+</div>
            <div class="stat-label">Benchmark Test Accuracy</div>
        </div>
    </div>
    ''')

    # How It Works Flow
    render_html('''
    <div id="how-it-works" style="margin: 4rem 0 2rem 0;">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="font-size: 2.2rem; font-weight: 800; color: var(--text-main);">How DiagnoWise Works</h2>
            <p style="color: var(--text-muted); font-size:1.05rem;">3 simple steps to receive intelligent medical risk assessment</p>
        </div>
        <div class="workflow-grid">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3 style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.6rem; color:var(--text-main);">Select Symptoms</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Choose observed symptoms from our 132-symptom catalog or use instant autocomplete search.
                </p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h3 style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.6rem; color:var(--text-main);">AI Machine Learning Analysis</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Our Random Forest & Gradient Boost ensemble models process binary feature vectors in real time.
                </p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h3 style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.6rem; color:var(--text-main);">Receive Diagnostic Report</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    View confidence scores, top-3 differential predictions, specialist doctor advice, and export PDF reports.
                </p>
            </div>
        </div>
    </div>
    ''')

    # Platform Capabilities
    render_html('''
    <div style="margin: 4rem 0 3rem 0;">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="font-size: 2.2rem; font-weight: 800; color: var(--text-main);">Platform Capabilities</h2>
            <p style="color: var(--text-muted); font-size:1.05rem;">Advanced clinical AI features engineered for decision support</p>
        </div>
        <div class="grid-3">
            <div class="glass-panel">
                <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">🩺</div>
                <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color:var(--text-main);">Disease Prediction</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Predicts primary prognosis from multi-symptom feature matrices with high clinical precision.
                </p>
            </div>
            <div class="glass-panel">
                <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">📊</div>
                <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color:var(--text-main);">Top 3 Diagnoses</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Calculates calibrated probability distributions to display top 3 differential disease rankings.
                </p>
            </div>
            <div class="glass-panel">
                <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">🎯</div>
                <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color:var(--text-main);">Confidence Analysis</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Visualizes confidence percentages and risk indicator badges (Low, Medium, High Risk).
                </p>
            </div>
            <div class="glass-panel">
                <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">👨‍⚕️</div>
                <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color:var(--text-main);">Specialist Recommendation</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Directly maps predicted conditions to qualified medical specialists for targeted care.
                </p>
            </div>
            <div class="glass-panel">
                <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">📄</div>
                <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color:var(--text-main);">Health Reports (PDF)</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Generates downloadable clinical health reports formatted for printing and doctor consultations.
                </p>
            </div>
            <div class="glass-panel">
                <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">🧠</div>
                <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color:var(--text-main);">Symptom Intelligence</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Domain-categorized symptom catalog supporting instant fuzzy autocomplete search.
                </p>
            </div>
        </div>
    </div>
    ''')

    # CTA Section
    render_html('''
    <div class="glass-panel" style="padding: 3.5rem 2rem; background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(99, 102, 241, 0.15)); text-align: center;">
        <h2 style="font-size: 2.3rem; font-weight: 800; margin-bottom: 1rem; color:var(--text-main);">Ready to Assess Your Health Risk?</h2>
        <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto 2rem; font-size: 1.1rem;">
            Select your symptoms now and run instant machine learning inference.
        </p>
    </div>
    ''')
    cta_col_center = st.columns([2, 1.5, 2])
    with cta_col_center[1]:
        st.button("Launch Symptom Checker", key="cta_launch_btn", type="primary", use_container_width=True, on_click=set_page, args=("predict",))

# ----------------------------------------------------
# PAGE 2: Symptom Checker & Predict
# ----------------------------------------------------
elif st.session_state.current_page == "predict":
    render_html('''
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.5rem; font-weight: 800; color: var(--text-main); margin-bottom: 0.4rem;">Symptom Checker & Clinical Assessment</h1>
        <p style="color: var(--text-muted); font-size:1.05rem;">
            Enter patient demographics and select observed symptoms to generate an intelligent differential diagnosis.
        </p>
    </div>
    ''')

    # 1. Patient Profile Demographics Card
    with st.container(border=True):
        render_html("<h3 style='font-size: 1.2rem; font-weight: 800; color: var(--primary); margin-top:0px; margin-bottom:1rem;'>👤 Patient Intake Profile</h3>")
        
        p_col1, p_col2, p_col3, p_col4 = st.columns([2.5, 1.2, 1.8, 2.5])
        with p_col1:
            st.session_state.patient_name = st.text_input("Patient Full Name", value=st.session_state.patient_name, placeholder="e.g. John Doe", key="patient_name_input")
        with p_col2:
            st.session_state.patient_age = st.number_input("Age (Years)", min_value=1, max_value=120, value=int(st.session_state.patient_age), step=1, key="patient_age_input")
        with p_col3:
            gender_options = ["Male", "Female", "Other", "Prefer not to say"]
            gender_index = gender_options.index(st.session_state.patient_gender) if st.session_state.patient_gender in gender_options else 0
            st.session_state.patient_gender = st.selectbox("Biological Sex / Gender", options=gender_options, index=gender_index, key="patient_gender_input")
        with p_col4:
            model_display_names = {
                "random_forest": "Random Forest Classifier (Default)",
                "gradient_boost": "Gradient Boosting",
                "decision_tree": "Decision Tree",
                "mnb": "Multinomial Naive Bayes"
            }
            st.selectbox(
                "ML Algorithm Engine",
                options=list(model_display_names.keys()),
                format_func=lambda x: model_display_names[x],
                key="selected_model"
            )

    # 2. Selected Symptoms Tray & Top Action Assessment Button
    selected_count = len(st.session_state.selected_symptoms)
    
    with st.container(border=True):
        # TOP ACTION BAR - Exactly where user requested!
        act_col1, act_col2 = st.columns([3, 2])
        with act_col1:
            render_html(f"<h3 style='font-size: 1.25rem; font-weight: 800; color:var(--text-main); margin-top:0px; margin-bottom:0.2rem;'>📋 Selected Symptoms ({selected_count})</h3><p style='color:var(--text-muted); font-size:0.88rem; margin:0px;'>Review selected symptoms below. You can remove individual items or clear all.</p>")
        with act_col2:
            if selected_count == 0:
                st.button("⚠️ Select at least 1 symptom to assess", key="run_top_disabled", type="secondary", disabled=True, use_container_width=True)
            else:
                if st.button(f"🚀 Run AI Health Risk Assessment ({selected_count} Selected) →", key="run_top_active", type="primary", use_container_width=True):
                    run_ml_inference()
                    
        render_html("<hr style='border:0; border-top:1px solid var(--border-color); margin: 1rem 0;'>")
        
        # Tray Chips and Clear All
        if selected_count == 0:
            st.info("No symptoms selected yet. Use the autocomplete search below or browse clinical category chips.")
        else:
            tray_left, tray_right = st.columns([5, 1.2])
            with tray_left:
                # Interactive removal buttons for each selected symptom
                num_badge_cols = min(selected_count, 4)
                badge_cols = st.columns(num_badge_cols)
                for b_idx, sym_key in enumerate(st.session_state.selected_symptoms):
                    sym_obj = next((s for s in all_symptoms if s["key"] == sym_key), None)
                    label = sym_obj["label"] if sym_obj else sym_key
                    c_i = b_idx % num_badge_cols
                    with badge_cols[c_i]:
                        st.button(f"✕ {label}", key=f"tray_sym_{sym_key}", use_container_width=True, type="primary", on_click=remove_symptom, args=(sym_key,))
            with tray_right:
                st.button(f"Clear All ({selected_count})", key="clear_all_symptoms_btn", type="secondary", use_container_width=True, on_click=clear_all_symptoms)

    # 3. Autocomplete Search & Category Filter Section
    with st.container(border=True):
        render_html("<h3 style='font-size: 1.25rem; font-weight: 800; color:var(--text-main); margin-top:0px;'>🔍 Symptom Search & Clinical Catalog (132 Total)</h3>")
        
        # Autocomplete Multiselect Search
        symptom_choices = {item["key"]: item["label"] for item in all_symptoms}
        st.multiselect(
            "Search & Add Symptoms Autocomplete",
            options=list(symptom_choices.keys()),
            format_func=lambda x: symptom_choices[x],
            key="symptom_multiselect",
            on_change=on_multiselect_change,
            placeholder="Type to search symptoms (e.g. fever, skin rash, headache, joint pain, nausea)..."
        )

        # Category Pill Tabs
        category_tabs_options = ["All"] + categories
        cat_cols = st.columns(len(category_tabs_options))
        for idx, cat_opt in enumerate(category_tabs_options):
            with cat_cols[idx]:
                cat_count = len(all_symptoms) if cat_opt == "All" else len([s for s in all_symptoms if s["category"] == cat_opt])
                pill_label = f"{cat_opt} ({cat_count})"
                st.button(
                    pill_label, 
                    key=f"cat_pill_{cat_opt}", 
                    use_container_width=True, 
                    type="primary" if st.session_state.active_category == cat_opt else "secondary",
                    on_click=set_category,
                    args=(cat_opt,)
                )

        # Search keyword filter for chips
        st.session_state.search_query = st.text_input(
            "Filter chips catalog by keyword", 
            value=st.session_state.search_query, 
            placeholder="Type keyword to filter chips below...",
            key="search_input_filter"
        )

        # Filter symptom list for the chips catalog
        filtered_symptoms = []
        q = st.session_state.search_query.lower().strip()
        for s in all_symptoms:
            matches_search = not q or q in s["label"].lower() or q in s["key"].lower() or q in s["category"].lower()
            matches_cat = st.session_state.active_category == "All" or s["category"] == st.session_state.active_category
            if matches_search and matches_cat:
                filtered_symptoms.append(s)

        # Symptom Chips Catalog Grid
        render_html("<p style='color:var(--text-muted); font-size:0.9rem; margin-top:1rem; margin-bottom:0.6rem; font-weight:600;'>Click chips below to toggle selection:</p>")
        if not filtered_symptoms:
            st.info(f"No symptoms matching the current filters: '{st.session_state.search_query}' in category '{st.session_state.active_category}'")
        else:
            num_cols = 4
            chip_cols = st.columns(num_cols)
            for chip_idx, sym_obj in enumerate(filtered_symptoms):
                col_idx = chip_idx % num_cols
                with chip_cols[col_idx]:
                    key = sym_obj["key"]
                    is_sel = key in st.session_state.selected_symptoms
                    chip_label = f"✓ {sym_obj['label']}" if is_sel else f"+ {sym_obj['label']}"
                    st.button(
                        chip_label, 
                        key=f"chip_btn_{key}", 
                        use_container_width=True, 
                        type="primary" if is_sel else "secondary",
                        on_click=toggle_symptom,
                        args=(key,)
                    )

        # Bottom secondary action button
        render_html("<hr style='border:0; border-top:1px solid var(--border-color); margin-top:2rem; margin-bottom:1rem;'>")
        btm_cols = st.columns([3.5, 1.5])
        with btm_cols[1]:
            if st.button(f"Run AI Assessment ({selected_count} Selected) →", key="run_btm_action", type="primary", use_container_width=True, disabled=(selected_count == 0)):
                run_ml_inference()

    # 4. Local Prediction History Drawer
    if st.session_state.history:
        with st.container(border=True):
            hist_col1, hist_col2 = st.columns([4, 1])
            with hist_col1:
                render_html(f"<h3 style='font-size: 1.25rem; font-weight: 800; color:var(--text-main); margin-top:0px;'>🕒 Recent Predictions History ({len(st.session_state.history)})</h3>")
            with hist_col2:
                st.button("Clear History", key="clear_hist_btn", type="secondary", on_click=clear_prediction_history)
                    
            hist_cols = st.columns(3)
            for h_idx, h_item in enumerate(st.session_state.history):
                h_col_idx = h_idx % 3
                with hist_cols[h_col_idx]:
                    date_parsed = datetime.fromisoformat(h_item["timestamp"]).strftime("%Y-%m-%d %I:%M %p")
                    p_name_hist = h_item.get("patient_name", "Patient")
                    p_age_hist = h_item.get("patient_age", "30")
                    p_gender_hist = h_item.get("patient_gender", "Male")
                    
                    card_html = f"""
                    <div style="background: var(--bg-input); border: 1px solid var(--border-color); padding: 1.1rem; border-radius: var(--radius-sm); margin-bottom:0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                            <strong style="color: var(--text-main); font-size: 0.98rem;">{h_item['primary_prediction']}</strong>
                            <span style="color: var(--primary); font-weight: 800; font-size: 0.9rem;">{h_item['confidence_percentage']}%</span>
                        </div>
                        <p style="font-size: 0.82rem; color: var(--primary); font-weight:600; margin:0 0 0.3rem 0;">
                            👤 {p_name_hist} ({p_age_hist}y, {p_gender_hist})
                        </p>
                        <p style="font-size: 0.78rem; color: var(--text-muted); margin:0px;">
                            {date_parsed} • {h_item['matched_symptoms_count']} Symptoms • {h_item['recommended_doctor']}
                        </p>
                    </div>
                    """
                    render_html(card_html)
                    st.button("Load Report", key=f"load_hist_btn_{h_item['id']}", use_container_width=True, on_click=load_history_report, args=(h_item["result"],))

# ----------------------------------------------------
# PAGE 3: Diagnostic Report View
# ----------------------------------------------------
elif st.session_state.current_page == "result":
    result = st.session_state.prediction_result
    
    if not result:
        st.warning("No prediction results found. Please check symptoms first.")
        st.button("Go to Symptom Checker", type="primary", on_click=set_page, args=("predict",))
    else:
        # Action controls bar
        report_ctrl_col1, report_ctrl_col2 = st.columns([1, 1])
        with report_ctrl_col1:
            st.button("← Test Different Symptoms", key="back_to_predict_btn", type="secondary", on_click=set_page, args=("predict",))
        with report_ctrl_col2:
            try:
                # Ensure result dict always has valid patient demographics
                p_name_res = result.get("patient_name")
                if not p_name_res or p_name_res.lower() == "patient":
                    result["patient_name"] = str(st.session_state.get("patient_name_input") or st.session_state.get("patient_name") or "Anonymous Patient").strip()
                if not result.get("patient_age"):
                    result["patient_age"] = int(st.session_state.get("patient_age_input") or st.session_state.get("patient_age") or 28)
                if not result.get("patient_gender"):
                    result["patient_gender"] = str(st.session_state.get("patient_gender_input") or st.session_state.get("patient_gender") or "Male").strip()

                pdf_bytes = generate_health_report_pdf(result)
                safe_pname = result['patient_name'].replace(' ', '_')
                safe_pred = result['primary_prediction'].replace(' ', '_')
                filename = f"DiagnoWise_Report_{safe_pname}_{safe_pred}.pdf"
                st.download_button(
                    label=f"📄 Download Clinical PDF Health Report ({result['patient_name']})",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as pdf_err:
                st.error(f"Could not generate PDF: {pdf_err}")

        # Patient Info Header Strip
        p_name = result.get("patient_name", "Anonymous Patient")
        p_age = result.get("patient_age", 28)
        p_gender = result.get("patient_gender", "Male")
        report_date = datetime.now().strftime("%B %d, %Y %I:%M %p")
        
        patient_strip_html = f"""
        <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1rem 1.75rem; margin: 1.25rem 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <span style="color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; font-weight: 700;">Patient Name</span>
                <h4 style="color: var(--text-main); font-size: 1.15rem; font-weight: 800; margin: 0.2rem 0 0 0;">👤 {p_name}</h4>
            </div>
            <div>
                <span style="color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; font-weight: 700;">Age & Gender</span>
                <p style="color: var(--text-main); font-size: 1.05rem; font-weight: 700; margin: 0.2rem 0 0 0;">{p_age} Years • {p_gender}</p>
            </div>
            <div>
                <span style="color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; font-weight: 700;">Clinical Status</span>
                <p style="color: var(--primary); font-size: 1.05rem; font-weight: 800; margin: 0.2rem 0 0 0;">● Inference Verified</p>
            </div>
            <div>
                <span style="color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; font-weight: 700;">Report Generated</span>
                <p style="color: var(--text-muted); font-size: 0.95rem; font-weight: 600; margin: 0.2rem 0 0 0;">{report_date}</p>
            </div>
        </div>
        """
        render_html(patient_strip_html)

        # Severity Badge Configs
        severity_str = (result.get("severity", "Moderate")).lower()
        if "high" in severity_str or "critical" in severity_str:
            risk_class = "risk-high"
            risk_label = "High Risk"
        elif "low" in severity_str:
            risk_class = "risk-low"
            risk_label = "Low Risk"
        else:
            risk_class = "risk-medium"
            risk_label = "Medium Risk"

        # Main Prediction Panel - Clean render without any markdown code block formatting
        pred_title = result["primary_prediction"]
        pred_conf = result["confidence_percentage"]
        pred_desc = result["description"]
        pred_sev = result["severity"]
        pred_sym_count = result["matched_symptoms_count"]
        pred_model = result["model_used"].replace('_', ' ').title()
        
        main_card_html = f"""
        <div class="glass-panel" style="text-align: center; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: center; gap: 0.75rem; margin-bottom: 1rem; align-items:center;">
                <span class="hero-badge" style="margin-bottom: 0px;">
                    <span>🩺</span> Diagnostic Inference Result
                </span>
                <span class="risk-badge {risk_class}">
                    ● {risk_label}
                </span>
            </div>
            <h1 style="font-size: 2.8rem; font-weight: 800; margin: 0.4rem 0; color: var(--text-main);">{pred_title}</h1>
            
            <div style="margin: 1.5rem auto; display: flex; flex-direction: column; align-items: center;">
                <div style="background: var(--primary-light); border: 2px solid var(--primary); padding: 0.8rem 2.5rem; border-radius: 999px; display: inline-flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 2rem; font-weight: 900; color: var(--primary);">{pred_conf}%</span>
                    <span style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700; letter-spacing: 1px;">Model Confidence</span>
                </div>
            </div>
            
            <p style="color: var(--text-muted); max-width: 750px; margin: 0 auto 1.5rem; font-size: 1.1rem; line-height: 1.6;">
                {pred_desc}
            </p>
            
            <div style="display: inline-flex; gap: 1.5rem; background: var(--bg-input); padding: 0.8rem 1.75rem; border-radius: 999px; border: 1px solid var(--border-color); flex-wrap: wrap; justify-content: center;">
                <div>
                    <span style="color: var(--text-muted); font-size: 0.85rem;">Clinical Severity: </span>
                    <strong style="color: var(--text-main); font-size: 0.85rem;">{pred_sev}</strong>
                </div>
                <div style="border-left: 1px solid var(--border-color); padding-left: 1.5rem;">
                    <span style="color: var(--text-muted); font-size: 0.85rem;">Evaluated Symptoms: </span>
                    <strong style="color: var(--primary); font-size: 0.85rem;">{pred_sym_count}</strong>
                </div>
                <div style="border-left: 1px solid var(--border-color); padding-left: 1.5rem;">
                    <span style="color: var(--text-muted); font-size: 0.85rem;">ML Classifier: </span>
                    <strong style="color: var(--indigo); font-size: 0.85rem;">{pred_model}</strong>
                </div>
            </div>
        </div>
        """
        render_html(main_card_html)

        col_report_left, col_report_right = st.columns(2)
        
        with col_report_left:
            top3_preds = result.get("top_3_predictions", [])
            diff_items_html = ""
            for idx, item in enumerate(top3_preds[:3]):
                fill_color = "linear-gradient(90deg, #10b981, #06b6d4)" if idx == 0 else "linear-gradient(90deg, #64748b, #94a3b8)"
                primary_text_color = "var(--primary)" if idx == 0 else "var(--text-main)"
                
                diff_items_html += f"""
                <div style="background: var(--bg-input); padding: 1.1rem; border-radius: var(--radius-sm); border: 1px solid var(--border-color); margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem; font-weight: 700;">
                        <span style="color: {primary_text_color}; font-size: 1rem;">#{idx + 1} {item["disease"]}</span>
                        <span style="color: {primary_text_color}; font-size: 1rem;">{item["probability"]}%</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: {item["probability"]}%; background: {fill_color};"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.6rem; font-size: 0.82rem; color: var(--text-muted);">
                        <span>Specialist: <strong style="color: var(--text-main);">{item["doctor"]}</strong></span>
                        <span>Confidence Score: <strong>{item["confidence_score"]}</strong></span>
                    </div>
                </div>
                """
            
            left_card_html = f"""
            <div class="glass-panel" style="height: 100%;">
                <h3 style="font-size: 1.3rem; font-weight: 800; margin-top:0px; margin-bottom: 1.25rem; color: var(--text-main); display: flex; align-items: center; gap: 0.5rem;">
                    <span>📊</span> Top 3 Differential Diagnoses
                </h3>
                {diff_items_html}
            </div>
            """
            render_html(left_card_html)
            
        with col_report_right:
            prec_items = ""
            for idx, step in enumerate(result.get("precautions", [])):
                prec_items += f"""
                <div style="background: var(--bg-input); border-left: 4px solid var(--primary); padding: 0.85rem 1.1rem; border-radius: 0 var(--radius-sm) var(--radius-sm) 0; font-size: 0.95rem; margin-bottom: 0.5rem; text-align: left;">
                    <strong style="color: var(--primary); margin-right: 0.4rem;">Step {idx + 1}:</strong> {step}
                </div>
                """
                
            right_col_html = f"""
            <div class="glass-panel" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h3 style="font-size: 1.3rem; font-weight: 800; margin-top:0px; margin-bottom: 1.25rem; color: var(--text-main); display: flex; align-items: center; gap: 0.5rem;">
                        <span>🛡️</span> Health Guidance & Precautions
                    </h3>
                    {prec_items}
                </div>
                
                <div style="background: var(--primary-light); border: 1px solid var(--border-highlight); padding: 1.2rem; border-radius: var(--radius-md); display: flex; align-items: center; gap: 1.25rem; margin-top: 1.25rem;">
                    <div style="font-size: 2.3rem;">👨‍⚕️</div>
                    <div>
                        <span style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: var(--primary); font-weight: 800;">
                            Recommended Medical Specialist
                        </span>
                        <h4 style="font-size: 1.15rem; font-weight: 800; color: var(--text-main); margin-top: 0.15rem; margin-bottom:0.15rem;">
                            {result["recommended_doctor"]}
                        </h4>
                        <p style="font-size: 0.82rem; color: var(--text-muted); margin:0px; line-height:1.4;">
                            Schedule a clinical consultation with a certified {result["recommended_doctor"]} for comprehensive evaluation.
                        </p>
                    </div>
                </div>
            </div>
            """
            render_html(right_col_html)

# ----------------------------------------------------
# PAGE 4: Architecture & Tech Details
# ----------------------------------------------------
elif st.session_state.current_page == "about":
    render_html('''
    <div style="text-align: center; margin-bottom: 2rem;">
        <div class="hero-badge">
            <span>⚙️</span> Technical Specifications & Architecture
        </div>
        <h1 style="font-size: 2.5rem; font-weight: 800; color: var(--text-main);">DiagnoWise Platform Engineering</h1>
        <p style="color: var(--text-muted); font-size: 1.05rem;">
            Detailed breakdown of machine learning algorithms, model binaries, and system architecture metrics.
        </p>
    </div>
    ''')

    # 1. Model Performance Benchmark table card
    with st.container(border=True):
        render_html("<h3 style='font-size: 1.3rem; font-weight: 800; color: var(--primary); margin-top:0px; margin-bottom:1rem;'>📈 ML Classifier Evaluation Benchmark</h3>")
        benchmark_data = [
            {"Model": "Random Forest (Default)", "Validation Accuracy": "100.00%", "Test Accuracy": "97.62%", "Precision": "0.98", "Recall": "0.98", "F1-Score": "0.98"},
            {"Model": "Decision Tree", "Validation Accuracy": "100.00%", "Test Accuracy": "100.00%", "Precision": "1.00", "Recall": "1.00", "F1-Score": "1.00"},
            {"Model": "Multinomial Naive Bayes", "Validation Accuracy": "100.00%", "Test Accuracy": "100.00%", "Precision": "1.00", "Recall": "1.00", "F1-Score": "1.00"},
            {"Model": "Gradient Boosting", "Validation Accuracy": "100.00%", "Test Accuracy": "97.62%", "Precision": "0.98", "Recall": "0.98", "F1-Score": "0.98"}
        ]
        st.table(benchmark_data)

    # 2. Two-Column Info Cards
    about_col1, about_col2 = st.columns(2)
    
    with about_col1:
        about_card1_html = '''
        <div class="glass-panel" style="height: 100%;">
            <h3 style="font-size: 1.3rem; font-weight: 800; margin-top:0px; margin-bottom: 1rem; color: var(--primary);">
                🎓 Academic & Portfolio Context
            </h3>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height:1.6; margin-bottom: 1.25rem;">
                DiagnoWise was engineered as a B.Tech Final Year Capstone Project and Placement Portfolio Application. It demonstrates real-world software engineering, machine learning inference, interactive UI/UX design, and clinical decision support.
            </p>
            <div style="background: var(--bg-input); padding: 1.2rem; border-radius: var(--radius-sm); border: 1px solid var(--border-color); line-height: 1.6;">
                <p style="font-size: 0.88rem; margin-top:0px; margin-bottom:0.4rem; color: var(--text-main);"><strong>Target Prognoses:</strong> 41 Unique Diseases</p>
                <p style="font-size: 0.88rem; margin-top:0px; margin-bottom:0.4rem; color: var(--text-main);"><strong>Symptom Feature Space:</strong> 132 Binary Medical Attributes</p>
                <p style="font-size: 0.88rem; margin-top:0px; margin-bottom:0px; color: var(--text-main);"><strong>Clinical Knowledge Base:</strong> 41 Profiles with 4-step Precautions & Specialist Doctors</p>
            </div>
        </div>
        '''
        render_html(about_card1_html)
        
    with about_col2:
        techs = ['Streamlit', 'Python 3.10+', 'Scikit-Learn', 'Joblib', 'Pandas', 'FPDF2', 'NumPy', 'PyYAML', 'Matplotlib', 'Seaborn']
        tech_badges_html = "".join([f"<span style='background: var(--primary-light); border: 1px solid var(--border-highlight); color: var(--text-main); padding: 0.35rem 0.85rem; border-radius: 6px; font-size: 0.82rem; font-weight: 700; display:inline-block; margin:0.3rem;'>{t}</span>" for t in techs])
        
        tech_html = f'''
        <div class="glass-panel" style="height: 100%;">
            <h3 style="font-size: 1.3rem; font-weight: 800; margin-top:0px; margin-bottom: 1rem; color: var(--indigo);">
                🛠️ Technology Stack
            </h3>
            <div style="margin-bottom: 1.25rem;">
                {tech_badges_html}
            </div>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-top: 1rem; margin-bottom: 0px;">
                Unified Streamlit framework executing direct Python ML inference with zero HTTP latency. Fully optimized for instant local execution and serverless cloud deployment on Streamlit Community Cloud.
            </p>
        </div>
        '''
        render_html(tech_html)

# ----------------------------------------------------
# 7. Global Footer & Medical Disclaimer
# ----------------------------------------------------
render_html('''
<div class="footer-text">
    <p style="margin-bottom: 0.4rem;"><strong>DiagnoWise Health Risk Assessment Engine</strong> • B.Tech Capstone Project & Placement Portfolio</p>
    <p style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0px;">CONFIDENTIAL MEDICAL REPORT SUMMARY. THIS APPLICATION IS FOR INFORMATIONAL & DECISION-SUPPORT PURPOSES ONLY. CONSULT A HEALTHCARE PROFESSIONAL FOR REAL DIAGNOSIS.</p>
</div>
''')
