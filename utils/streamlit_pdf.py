"""
DiagnoWise Health Report PDF Generator
Generates a beautifully formatted, printable clinical health report PDF using FPDF2.
Includes Patient Profile (Name, Age, Sex), Diagnostic Inference, Differential Diagnoses,
Precautions, and Specialist Recommendation.
"""

import io
from datetime import datetime
from fpdf import FPDF


def clean_pdf_text(text: str) -> str:
    """Replace non-latin1 characters with ASCII equivalents to prevent FPDF Unicode Encoding Exception."""
    if not text:
        return ""
    replacements = {
        "\u2022": "-", # Bullet
        "\u201c": '"', # Left double quote
        "\u201d": '"', # Right double quote
        "\u2019": "'", # Apostrophe
        "\u2018": "'", # Left single quote
        "\u2013": "-", # En dash
        "\u2014": "--", # Em dash
        "\u00ae": "(R)", # Registered trademark
        "\u2122": "TM", # Trademark
        "\u00a9": "(C)", # Copyright
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text.encode("latin-1", errors="ignore").decode("latin-1")


class HealthReportPDF(FPDF):
    def __init__(self, patient_info: str = ""):
        super().__init__(orientation='P', unit='mm', format='letter')
        self.patient_info = patient_info
        self.set_margins(15, 12, 15)
        self.set_auto_page_break(auto=True, margin=12)
        
    def header(self):
        # Top primary emerald color stripe
        self.set_fill_color(16, 185, 129)
        self.rect(0, 0, 215.9, 4, 'F')
        
    def footer(self):
        self.set_y(-13)
        self.set_font('helvetica', 'I', 7.5)
        self.set_text_color(100, 116, 139) # slate-500
        if self.patient_info:
            self.cell(0, 4, f'Patient Record: {self.patient_info} | DiagnoWise AI Health Risk Assessment Engine', 0, 1, 'C')
        else:
            self.cell(0, 4, 'DiagnoWise AI Health Risk Assessment Engine - B.Tech Final Year Capstone Project', 0, 1, 'C')
        self.cell(0, 4, 'CONFIDENTIAL MEDICAL REPORT. FOR INFORMATIONAL & DECISION-SUPPORT PURPOSES ONLY. CONSULT A LICENSED PHYSICIAN.', 0, 0, 'C')


def generate_health_report_pdf(result: dict) -> bytes:
    """
    Constructs a professional medical PDF document with Patient Profile,
    Primary Prognosis, Confidence Score, Differential Rankings, and Precautions.
    """
    p_name = clean_pdf_text(str(result.get('patient_name') or 'Anonymous Patient').strip())
    if not p_name:
        p_name = 'Anonymous Patient'
    p_age = str(result.get('patient_age', 28))
    p_sex = clean_pdf_text(str(result.get('patient_gender') or 'Male').strip())
    rec_doctor = clean_pdf_text(result.get('recommended_doctor', 'General Physician'))
    
    patient_summary = f"{p_name} ({p_age}y, {p_sex})"
    pdf = HealthReportPDF(patient_info=patient_summary)
    pdf.add_page()
    
    # ----------------------------------------------------
    # Header Section
    # ----------------------------------------------------
    pdf.set_y(10)
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(15, 23, 42) # slate-900
    pdf.write(10, "Diagno")
    
    pdf.set_text_color(16, 185, 129) # emerald-500
    pdf.write(10, "Wise")
    
    pdf.set_text_color(6, 182, 212) # cyan-500
    pdf.set_font('helvetica', 'B', 13)
    pdf.write(10, " AI")
    
    # Right-aligned timestamp & patient metadata
    pdf.set_font('helvetica', '', 8.5)
    pdf.set_text_color(71, 85, 105) # slate-600
    date_str = datetime.now().strftime("%B %d, %Y %I:%M %p")
    model_name = clean_pdf_text(result.get('model_used', 'random_forest').replace('_', ' ').upper())
    
    pdf.set_xy(115, 7)
    pdf.multi_cell(85, 4, f"Report Date: {date_str}\nPatient: {p_name} ({p_age}y, {p_sex})\nML Classifier: {model_name}", 0, 'R')
    
    # Divider line
    pdf.set_draw_color(16, 185, 129)
    pdf.set_line_width(0.5)
    pdf.line(15, 24, 200.9, 24)
    
    # ----------------------------------------------------
    # 1. Patient Profile Card (Highly Prominent Clinical Intake)
    # ----------------------------------------------------
    pdf.set_fill_color(248, 250, 252) # slate-50
    pdf.set_draw_color(203, 213, 225) # slate-300
    pdf.rect(15, 27, 185.9, 21, 'DF')
    
    # Left emerald decorative accent bar
    pdf.set_fill_color(16, 185, 129)
    pdf.rect(15, 27, 3.5, 21, 'F')
    
    # Card Header
    pdf.set_xy(22, 28.5)
    pdf.set_font('helvetica', 'B', 7)
    pdf.set_text_color(16, 185, 129) # emerald-600
    pdf.cell(0, 3, "PATIENT PROFILE & CLINICAL INTAKE IDENTIFIERS", 0, 1)
    
    # Column Labels
    pdf.set_xy(22, 32.5)
    pdf.set_font('helvetica', 'B', 7.5)
    pdf.set_text_color(100, 116, 139) # slate-500
    pdf.cell(62, 3.5, "PATIENT FULL NAME", 0, 0)
    pdf.cell(32, 3.5, "AGE", 0, 0)
    pdf.cell(42, 3.5, "BIOLOGICAL SEX", 0, 0)
    pdf.cell(44, 3.5, "CLINICAL STATUS", 0, 1)
    
    # Column Values
    pdf.set_xy(22, 37)
    pdf.set_font('helvetica', 'B', 10.5)
    pdf.set_text_color(15, 23, 42) # slate-900
    pdf.cell(62, 5, p_name, 0, 0)
    pdf.cell(32, 5, f"{p_age} Years", 0, 0)
    pdf.cell(42, 5, p_sex, 0, 0)
    pdf.set_font('helvetica', 'B', 9.5)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(44, 5, "Verified Inference", 0, 1)
    
    # ----------------------------------------------------
    # 2. Primary Diagnostic Inference Card
    # ----------------------------------------------------
    pdf.set_fill_color(248, 250, 252) # slate-50
    pdf.set_draw_color(226, 232, 240) # slate-200
    pdf.rect(15, 50, 185.9, 52, 'DF')
    
    pdf.set_xy(20, 53)
    pdf.set_font('helvetica', 'B', 8)
    pdf.set_text_color(100, 116, 139) # slate-500
    pdf.cell(0, 4, "PRIMARY DIAGNOSTIC INFERENCE", 0, 1)
    
    pdf.set_x(20)
    pdf.set_font('helvetica', 'B', 19)
    pdf.set_text_color(15, 23, 42) # slate-900
    primary_pred = clean_pdf_text(result.get('primary_prediction', '').strip())
    pdf.cell(0, 9, primary_pred, 0, 1)
    
    # Badges Row
    pdf.set_x(20)
    conf_pct = result.get('confidence_percentage', 0.0)
    severity = clean_pdf_text(result.get('severity', 'Moderate'))
    
    # Determine risk colors
    sev_lower = severity.lower()
    if 'high' in sev_lower or 'critical' in sev_lower:
        badge_bg = (254, 226, 226)
        badge_text = (153, 27, 27)
        risk_label = f"{severity} Risk"
    elif 'low' in sev_lower:
        badge_bg = (209, 250, 229)
        badge_text = (6, 95, 70)
        risk_label = f"{severity} Risk"
    else:
        badge_bg = (254, 243, 199)
        badge_text = (146, 64, 14)
        risk_label = f"{severity} Risk"
        
    pdf.set_fill_color(16, 185, 129)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 8.5)
    pdf.cell(48, 5.5, f"  {conf_pct}% Confidence Score  ", 0, 0, 'C', True)
    
    pdf.set_x(71)
    pdf.set_fill_color(*badge_bg)
    pdf.set_text_color(*badge_text)
    pdf.cell(42, 5.5, f"  {risk_label}  ", 0, 1, 'C', True)
    
    # Clinical Description text
    pdf.set_xy(20, 75)
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(71, 85, 105) # slate-600
    description_cleaned = clean_pdf_text(result.get('description', ''))
    pdf.multi_cell(175, 4.2, description_cleaned, 0, 'L')
    
    # ----------------------------------------------------
    # 3. Evaluated Symptoms Card
    # ----------------------------------------------------
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(15, 104, 185.9, 21, 'DF')
    
    pdf.set_xy(20, 106)
    pdf.set_font('helvetica', 'B', 9)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 4, f"Evaluated Present Symptoms ({result.get('matched_symptoms_count', 0)})", 0, 1)
    
    pdf.set_x(20)
    pdf.set_font('helvetica', '', 8.5)
    pdf.set_text_color(71, 85, 105)
    symptoms_formatted = [clean_pdf_text(s.replace('_', ' ').title()) for s in result.get('matched_symptoms', [])]
    symptoms_text = ", ".join(symptoms_formatted) if symptoms_formatted else "No specific symptoms evaluated."
    pdf.multi_cell(175, 3.8, symptoms_text, 0, 'L')
    
    # ----------------------------------------------------
    # 4. Grid: Top 3 Differentials (Left) & Specialist Recommendation (Right)
    # ----------------------------------------------------
    y_grid = 127
    grid_height = 47
    
    # Left Column: Differentials
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(15, y_grid, 90, grid_height, 'DF')
    
    pdf.set_xy(20, y_grid + 3)
    pdf.set_font('helvetica', 'B', 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(80, 4.5, "Top 3 Differential Diagnoses", 0, 1)
    
    top3 = result.get('top_3_predictions', [])
    for idx, item in enumerate(top3[:3]):
        pdf.set_x(20)
        pdf.set_font('helvetica', 'B', 8.5)
        pdf.set_text_color(15, 23, 42)
        d_name = clean_pdf_text(item['disease'])
        pdf.cell(55, 4, f"#{idx+1} {d_name}", 0, 0)
        
        pdf.set_font('helvetica', 'B', 8.5)
        pdf.set_text_color(16, 185, 129)
        pdf.cell(20, 4, f"{item['probability']}%", 0, 1, 'R')
        
        pdf.set_x(20)
        pdf.set_font('helvetica', '', 7.5)
        pdf.set_text_color(100, 116, 139)
        doc_name_clean = clean_pdf_text(item['doctor'])
        pdf.cell(80, 3.5, f"Specialist: {doc_name_clean}", 0, 1)
        pdf.ln(1)
        
    # Right Column: Recommended Specialist
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(110.9, y_grid, 90, grid_height, 'DF')
    
    pdf.set_xy(115.9, y_grid + 3)
    pdf.set_font('helvetica', 'B', 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(80, 4.5, "Recommended Specialist Doctor", 0, 1)
    
    pdf.set_xy(115.9, y_grid + 11)
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(80, 6, f"Specialist: {rec_doctor}", 0, 1)
    
    pdf.set_xy(115.9, y_grid + 19)
    pdf.set_font('helvetica', '', 8.5)
    pdf.set_text_color(71, 85, 105)
    specialist_note = (
        f"We recommend scheduling a clinical consultation with a certified {rec_doctor} "
        "for comprehensive laboratory workup, diagnostic tests, and tailored disease management."
    )
    pdf.multi_cell(80, 4, clean_pdf_text(specialist_note), 0, 'L')
    
    # ----------------------------------------------------
    # 5. Actionable Precautions & Guidance Section
    # ----------------------------------------------------
    y_prec = 176
    pdf.set_y(y_prec)
    pdf.set_font('helvetica', 'B', 10.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 5, "Actionable Medical Precautions & Self-Care Guidance", 0, 1)
    
    pdf.set_draw_color(16, 185, 129)
    pdf.set_line_width(0.3)
    pdf.line(15, y_prec + 6, 200.9, y_prec + 6)
    
    pdf.set_y(y_prec + 8)
    precautions = result.get('precautions', [])
    for idx, step in enumerate(precautions):
        curr_y = pdf.get_y()
        pdf.set_fill_color(16, 185, 129)
        pdf.rect(15, curr_y + 0.5, 2.5, 7.5, 'F')
        
        pdf.set_x(20)
        pdf.set_font('helvetica', 'B', 9)
        pdf.set_text_color(16, 185, 129)
        pdf.cell(15, 4.5, f"Step {idx+1}:", 0, 0)
        
        pdf.set_font('helvetica', '', 9)
        pdf.set_text_color(71, 85, 105)
        pdf.multi_cell(165, 4.5, clean_pdf_text(step), 0, 'L')
        pdf.ln(1)
        
    return bytes(pdf.output())
