"""
🩺 DiagnoWise AI (DiagnoWise) - Disease Prediction from Symptoms
Streamlit Production Application optimized for Streamlit Cloud.
Replicates the premium glassmorphism visual layout and model inference capabilities.
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime

# Configure page settings as early as possible
st.set_page_config(
    page_title="DiagnoWise AI - Disease Prediction from Symptoms",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ensure root folder is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app.services.prediction_service import prediction_service
from utils.streamlit_pdf import generate_health_report_pdf

# ----------------------------------------------------
# Session State Initialization
# ----------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []
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
# Global Styling & Glassmorphism Injector
# ----------------------------------------------------
theme_accent = "#10b981" # Emerald primary

if st.session_state.theme == "dark":
    theme_css = """
    :root {
      --primary: #10b981;
      --primary-hover: #059669;
      --primary-light: rgba(16, 185, 129, 0.12);
      --accent: #06b6d4;
      --accent-light: rgba(6, 182, 212, 0.12);
      --indigo: #6366f1;
      
      --bg-main: #090d16;
      --bg-secondary: #0f172a;
      --bg-card: rgba(15, 23, 42, 0.75);
      --bg-card-hover: rgba(30, 41, 59, 0.85);
      --bg-input: rgba(15, 23, 42, 0.6);
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
    theme_css = """
    :root {
      --primary: #10b981;
      --primary-hover: #059669;
      --primary-light: rgba(16, 185, 129, 0.08);
      --accent: #06b6d4;
      --accent-light: rgba(6, 182, 212, 0.08);
      --indigo: #6366f1;
      
      --bg-main: #f8fafc;
      --bg-secondary: #ffffff;
      --bg-card: rgba(255, 255, 255, 0.9);
      --bg-card-hover: #ffffff;
      --bg-input: #ffffff;
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

style_css = theme_css + """
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
  margin-bottom: 2rem;
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
.glass-panel {
  background: var(--bg-card);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: 2.2rem;
  margin-bottom: 1.5rem;
  transition: border-color 0.25s ease;
}

.glass-panel:hover {
  border-color: var(--border-highlight);
}

.hero-section {
  text-align: center;
  padding: 3rem 1rem 3.5rem;
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
  margin-bottom: 1.75rem;
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
  margin-top: 1.25rem;
  padding: 1.25rem;
  background: var(--primary-light);
  border: 1.5px dashed var(--border-highlight);
  border-radius: var(--radius-md);
  margin-bottom: 1.25rem;
}

/* Custom styled gauge display */
.confidence-gauge-html {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 2rem auto;
}

.gauge-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: conic-gradient(var(--primary) calc(var(--percentage) * 1%), var(--border-color) 0);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: var(--shadow-sm);
}

.gauge-circle::before {
  content: "";
  position: absolute;
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background-color: var(--bg-secondary);
}

.gauge-text {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
  margin-top: 5rem;
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

/* Tab overrides */
button[data-baseweb="tab"] {
  background-color: transparent !important;
  color: var(--text-muted) !important;
  font-weight: 600 !important;
  border-bottom: 2px solid transparent !important;
  transition: all 0.2s ease !important;
  padding: 0.6rem 1.2rem !important;
  border-radius: 8px 8px 0 0 !important;
}

button[data-baseweb="tab"]:hover {
  color: var(--primary) !important;
  background-color: var(--primary-light) !important;
}

button[aria-selected="true"] {
  color: var(--primary) !important;
  border-bottom: 2px solid var(--primary) !important;
  font-weight: 700 !important;
}

/* Style select box items */
div[data-baseweb="select"] {
  background-color: var(--bg-input) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-sm) !important;
}

div[role="listbox"] {
  background-color: var(--bg-secondary) !important;
  border: 1px solid var(--border-color) !important;
  color: var(--text-main) !important;
}

/* Remove default streamlit container paddings to allow full styling */
div.block-container {
  padding-top: 1.5rem !important;
  padding-bottom: 2.5rem !important;
  max-width: 1240px !important;
}

