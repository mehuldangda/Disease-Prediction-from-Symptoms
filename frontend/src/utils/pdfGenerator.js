/**
 * DiagnoWise Health Report PDF Generator
 * Creates a formatted, printable health report document.
 */

export function generateHealthReportPDF(result) {
  if (!result) return;

  const dateStr = new Date().toLocaleString('en-US', {
    dateStyle: 'full',
    timeStyle: 'medium'
  });

  const reportHTML = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>DiagnoWise - Medical Health Assessment Report</title>
      <style>
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1e293b; padding: 40px; margin: 0; background: #fff; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #10b981; padding-bottom: 20px; margin-bottom: 30px; }
        .logo { font-size: 26px; font-weight: 800; color: #0f172a; }
        .logo span { color: #10b981; }
        .timestamp { color: #64748b; font-size: 13px; text-align: right; }
        .card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
        .primary-title { font-size: 28px; font-weight: 800; color: #0f172a; margin: 8px 0; }
        .confidence-badge { display: inline-block; background: #10b981; color: white; padding: 6px 14px; border-radius: 999px; font-weight: 700; font-size: 14px; }
        .risk-badge { display: inline-block; padding: 6px 14px; border-radius: 999px; font-weight: 800; font-size: 12px; text-transform: uppercase; margin-left: 10px; }
        .risk-Low { background: #d1fae5; color: #065f46; }
        .risk-Moderate { background: #fef3c7; color: #92400e; }
        .risk-High { background: #fee2e2; color: #991b1b; }
        .section-title { font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 12px; border-left: 4px solid #10b981; padding-left: 10px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .symptom-tag { display: inline-block; background: #e2e8f0; color: #334155; padding: 4px 10px; border-radius: 6px; font-size: 12px; margin: 3px; }
        .precaution-item { background: #fff; border: 1px solid #cbd5e1; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px; font-size: 14px; }
        .footer { margin-top: 40px; border-top: 1px solid #e2e8f0; pt-20px; padding-top: 20px; color: #94a3b8; font-size: 11px; text-align: center; }
        @media print { body { padding: 20px; } }
      </style>
    </head>
    <body>
      <div class="header">
        <div>
          <div class="logo">Diagno<span>Wise</span> AI</div>
          <div style="font-size: 13px; color: #64748b; margin-top: 4px;">Health Risk Assessment & Disease Prediction Report</div>
        </div>
        <div class="timestamp">
          <div><strong>Report Generated:</strong></div>
          <div>${dateStr}</div>
          <div><strong>Model:</strong> ${result.model_used.replace('_', ' ').toUpperCase()}</div>
        </div>
      </div>

      <div class="card">
        <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #64748b; font-weight: 700;">Primary Diagnostic Inference</div>
        <div class="primary-title">${result.primary_prediction}</div>
        <div style="margin-top: 10px;">
          <span class="confidence-badge">${result.confidence_percentage}% Confidence Score</span>
          <span class="risk-badge risk-${result.severity.includes('High') ? 'High' : (result.severity.includes('Low') ? 'Low' : 'Moderate')}">${result.severity} Risk</span>
        </div>
        <p style="color: #475569; font-size: 14px; line-height: 1.6; margin-top: 14px;">${result.description}</p>
      </div>

      <div class="card">
        <div class="section-title">Evaluated Symptoms (${result.matched_symptoms_count})</div>
        <div>
          ${(result.matched_symptoms || []).map(s => `<span class="symptom-tag">✓ ${s.replace(/_/g, ' ')}</span>`).join('')}
        </div>
      </div>

      <div class="grid">
        <div class="card">
          <div class="section-title">Top Differential Diagnoses</div>
          ${(result.top_3_predictions || []).map((item, idx) => `
            <div style="margin-bottom: 12px; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
              <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 14px;">
                <span>#${idx + 1} ${item.disease}</span>
                <span style="color: #10b981;">${item.probability}%</span>
              </div>
              <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Recommended Specialist: ${item.doctor}</div>
            </div>
          `).join('')}
        </div>

        <div class="card">
          <div class="section-title">Recommended Specialist</div>
          <div style="font-size: 20px; font-weight: 800; color: #0f172a; margin-top: 6px;">👨‍⚕️ ${result.recommended_doctor}</div>
          <p style="font-size: 13px; color: #64748b; margin-top: 6px;">Consult a certified ${result.recommended_doctor} for complete clinical evaluation and diagnostic testing.</p>
        </div>
      </div>

      <div class="card">
        <div class="section-title">Actionable Precautions & Guidance</div>
        ${(result.precautions || []).map((step, idx) => `
          <div class="precaution-item"><strong>Step ${idx + 1}:</strong> ${step}</div>
        `).join('')}
      </div>

      <div class="footer">
        <p><strong>DiagnoWise Health Risk Assessment Engine</strong> • B.Tech Final Year Project & Portfolio Project</p>
        <p style="margin-top: 4px;">CONFIDENTIAL MEDICAL REPORT SUMMARY. THIS REPORT IS FOR INFORMATIONAL & DECISION-SUPPORT PURPOSES ONLY.</p>
      </div>

      <script>
        window.onload = function() {
          window.print();
        };
      </script>
    </body>
    </html>
  `;

  const printWindow = window.open('', '_blank');
  printWindow.document.write(reportHTML);
  printWindow.document.close();
}
