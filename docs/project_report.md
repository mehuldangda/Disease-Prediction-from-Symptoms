# Disease Prediction System - B.Tech Final Year Project Report

## Abstract
Disease Prediction from Symptoms is an artificial intelligence decision-support framework engineered to infer probable human medical diagnoses from user-selected symptom combinations. Utilizing clinical data representing 41 target prognoses and 132 symptom features, the system employs supervised ensemble classification (Random Forest, Decision Tree, Naive Bayes, Gradient Boosting) to deliver differential diagnoses accompanied by calibrated confidence percentages, 4-step precautionary measures, and specialist medical doctor recommendations.

---

## 1. Introduction
Early symptom identification plays a critical role in proactive healthcare intervention. Traditional medical diagnostic tools often lack accessible web interfaces or fail to provide probability rankings across differential diagnoses. This project bridges that gap by providing a modern, full-stack, decoupled architecture comprising a FastAPI backend and a React (Vite) client interface.

---

## 2. Machine Learning Methodology & Evaluation

### 2.1 Dataset Description
- **Total Symptoms (Features):** 132 binary features ($X \in \{0, 1\}^{132}$)
- **Total Diseases (Target Labels):** 41 unique clinical prognoses ($y \in \mathcal{C}$)
- **Training Records:** 4,920 samples
- **Test Validation Set:** 42 samples

### 2.2 Model Architecture & Algorithms
1. **Random Forest Classifier (Primary):** Ensemble of 10 decision trees evaluated using entropy and Gini impurity metrics. Provides calibrated class probabilities via `predict_proba()`.
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
- **Backend API (FastAPI):** Asynchronous route handlers, Pydantic v2 schemas, CORS middleware, structured logging, and joblib model persistence.
- **Frontend Client (React + Vite):** Component-driven architecture using Vanilla CSS design tokens (teal/cyan dark aesthetic, responsive breakpoints, autocomplete search).
- **Knowledge Base Integration:** Rich metadata lookup mapping all 41 prognoses to descriptions, 4-step precautions, and recommended medical specialists (Dermatologists, Pulmonologists, Gastroenterologists, Neurologists, Cardiologists).

---

## 4. Conclusion & Future Scope
The system achieves exceptional accuracy across test benchmarks while providing an intuitive, patient-friendly diagnostic interface. Future developments include integrating EHR (Electronic Health Record) standards, multi-language localization, and LLM-driven medical summary generation.
