# DiagnoWise AI Disease Prediction System - B.Tech Final Year Project Report

## Abstract
DiagnoWise AI (Disease Prediction from Symptoms) is an artificial intelligence clinical decision-support framework engineered to infer probable human medical diagnoses from user-selected symptom combinations. Utilizing clinical data representing 41 target prognoses and 132 symptom features, the system employs supervised ensemble classification (Random Forest, Decision Tree, Naive Bayes, Gradient Boosting) to deliver differential diagnoses accompanied by calibrated confidence percentages, 4-step precautionary measures, specialist medical doctor recommendations, and printable clinical PDF health reports via a unified Streamlit web application.

---

## 1. Introduction
Early symptom identification plays a critical role in proactive healthcare intervention. Traditional medical diagnostic tools often lack accessible interfaces or fail to provide differential probability distributions. This project bridges that gap by providing a high-performance, single-stack Streamlit web application that runs ML inference directly in Python with zero network overhead.

---

## 2. Machine Learning Methodology & Evaluation

### 2.1 Dataset Description
- **Total Symptoms (Features):** 132 binary features ($X \in \{0, 1\}^{132}$)
- **Total Diseases (Target Labels):** 41 unique clinical prognoses ($y \in \mathcal{C}$)
- **Training Records:** 4,920 samples
- **Test Validation Set:** 42 samples

### 2.2 Model Architecture & Algorithms
1. **Random Forest Classifier (Primary):** Ensemble of decision trees evaluated using entropy and Gini impurity metrics. Provides calibrated class probabilities via `predict_proba()`.
2. **Gradient Boosting Classifier:** Sequential boosting trees optimized with Friedman MSE criterion.
3. **Decision Tree Classifier:** Single-tree decision boundary benchmark.
4. **Multinomial Naive Bayes (MNB):** Probabilistic baseline for categorical binary feature vectors.

### 2.3 Empirical Results
| Model Name | Validation Accuracy | Test Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | 100.00% | **97.62%** | 0.98 | 0.98 | 0.98 |
| **Decision Tree** | 100.00% | **100.00%** | 1.00 | 1.00 | 1.00 |
| **Multinomial Naive Bayes** | 100.00% | **100.00%** | 1.00 | 1.00 | 1.00 |
| **Gradient Boosting** | 100.00% | **97.62%** | 0.98 | 0.98 | 0.98 |

---

## 3. System Architecture & Component Design
- **Application Framework (Streamlit):** Unified reactive UI with session state management, `@st.cache_resource` model caching, and custom glassmorphism styling.
- **Inference Engine (`ml/predictor.py`):** Direct vector construction and `predict_proba()` inference without intermediate REST latency.
- **Knowledge Base Integration (`ml/disease_db.py`):** Rich metadata lookup mapping all 41 prognoses to descriptions, 4-step precautions, and recommended medical specialists (Dermatologists, Pulmonologists, Gastroenterologists, Neurologists, Cardiologists).
- **Report Generation (`utils/streamlit_pdf.py`):** Printable clinical PDF report generator utilizing FPDF2.

---

## 4. Conclusion & Future Scope
The system achieves exceptional accuracy across test benchmarks while providing an intuitive, patient-friendly diagnostic interface. Future developments include integrating EHR (Electronic Health Record) standards, multi-language localization, and LLM-driven medical consultation assistance.