/* Hide streamlit default options to look professional */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
"""

st.markdown(f"<style>{style_css}</style>", unsafe_allow_html=True)

# ----------------------------------------------------
# Helper Functions & Callback Logic
# ----------------------------------------------------
def toggle_symptom(symptom_key: str):
    """Toggle symptom inclusion in the selected symptoms catalog."""
    if symptom_key in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.remove(symptom_key)
    else:
        st.session_state.selected_symptoms.append(symptom_key)

def clear_all_symptoms():
    st.session_state.selected_symptoms = []
    st.session_state.prediction_result = None

def run_ml_inference():
    if not st.session_state.selected_symptoms:
        return
    
    # We display a spinner during inference
    with st.spinner("Analyzing Present Symptoms..."):
        try:
            result = prediction_service.predict_disease(
                symptoms=st.session_state.selected_symptoms,
                model_name=st.session_state.selected_model
            )
            st.session_state.prediction_result = result
            
            # Save prediction to local state prediction history
            history_item = {
                "id": str(datetime.now().timestamp()),
                "timestamp": datetime.now().isoformat(),
                "primary_prediction": result["primary_prediction"],
                "confidence_percentage": result["confidence_percentage"],
                "severity": result["severity"],
                "recommended_doctor": result["recommended_doctor"],
                "matched_symptoms_count": result["matched_symptoms_count"],
                "symptoms": list(st.session_state.selected_symptoms),
                "result": result
            }
            # Add to front of history list, keeping max 15 entries
            st.session_state.history = [history_item] + st.session_state.history
            st.session_state.history = st.session_state.history[:15]
            
            # Transition to result page
            st.session_state.current_page = "result"
            st.rerun()
        except Exception as e:
            st.error(f"Inference Engine Error: {str(e)}")

# ----------------------------------------------------
# Main Layout Header (Top Navigation Menu)
# ----------------------------------------------------
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([3.5, 1.2, 1.6, 2.0, 1.0])

with nav_col1:
    st.markdown(
        '''
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
        ''',
        unsafe_allow_html=True
    )

with nav_col2:
    if st.button("Home", key="nav_home", use_container_width=True, type="primary" if st.session_state.current_page == "home" else "secondary"):
        st.session_state.current_page = "home"
        st.rerun()

with nav_col3:
    if st.button("Symptom Checker", key="nav_predict", use_container_width=True, type="primary" if st.session_state.current_page == "predict" else "secondary"):
        st.session_state.current_page = "predict"
        st.rerun()

with nav_col4:
    if st.button("Architecture & Tech", key="nav_about", use_container_width=True, type="primary" if st.session_state.current_page == "about" else "secondary"):
        st.session_state.current_page = "about"
        st.rerun()

with nav_col5:
    theme_text = "☀️ Light" if st.session_state.theme == "dark" else "🌙 Dark"
    if st.button(theme_text, key="nav_theme_toggle", use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

st.markdown("<hr style='margin-top:0.5rem; margin-bottom:2rem; border:0; border-top:1px solid var(--border-color);'>", unsafe_allow_html=True)

# Fetch data catalog
symptoms_data = prediction_service.get_symptoms_list()
all_symptoms = symptoms_data["symptoms"]
categories = symptoms_data["categories"]

# ----------------------------------------------------
# PAGE 1: Home Landing Page
# ----------------------------------------------------
if st.session_state.current_page == "home":
    st.markdown(
        '''
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
        ''',
        unsafe_allow_html=True
    )
    
    # Hero buttons row
    cta_col1, cta_col2, cta_col3, cta_col4 = st.columns([1.5, 1.2, 1.2, 1.5])
    with cta_col2:
        if st.button("Start Diagnosis →", key="hero_start_btn", type="primary", use_container_width=True):
            st.session_state.current_page = "predict"
            st.rerun()
    with cta_col3:
        st.markdown(
            '<a href="#how-it-works" class="stButton" style="text-decoration:none;"><button class="btn btn-secondary" style="width:100%;">Learn More</button></a>',
            unsafe_allow_html=True
        )

    # Statistics Grid
    st.markdown(
        f'''
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
        ''',
        unsafe_allow_html=True
    )

    # How It Works Flow
    st.markdown(
        '''
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
        ''',
        unsafe_allow_html=True
    )

    # Capabilities
    st.markdown(
        '''
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
        ''',
        unsafe_allow_html=True
    )

    # CTA Section Panel
    st.markdown(
        '''
        <div class="glass-panel" style="padding: 3.5rem 2rem; background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(99, 102, 241, 0.15)); text-align: center;">
            <h2 style="font-size: 2.3rem; font-weight: 800; margin-bottom: 1rem; color:var(--text-main);">Ready to Assess Your Health Risk?</h2>
            <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto 2rem; font-size: 1.1rem;">
                Select your symptoms now and run instant machine learning inference.
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )
    cta_col_center = st.columns([2, 1.5, 2])
    with cta_col_center[1]:
        if st.button("Launch Symptom Checker", key="cta_launch_btn", type="primary", use_container_width=True):
            st.session_state.current_page = "predict"
            st.rerun()

# ----------------------------------------------------
# PAGE 2: Symptom Checker
# ----------------------------------------------------
elif st.session_state.current_page == "predict":
    st.markdown(
        '''
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 800; color: var(--text-main);">Symptom Checker & Clinical Assessment</h1>
            <p style="color: var(--text-muted); font-size:1.05rem;">
                Select patient symptoms to evaluate health risk and predict probable diagnoses.
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Main Selection Interface Card
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    # 1. Header: Patient Symptom Intelligence & Model Selector
    checker_hdr_col1, checker_hdr_col2 = st.columns([3, 2])
    with checker_hdr_col1:
        st.markdown(
            '''
            <h2 style="font-size: 1.6rem; font-weight: 800; margin-top:0px; color: var(--text-main);">Patient Symptom Intelligence</h2>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom:0.8rem;">Select all present symptoms to run AI diagnostic inference.</p>
            ''',
            unsafe_allow_html=True
        )
    with checker_hdr_col2:
        model_display_names = {
            "random_forest": "Random Forest Classifier (Default)",
            "gradient_boost": "Gradient Boosting",
            "decision_tree": "Decision Tree",
            "mnb": "Multinomial Naive Bayes"
        }
        selected_model_display = st.selectbox(
            "ML Engine Classifier Model",
            options=list(model_display_names.keys()),
            format_func=lambda x: model_display_names[x],
            key="model_selector"
        )
        st.session_state.selected_model = selected_model_display

    # 2. Selected Tray Panel
    # Make a clean list of displaying symptom labels
    selected_count = len(st.session_state.selected_symptoms)
    
    st.markdown('<div class="selected-tray-html">', unsafe_allow_html=True)
    tray_col1, tray_col2 = st.columns([4, 1.5])
    
    with tray_col1:
        st.markdown(f"<strong style='color:var(--text-main); font-size:1.05rem;'>📋 Selected Symptoms ({selected_count})</strong>", unsafe_allow_html=True)
        if selected_count == 0:
            st.markdown("<p style='color:var(--text-muted); font-size:0.92rem; margin-top:0.5rem;'>No symptoms selected yet. Click symptom chips below or use search.</p>", unsafe_allow_html=True)
        else:
            badges_html = ""
            for sym_key in st.session_state.selected_symptoms:
                sym_obj = next((s for s in all_symptoms if s["key"] == sym_key), None)
                label = sym_obj["label"] if sym_obj else sym_key
                badges_html += f"<span class='selected-badge-item'>✓ {label}</span>"
            st.markdown(f"<div style='margin-top:0.75rem;'>{badges_html}</div>", unsafe_allow_html=True)
            
    with tray_col2:
        if selected_count > 0:
            st.markdown("<div style='display:flex; justify-content:flex-end; align-items:center; height:100%;'>", unsafe_allow_html=True)
            if st.button(f"Clear All ({selected_count})", key="clear_all_symptoms_btn", type="secondary"):
                clear_all_symptoms()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Autocomplete Search Box (Integrated with multiselect!)
    symptom_choices = {item["key"]: item["label"] for item in all_symptoms}
    # User can search and select via standard multiselect
    multiselect_sel = st.multiselect(
        "Search & Add Symptoms Autocomplete",
        options=list(symptom_choices.keys()),
        format_func=lambda x: symptom_choices[x],
        default=st.session_state.selected_symptoms,
        placeholder="Search symptoms by keyword (e.g. fever, skin rash, headache, joint pain)...",
        key="symptom_multiselect"
    )
    # Sync multiselect selection to selected symptoms list
    if multiselect_sel != st.session_state.selected_symptoms:
        st.session_state.selected_symptoms = multiselect_sel
        st.rerun()

    # 4. Filter chips by Category & Search keyword
    category_tabs_options = ["All"] + categories
    # Render horizontal category tab buttons
    cat_cols = st.columns(len(category_tabs_options))
    for idx, cat_opt in enumerate(category_tabs_options):
        with cat_cols[idx]:
            cat_count = len(all_symptoms) if cat_opt == "All" else len([s for s in all_symptoms if s["category"] == cat_opt])
            pill_label = f"{cat_opt} ({cat_count})"
            if st.button(
                pill_label, 
                key=f"cat_pill_{cat_opt}", 
                use_container_width=True, 
                type="primary" if st.session_state.active_category == cat_opt else "secondary"
            ):
                st.session_state.active_category = cat_opt
                st.rerun()

    # Text input search filter for the chips catalog
    st.session_state.search_query = st.text_input(
        "Filter chips catalog by keyword", 
        value=st.session_state.search_query, 
        placeholder="Type to filter chips below...",
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

    # 5. Symptom Chips Catalog Grid
    st.markdown("<p style='color:var(--text-muted); font-size:0.9rem; margin-bottom:0.6rem; font-weight:600;'>Browse Symptoms Chips Catalog</p>", unsafe_allow_html=True)
    if not filtered_symptoms:
        st.info(f"No symptoms matching the current filters: '{st.session_state.search_query}' in category '{st.session_state.active_category}'")
    else:
        # Replicates index.css chips-container with responsive columns
        num_cols = 4
        chip_cols = st.columns(num_cols)
        for chip_idx, sym_obj in enumerate(filtered_symptoms):
            col_idx = chip_idx % num_cols
            with chip_cols[col_idx]:
                key = sym_obj["key"]
                is_sel = key in st.session_state.selected_symptoms
                chip_label = f"✓ {sym_obj['label']}" if is_sel else f"+ {sym_obj['label']}"
                # Using primary button style for selected chips!
                if st.button(
                    chip_label, 
                    key=f"chip_btn_{key}", 
                    use_container_width=True,
                    type="primary" if is_sel else "secondary"
                ):
                    toggle_symptom(key)
                    st.rerun()

    # 6. Action Footer
    st.markdown("<hr style='border:0; border-top:1px solid var(--border-color); margin-top:2rem; margin-bottom:1.5rem;'>", unsafe_allow_html=True)
    footer_cols = st.columns([4, 1.5])
    with footer_cols[1]:
        predict_btn_label = f"Run AI Health Risk Assessment ({selected_count} Selected) →"
        if st.button(
            predict_btn_label, 
            key="run_prediction_action_btn", 
            type="primary", 
            use_container_width=True, 
            disabled=(selected_count == 0)
        ):
            run_ml_inference()
            
    st.markdown('</div>', unsafe_allow_html=True)

    # 7. Local Prediction History Drawer
    if st.session_state.history:
        st.markdown('<div class="glass-panel" style="margin-top: 2rem;">', unsafe_allow_html=True)
        hist_col1, hist_col2 = st.columns([4, 1])
        with hist_col1:
            st.markdown(f"<h3 style='font-size: 1.25rem; font-weight: 800; color:var(--text-main); margin-top:0px;'>🕒 Recent Predictions History ({len(st.session_state.history)})</h3>", unsafe_allow_html=True)
        with hist_col2:
            if st.button("Clear History", key="clear_hist_btn", type="secondary"):
                st.session_state.history = []
                st.rerun()
                
        # History cards grid
        hist_cols = st.columns(3)
        for h_idx, h_item in enumerate(st.session_state.history):
            h_col_idx = h_idx % 3
            with hist_cols[h_col_idx]:
                date_parsed = datetime.fromisoformat(h_item["timestamp"]).strftime("%Y-%m-%d %I:%M %p")
                hist_card_html = f"""
                <div style="background: var(--bg-input); border: 1px solid var(--border-color); padding: 1.1rem; border-radius: var(--radius-sm); margin-bottom:1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <strong style="color: var(--text-main); font-size: 0.98rem;">{h_item['primary_prediction']}</strong>
                        <span style="color: var(--primary); font-weight: 800; font-size: 0.9rem;">{h_item['confidence_percentage']}%</span>
                    </div>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin:0px;">
                        {date_parsed} • {h_item['matched_symptoms_count']} Symptoms • {h_item['recommended_doctor']}
                    </p>
                </div>
                """
                st.markdown(hist_card_html, unsafe_allow_html=True)
                if st.button("Load Report", key=f"load_hist_btn_{h_item['id']}", use_container_width=True):
                    st.session_state.prediction_result = h_item["result"]
                    st.session_state.current_page = "result"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# PAGE 3: Diagnostic Report View
# ----------------------------------------------------
elif st.session_state.current_page == "result":
    result = st.session_state.prediction_result
    
    if not result:
        st.warning("No prediction results found. Please check symptoms first.")
        if st.button("Go to Symptom Checker", type="primary"):
            st.session_state.current_page = "predict"
            st.rerun()
    else:
        # Header controls
        report_ctrl_col1, report_ctrl_col2 = st.columns([1, 1])
        with report_ctrl_col1:
            if st.button("← Test Different Symptoms", key="back_to_predict_btn", type="secondary"):
                st.session_state.current_page = "predict"
                st.rerun()
        with report_ctrl_col2:
            # Generate PDF bytes in python
            try:
                pdf_bytes = generate_health_report_pdf(result)
                filename = f"DiagnoWise_Health_Report_{result['primary_prediction'].replace(' ', '_')}.pdf"
                st.download_button(
                    label="📄 Download Clinical PDF Health Report",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as pdf_err:
                st.error(f"Could not generate PDF: {pdf_err}")

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

        # Main Prediction Panel
        st.markdown(
            f'''
            <div class="glass-panel" style="text-align: center;">
                <div style="display: flex; justify-content: center; gap: 0.75rem; margin-bottom: 1rem; align-items:center;">
                    <span class="hero-badge" style="margin-bottom: 0px;">
                        <span>🩺</span> Diagnostic Inference Result
                    </span>
                    <span class="risk-badge {risk_class}">
                        ● {risk_label}
                    </span>
                </div>
                <h1 style="font-size: 2.8rem; font-weight: 800; margin: 0.4rem 0; color: var(--text-main);">{result["primary_prediction"]}</h1>
                
                <div class="confidence-gauge-html" style="--percentage: {result["confidence_percentage"]};">
                    <div class="gauge-circle">
                        <div class="gauge-text">
                            <span style="font-size: 1.5rem; font-weight:800; color: var(--primary);">{result["confidence_percentage"]}%</span>
                            <span style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; font-weight:700;">Confidence</span>
                        </div>
                    </div>
                </div>
                
                <p style="color: var(--text-muted); max-width: 750px; margin: 0 auto 1.5rem; font-size: 1.1rem; line-height: 1.6;">
                    {result["description"]}
                </p>
                
                <div style="display: inline-flex; gap: 1.5rem; background: var(--bg-input); padding: 0.8rem 1.75rem; border-radius: 999px; border: 1px solid var(--border-color); flex-wrap: wrap; justify-content: center;">
                    <div>
                        <span style="color: var(--text-muted); font-size: 0.85rem;">Clinical Severity: </span>
                        <strong style="color: var(--text-main); font-size: 0.85rem;">{result["severity"]}</strong>
                    </div>
                    <div style="border-left: 1px solid var(--border-color); padding-left: 1.5rem;">
                        <span style="color: var(--text-muted); font-size: 0.85rem;">Evaluated Symptoms: </span>
                        <strong style="color: var(--primary); font-size: 0.85rem;">{result["matched_symptoms_count"]}</strong>
                    </div>
                    <div style="border-left: 1px solid var(--border-color); padding-left: 1.5rem;">
                        <span style="color: var(--text-muted); font-size: 0.85rem;">ML Classifier: </span>
                        <strong style="color: var(--indigo); font-size: 0.85rem; text-transform: capitalize;">{result["model_used"].replace('_', ' ')}</strong>
                    </div>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )

        # Columns Grid layout: Differentials & Medical Specialist
        col_report_left, col_report_right = st.columns(2)
        
        with col_report_left:
            st.markdown('<div class="glass-panel" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown(
                '''
                <h3 style="font-size: 1.3rem; font-weight: 800; margin-top:0px; margin-bottom: 1.25rem; color: var(--text-main); display: flex; align-items: center; gap: 0.5rem;">
                    <span>📊</span> Top 3 Differential Diagnoses
                </h3>
                ''',
                unsafe_allow_html=True
            )
            
            top3_preds = result.get("top_3_predictions", [])
            for idx, item in enumerate(top3_preds[:3]):
                fill_color = "linear-gradient(90deg, #10b981, #06b6d4)" if idx == 0 else "linear-gradient(90deg, #64748b, #94a3b8)"
                primary_text_color = "var(--primary)" if idx == 0 else "var(--text-main)"
                
                st.markdown(
                    f'''
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
                    ''',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_report_right:
            st.markdown('<div class="glass-panel" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">', unsafe_allow_html=True)
            st.markdown(
                '''
                <div>
                    <h3 style="font-size: 1.3rem; font-weight: 800; margin-top:0px; margin-bottom: 1.25rem; color: var(--text-main); display: flex; align-items: center; gap: 0.5rem;">
                        <span>🛡️</span> Health Guidance & Precautions
                    </h3>
                ''',
                unsafe_allow_html=True
            )
            
            # Actionable precautions
            prec_steps_html = ""
            for idx, step in enumerate(result.get("precautions", [])):
                prec_steps_html += f"""
                <div style="background: var(--bg-input); border-left: 4px solid var(--primary); padding: 0.9rem 1.1rem; border-radius: 0 var(--radius-sm) var(--radius-sm) 0; font-size: 0.95rem; margin-bottom: 0.6rem; text-align: left;">
                    <strong style="color: var(--primary); margin-right: 0.4rem;">Step {idx + 1}:</strong> {step}
                </div>
                """
            st.markdown(f"{prec_steps_html}</div>", unsafe_allow_html=True)
            
            # Specialist Card
            st.markdown(
                f'''
                <div style="background: var(--primary-light); border: 1px solid var(--border-highlight); padding: 1.3rem; border-radius: var(--radius-md); display: flex; align-items: center; gap: 1.25rem; margin-top: 1.5rem;">
                    <div style="font-size: 2.3rem;">👨‍⚕️</div>
                    <div>
                        <span style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: var(--primary); font-weight: 800;">
                            Recommended Medical Specialist
                        </span>
                        <h4 style="font-size: 1.15rem; font-weight: 800; color: var(--text-main); margin-top: 0.15rem; margin-bottom:0.15rem;">
                            {result["recommended_doctor"]}
                        </h4>
                        <p style="font-size: 0.82rem; color: var(--text-muted); margin:0px; line-height:1.4;">
                            Schedule a clinical consultation with a certified {result["recommended_doctor"]} for comprehensive diagnosis.
                        </p>
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# PAGE 4: Architecture & Tech Details
# ----------------------------------------------------
elif st.session_state.current_page == "about":
    st.markdown(
        '''
        <div style="text-align: center; margin-bottom: 2rem;">
            <div class="hero-badge">
                <span>⚙️</span> Technical Specifications & Architecture
            </div>
            <h1 style="font-size: 2.5rem; font-weight: 800; color: var(--text-main);">DiagnoWise Platform Engineering</h1>
            <p style="color: var(--text-muted); font-size: 1.05rem;">
                Detailed breakdown of machine learning algorithms, model binaries, and system architecture metrics.
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # 1. Model Performance Benchmark table card
    st.markdown('<div class="glass-panel" style="margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.markdown(
        '''
        <h3 style="font-size: 1.3rem; font-weight: 800; color: var(--primary); margin-top:0px; margin-bottom:1rem;">
            📈 ML Classifier Evaluation Benchmark
        </h3>
        ''',
        unsafe_allow_html=True
    )
    
    # We display a nice tabular format
    benchmark_data = [
        {"Model": "Random Forest (Default)", "Validation Accuracy": "100.00%", "Test Accuracy": "97.62%", "Precision": "0.98", "Recall": "0.98", "F1-Score": "0.98"},
        {"Model": "Decision Tree", "Validation Accuracy": "100.00%", "Test Accuracy": "100.00%", "Precision": "1.00", "Recall": "1.00", "F1-Score": "1.00"},
        {"Model": "Multinomial Naive Bayes", "Validation Accuracy": "100.00%", "Test Accuracy": "100.00%", "Precision": "1.00", "Recall": "1.00", "F1-Score": "1.00"},
        {"Model": "Gradient Boosting", "Validation Accuracy": "100.00%", "Test Accuracy": "97.62%", "Precision": "0.98", "Recall": "0.98", "F1-Score": "0.98"}
    ]
    st.table(benchmark_data)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Two-Column Info Cards
    about_col1, about_col2 = st.columns(2)
    
    with about_col1:
        st.markdown(
            '''
            <div class="glass-panel" style="height: 100%;">
                <h3 style="font-size: 1.3rem; font-weight: 800; margin-top:0px; margin-bottom: 1rem; color: var(--primary);">
                    🎓 Academic & Portfolio Context
                </h3>
                <p style="color: var(--text-muted); font-size: 0.95rem; line-height:1.6; margin-bottom: 1.25rem;">
                    DiagnoWise was engineered as a B.Tech Final Year Capstone Project and Placement Portfolio Application. It demonstrates real-world software engineering, machine learning inference, REST API architecture, and UI/UX design.
                </p>
                <div style="background: var(--bg-input); padding: 1.2rem; border-radius: var(--radius-sm); border: 1px solid var(--border-color); line-height: 1.6;">
                    <p style="font-size: 0.88rem; margin-top:0px; margin-bottom:0.4rem; color: var(--text-main);"><strong>Target Prognoses:</strong> 41 Unique Diseases</p>
                    <p style="font-size: 0.88rem; margin-top:0px; margin-bottom:0.4rem; color: var(--text-main);"><strong>Symptom Feature Space:</strong> 132 Binary Medical Attributes</p>
                    <p style="font-size: 0.88rem; margin-top:0px; margin-bottom:0px; color: var(--text-main);"><strong>Clinical Knowledge Base:</strong> 41 Profiles with 4-step Precautions & Specialist Doctors</p>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
    with about_col2:
        st.markdown('<div class="glass-panel" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown(
            '''
            <h3 style="font-size: 1.3rem; font-weight: 800; margin-top:0px; margin-bottom: 1rem; color: var(--indigo);">
                🛠️ Technology Stack
            </h3>
            ''',
            unsafe_allow_html=True
        )
        
        techs = ['Streamlit', 'Python 3.10+', 'Scikit-Learn', 'Joblib', 'Pandas', 'FPDF2', 'FastAPI', 'React 18', 'Vite', 'Vanilla CSS']
        tech_badges_html = ""
        for t in techs:
            tech_badges_html += f"<span style='background: var(--primary-light); border: 1px solid var(--border-highlight); color: var(--text-main); padding: 0.35rem 0.85rem; border-radius: 6px; font-size: 0.82rem; font-weight: 700; display:inline-block; margin:0.3rem;'>{t}</span>"
        
        st.markdown(
            f'''
            <div style="margin-bottom: 1.25rem;">
                {tech_badges_html}
            </div>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-top: 1rem; margin-bottom: 0px;">
                Decoupled architecture utilizing an asynchronous FastAPI backend for vector prediction and a responsive React client interface. Transitioned to a single-layer Streamlit framework for optimized serverless deployment on Streamlit Cloud.
            </p>
            ''',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# Main Layout Footer
# ----------------------------------------------------
st.markdown(
    '''
    <div class="footer-text">
        <p style="margin-bottom: 0.4rem;"><strong>DiagnoWise Health Risk Assessment Engine</strong> • B.Tech Capstone Project & Placement Portfolio</p>
        <p style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0px;">CONFIDENTIAL MEDICAL REPORT SUMMARY. THIS APPLICATION IS FOR INFORMATIONAL & DECISION-SUPPORT PURPOSES ONLY. CONSULT A HEALTHCARE PROFESSIONAL FOR REAL DIAGNOSIS.</p>
    </div>
    ''',
    unsafe_allow_html=True
)
