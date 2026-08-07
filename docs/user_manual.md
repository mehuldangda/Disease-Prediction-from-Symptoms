# User Manual - DiagnoWise AI Disease Predictor

## 1. Overview
DiagnoWise AI helps users analyze observed symptoms and generate differential diagnosis predictions backed by machine learning.

---

## 2. Step-by-Step User Flow

### Step 1: Accessing the Application
Open your web browser and navigate to `http://localhost:8000` (or `http://localhost:5173` if running React dev server).

### Step 2: Selecting Symptoms
1. Click **Symptom Checker** in the top navigation bar.
2. Use the **Search bar** to quickly find specific symptoms (e.g., "itching", "fever", "cough").
3. Alternatively, click category tabs (e.g. *Dermatological*, *Respiratory*, *Gastrointestinal*) to filter symptoms.
4. Click on any symptom chip to select it. Selected symptoms appear in the active selection tray below.

### Step 3: Selecting ML Algorithm Model
In the top-right model selector dropdown, choose your preferred classifier:
- **Random Forest Classifier (Recommended Default)**
- **Gradient Boosting**
- **Decision Tree**
- **Multinomial Naive Bayes**

### Step 4: Running Inference
Click the **Run Medical Prediction →** button.

### Step 5: Understanding Results
- **Primary Diagnosis:** Shows the most likely disease with its calibrated confidence percentage.
- **Top 3 Differential Diagnoses:** Visualizes progress bars and probability scores for top alternative diagnoses.
- **Actionable Precautions:** Displays 4 key steps to take immediately.
- **Recommended Specialist Doctor:** Highlights the appropriate doctor to consult (e.g., Dermatologist, Pulmonologist, Gastroenterologist).
