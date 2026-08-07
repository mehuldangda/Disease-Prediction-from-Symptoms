"""
DiagnoWise Health Report PDF Generator
Generates a beautifully formatted, printable health report PDF using FPDF2.
"""

import io
from datetime import datetime
from fpdf import FPDF

def clean_pdf_text(text: str) -> str:
    """Replace non-latin1 characters with close ASCII equivalents to prevent FPDF Unicode Encoding Exception."""
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
    # Fallback to encode latin-1 ignoring unencodable characters
    return text.encode("latin-1", errors="ignore").decode("latin-1")

class HealthReportPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='letter')
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # Draw a top decorative color stripe
        self.set_fill_color(16, 185, 129) # Primary Emerald
        self.rect(0, 0, 215.9, 4, 'F')
        
    def footer(self):
        # Position at 15 mm from bottom
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(148, 163, 184) # slate-400
        self.cell(0, 5, 'DiagnoWise Health Risk Assessment Engine - B.Tech Capstone Project', 0, 1, 'C')
        self.cell(0, 5, 'CONFIDENTIAL MEDICAL REPORT SUMMARY. FOR INFORMATIONAL & DECISION-SUPPORT PURPOSES ONLY.', 0, 0, 'C')

def generate_health_report_pdf(result: dict) -> bytes:
    """
    Constructs a PDF document based on prediction results and returns the bytes.
    """
    pdf = HealthReportPDF()
    pdf.add_page()
    
    # ----------------------------------------------------
    # Header Section
    # ----------------------------------------------------
    pdf.set_font('helvetica', 'B', 22)
    pdf.set_text_color(15, 23, 42) # slate-900
    pdf.write(12, "Diagno")
    
    pdf.set_text_color(16, 185, 129) # emerald-500
    pdf.write(12, "Wise")
    
    pdf.set_text_color(6, 182, 212) # cyan-500
    pdf.set_font('helvetica', 'B', 14)
    pdf.write(12, " AI")
    
    # Right-aligned timestamp & info
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(71, 85, 105) # slate-600
    date_str = datetime.now().strftime("%B %d, %Y %I:%M %p")
    
    # We position x to write the meta information on the right side
    pdf.set_xy(135, 15)
    model_name = clean_pdf_text(result['model_used'].replace('_', ' ').upper())
    pdf.multi_cell(65, 4.5, f"Report Generated:\n{date_str}\nModel: {model_name}", 0, 'R')
    
    # Line divider
    pdf.set_draw_color(16, 185, 129)
    pdf.set_line_width(0.5)
    pdf.line(15, 32, 200, 32)
    
    pdf.ln(10)
    
    # ----------------------------------------------------
    # Primary Diagnosis Card
    # ----------------------------------------------------
    # Background rect for card
    pdf.set_fill_color(248, 250, 252) # slate-50
    pdf.set_draw_color(226, 232, 240) # slate-200
    pdf.rect(15, 36, 185.9, 58, 'DF')
    
    pdf.set_xy(20, 39)
    pdf.set_font('helvetica', 'B', 9)
    pdf.set_text_color(100, 116, 139) # slate-500
    pdf.cell(0, 5, "PRIMARY DIAGNOSTIC INFERENCE", 0, 1)
    
    pdf.set_x(20)
    pdf.set_font('helvetica', 'B', 22)
    pdf.set_text_color(15, 23, 42) # slate-900
    primary_pred = clean_pdf_text(result.get('primary_prediction', '').strip())
    pdf.cell(0, 10, primary_pred, 0, 1)
    
    # Badges
    pdf.set_x(20)
    conf_pct = result.get('confidence_percentage', 0.0)
    severity = clean_pdf_text(result.get('severity', 'Moderate'))
    
    # Determine risk colors
    sev_lower = severity.lower()
    if 'high' in sev_lower or 'critical' in sev_lower:
        badge_bg = (254, 226, 226) # light red
        badge_text = (153, 27, 27) # dark red
        risk_label = f"{severity} Risk"
    elif 'low' in sev_lower:
        badge_bg = (209, 250, 229) # light green
        badge_text = (6, 95, 70) # dark green
        risk_label = f"{severity} Risk"
    else:
        badge_bg = (254, 243, 199) # light yellow
        badge_text = (146, 64, 14) # dark yellow
        risk_label = f"{severity} Risk"
        
    # Draw Confidence badge in green
    pdf.set_fill_color(16, 185, 129)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(48, 6, f"  {conf_pct}% Confidence Score  ", 0, 0, 'C', True)
    
    # Draw Risk badge
    pdf.set_x(72)
    pdf.set_fill_color(*badge_bg)
    pdf.set_text_color(*badge_text)
    pdf.cell(42, 6, f"  {risk_label}  ", 0, 1, 'C', True)
    
    # Description text
    pdf.set_xy(20, 64)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(71, 85, 105) # slate-600
    description_cleaned = clean_pdf_text(result.get('description', ''))
    pdf.multi_cell(175, 5, description_cleaned, 0, 'L')
    
    # Position back after card
    pdf.set_y(98)
    
    # ----------------------------------------------------
    # Symptoms Catalog Card
    # ----------------------------------------------------
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(15, 98, 185.9, 26, 'DF')
    
    pdf.set_xy(20, 101)
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 5, f"Evaluated Present Symptoms ({result.get('matched_symptoms_count', 0)})", 0, 1)
    
    pdf.set_x(20)
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(71, 85, 105)
    symptoms_formatted = [clean_pdf_text(s.replace('_', ' ').title()) for s in result.get('matched_symptoms', [])]
    symptoms_text = ", ".join(symptoms_formatted)
    if not symptoms_text:
        symptoms_text = "No symptoms evaluated."
    pdf.multi_cell(175, 4.5, symptoms_text, 0, 'L')
    
    pdf.set_y(128)
    
    # ----------------------------------------------------
    # Grid Layout: Left Column (Top 3 Differentials) & Right Column (Specialist)
    # ----------------------------------------------------
    # Draw Top Differential Diagnoses Box
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(15, 128, 90, 58, 'DF')
    
    pdf.set_xy(20, 131)
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(80, 5, "Top 3 Differential Diagnoses", 0, 1)
    
    pdf.ln(2)
    
    top3 = result.get('top_3_predictions', [])
    for idx, item in enumerate(top3[:3]):
        pdf.set_x(20)
        pdf.set_font('helvetica', 'B', 9)
        pdf.set_text_color(15, 23, 42)
        disease_name = clean_pdf_text(item['disease'])
        pdf.cell(55, 4.5, f"#{idx+1} {disease_name}", 0, 0)
        
        pdf.set_font('helvetica', 'B', 9)
        pdf.set_text_color(16, 185, 129)
        pdf.cell(20, 4.5, f"{item['probability']}%", 0, 1, 'R')
        
        pdf.set_x(20)
        pdf.set_font('helvetica', '', 8)
        pdf.set_text_color(100, 116, 139)
        doctor_name_clean = clean_pdf_text(item['doctor'])
        pdf.cell(80, 4, f"Specialist: {doctor_name_clean}", 0, 1)
        pdf.ln(1)
        
    # Draw Recommended Specialist Box
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(110.9, 128, 90, 58, 'DF')
    
    pdf.set_xy(115.9, 131)
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(80, 5, "Recommended Medical Specialist", 0, 1)
    
    pdf.set_xy(115.9, 140)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(16, 185, 129)
    doctor_name = clean_pdf_text(result.get('recommended_doctor', 'General Physician'))
    pdf.cell(80, 8, f"Specialist: {doctor_name}", 0, 1)
    
    pdf.set_xy(115.9, 150)
    pdf.set_font('helvetica', '', 9.5)
    pdf.set_text_color(71, 85, 105)
    specialist_note = (
        f"We recommend scheduling a clinical consultation with a certified {doctor_name} "
        "for a comprehensive evaluation, diagnostic tests, and personalized treatment planning."
    )
    pdf.multi_cell(80, 4.5, clean_pdf_text(specialist_note), 0, 'L')
    
    # ----------------------------------------------------
    # Actionable Precautions & Guidance Section
    # ----------------------------------------------------
    pdf.set_y(190)
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Actionable Medical Precautions & Self-Care Guidance", 0, 1)
    
    pdf.set_draw_color(16, 185, 129)
    pdf.set_line_width(0.3)
    pdf.line(15, 197, 200, 197)
    
    pdf.ln(3)
    
    precautions = result.get('precautions', [])
    for idx, step in enumerate(precautions):
        pdf.set_x(15)
        # Left boundary color indicator line (drawn manually)
        y_pos = pdf.get_y()
        pdf.set_fill_color(16, 185, 129)
        pdf.rect(15, y_pos + 1, 2.5, 9, 'F')
        
        pdf.set_x(20)
        pdf.set_font('helvetica', 'B', 9.5)
        pdf.set_text_color(16, 185, 129)
        pdf.cell(16, 5, f"Step {idx+1}:", 0, 0)
        
        pdf.set_font('helvetica', '', 9.5)
        pdf.set_text_color(71, 85, 105)
        pdf.multi_cell(164, 5, clean_pdf_text(step), 0, 'L')
        pdf.ln(1)
        
    # Return PDF bytes
    pdf_bytes = bytes(pdf.output())
    return pdf_bytes
