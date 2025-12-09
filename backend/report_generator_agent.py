import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime

REPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "storage", "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

class ReportGeneratorAgent:
    def generate_pdf_summary(self, mit):
        filename = f"{mit['molecule']}_summary_{datetime.datetime.utcnow().timestamp()}.pdf"
        path = os.path.join(REPORT_DIR, filename)

        c = canvas.Canvas(path, pagesize=letter)
        c.setFont("Helvetica", 12)

        c.drawString(50, 750, f"Molecule: {mit['molecule']}")
        c.drawString(50, 730, f"Innovation Score: {mit.get('innovation_score', 'N/A')}")
        c.drawString(50, 710, "Highlights:")

        y = 690
        for item in mit.get("highlights", []):
            c.drawString(60, y, f"- {item}")
            y -= 15

        c.save()
        return path
