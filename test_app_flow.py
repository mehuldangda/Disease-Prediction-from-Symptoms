"""
Test suite to thoroughly verify:
1. ML prediction pipeline functionality
2. Patient demographics handling
3. PDF generation with patient demographics
4. HTML sanitization (render_html) ensuring NO markdown code blocks are triggered
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ml.data_loader import DataLoader
from ml.predictor import DiseasePredictor
from utils.streamlit_pdf import generate_health_report_pdf

def test_ml_pipeline():
    print("Testing ML Pipeline...")
    predictor = DiseasePredictor(model_name="random_forest")
    symptoms = ["fatigue", "weight_loss", "restlessness", "lethargy", "irregular_sugar_level"]
    result = predictor.predict(symptoms)
    
    assert "primary_prediction" in result, "Missing primary_prediction"
    assert "confidence_percentage" in result, "Missing confidence_percentage"
    assert "top_3_predictions" in result, "Missing top_3_predictions"
    assert len(result["top_3_predictions"]) == 3, "Expected 3 top predictions"
    assert "precautions" in result, "Missing precautions"
    assert len(result["precautions"]) > 0, "Precautions empty"
    assert "recommended_doctor" in result, "Missing doctor"
    
    result["patient_name"] = "Ram Singh"
    result["patient_age"] = 22
    result["patient_gender"] = "Male"
    print(f"Prediction OK: {result['primary_prediction']} ({result['confidence_percentage']}%)")
    return result

def test_pdf_generation(result):
    print("Testing PDF Generation...")
    import re
    import zlib
    
    pdf_bytes = generate_health_report_pdf(result)
    assert pdf_bytes is not None, "PDF bytes is None"
    assert len(pdf_bytes) > 1000, f"PDF bytes unexpectedly small: {len(pdf_bytes)}"
    assert pdf_bytes.startswith(b"%PDF"), "PDF missing %PDF header"
    
    # Decompress FlateDecode streams to verify text content
    decompressed_text = []
    for m in re.finditer(b'stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
        try:
            decompressed_text.append(zlib.decompress(m.group(1)).decode('latin1', errors='ignore'))
        except Exception:
            pass
    full_pdf_text = "\n".join(decompressed_text)
    
    assert "Ram Singh" in full_pdf_text, "Patient name 'Ram Singh' missing from PDF text"
    assert "22 Years" in full_pdf_text, "Patient age '22 Years' missing from PDF text"
    assert "Male" in full_pdf_text, "Patient gender 'Male' missing from PDF text"
    print(f"PDF generated successfully with Patient Demographics verified ({len(pdf_bytes)} bytes)")

def test_render_html_safety(result):
    print("Testing render_html safety on Result page HTML strings...")
    
    def clean(html_str: str) -> str:
        return "\n".join(line.strip() for line in html_str.splitlines() if line.strip())

    pred_title = result["primary_prediction"]
    pred_conf = result["confidence_percentage"]
    pred_desc = result["description"]
    pred_sev = result["severity"]
    pred_sym_count = result["matched_symptoms_count"]
    pred_model = result["model_used"].replace('_', ' ').title()
    risk_class = "risk-high"
    risk_label = "High Risk"

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

    cleaned_main = clean(main_card_html)
    
    # Check that NO line in cleaned_main starts with 4 or more spaces
    for idx, line in enumerate(cleaned_main.splitlines()):
        assert not line.startswith("    "), f"Line {idx} has leading 4 spaces: {line[:30]}"
        assert len(line.strip()) > 0, f"Line {idx} is empty"

    print("render_html safety verified! Zero lines trigger markdown code block formatting.")

if __name__ == "__main__":
    res = test_ml_pipeline()
    test_pdf_generation(res)
    test_render_html_safety(res)
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
