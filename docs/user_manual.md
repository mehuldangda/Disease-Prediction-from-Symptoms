# User Manual - DiagnoWise AI Disease Predictor

## 1. Overview
DiagnoWise AI helps clinicians, researchers, and users analyze observed symptoms and generate differential diagnosis predictions backed by high-precision machine learning models.

---

## 2. Step-by-Step User Flow

### Step 1: Accessing the Application
Launch the Streamlit app and open `http://localhost:8501` in your browser.

### Step 2: Selecting Symptoms
1. Click **Symptom Checker** in the top navigation bar (or click "Start Diagnosis →" from the Home page).
2. Use the **Search & Add Symptoms Autocomplete** box to search directly by keyword (e.g., "itching", "skin rash", "fever", "cough").
3. Alternatively, click category pills (*All*, *Dermatological & Skin*, *Respiratory & ENT*, *Gastrointestinal*, *Musculoskeletal*, *General & Systemic*, *Urinary & Renal*, *Neurological & Mental Health*) to filter the symptom chips catalog.
4. Click on any symptom chip to toggle selection. Selected symptoms appear in the active selection tray.

### Step 3: Selecting ML Algorithm Model
In the top-right model selector dropdown, choose your preferred classifier:
- **Random Forest Classifier (Default)**
- **Gradient Boosting**
- **Decision Tree**
- **Multinomial Naive Bayes**

### Step 4: Running Inference
Click the **Run AI Health Risk Assessment →** button.

### Step 5: Understanding Results
- **Primary Diagnosis:** Shows the most likely disease with its calibrated confidence percentage and severity risk badge (Low, Medium, High).
- **Confidence Gauge:** Visual radial meter representing model certainty.
- **Top 3 Differential Diagnoses:** Visualizes progress bars and probability scores for the top 3 differential diagnoses.
- **Actionable Precautions:** Displays 4 key steps to take immediately.
- **Recommended Specialist Doctor:** Highlights the appropriate medical specialist to consult (e.g., Dermatologist, Pulmonologist, Gastroenterologist).
- **Download PDF Report:** Click "📄 Download Clinical PDF Health Report" to export a printable PDF health report.
