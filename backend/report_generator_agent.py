import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime

# Get the absolute path to the storage/reports directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
REPORT_DIR = os.path.join(PROJECT_ROOT, "storage", "reports")

# Create directory if it doesn't exist
os.makedirs(REPORT_DIR, exist_ok=True)

class ReportGeneratorAgent:
    def generate_pdf_summary(self, mit):
        """Generate a PDF summary of the MIT analysis"""
        try:
            # Create filename with sanitized molecule name
            molecule_name = mit.get('molecule', 'Unknown').replace(' ', '_').replace('/', '_')
            timestamp = str(int(datetime.datetime.utcnow().timestamp()))
            filename = f"{molecule_name}_summary_{timestamp}.pdf"
            filepath = os.path.join(REPORT_DIR, filename)
            
            # Create the PDF
            c = canvas.Canvas(filepath, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, "Molecule Innovation Twin (MIT) Report")
            
            c.setFont("Helvetica", 12)
            c.drawString(50, 730, f"Molecule: {mit.get('molecule', 'N/A')}")
            c.drawString(50, 710, f"Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
            # Innovation Score
            if 'innovation_score' in mit:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, 690, f"Innovation Score: {mit['innovation_score']:.2f}/100")
                c.setFont("Helvetica", 10)
            
            # Highlights
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, 670, "Key Highlights:")
            c.setFont("Helvetica", 10)
            
            y = 650
            for item in mit.get("highlights", []):
                c.drawString(70, y, f"• {item}")
                y -= 20
            
            # Market Summary
            if mit.get('market'):
                y -= 10
                c.setFont("Helvetica-Bold", 11)
                c.drawString(50, y, "Market Data:")
                c.setFont("Helvetica", 10)
                y -= 15
                market = mit['market']
                if isinstance(market, dict):
                    for key, value in market.items():
                        if key != 'regions':
                            c.drawString(70, y, f"{key}: {value}")
                            y -= 15
            
            c.save()
            return filepath
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            raise
