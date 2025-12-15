"""
PDF Parser for extracting insights from internal company documents
"""
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PDFParser:
    """Parses uploaded PDFs and extracts key insights"""
    
    def __init__(self):
        self.upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def parse_pdf(self, file_path, molecule=None):
        """
        Parse PDF and extract key information
        
        Args:
            file_path: Path to uploaded PDF
            molecule: Optional molecule name for context
            
        Returns:
            Dictionary with extracted insights
        """
        try:
            # For now, extract basic file info and simulate content parsing
            # In production, use PyPDF2 or pdfplumber for actual extraction
            
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                return None
            
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            
            # Simulate PDF content extraction
            insights = {
                "file_name": file_name,
                "file_size": file_size,
                "parsed_date": datetime.utcnow().isoformat(),
                "molecule": molecule,
                "key_findings": self._extract_key_findings(file_path),
                "unmet_needs": self._extract_unmet_needs(file_path),
                "recommendations": self._extract_recommendations(file_path)
            }
            
            logger.info(f"Successfully parsed PDF: {file_name}")
            return insights
            
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            return None
    
    def _extract_key_findings(self, file_path):
        """Extract key findings from PDF"""
        # Simulated key findings
        return [
            "Strong market potential identified",
            "Competitive landscape analysis complete",
            "Regulatory pathway clear for new indication"
        ]
    
    def _extract_unmet_needs(self, file_path):
        """Extract unmet needs from document"""
        return [
            "Limited treatment options for resistant cases",
            "Patient compliance issues with current therapy",
            "Safety concerns with existing alternatives"
        ]
    
    def _extract_recommendations(self, file_path):
        """Extract recommendations from document"""
        return [
            "Consider combination therapy approach",
            "Target patient population: 50+ with comorbidities",
            "Timeline: 18-24 months for Phase 2 initiation"
        ]
    
    def save_upload(self, file_obj, molecule):
        """
        Save uploaded file to storage
        
        Args:
            file_obj: File object from request
            molecule: Molecule name for file naming
            
        Returns:
            Saved file path
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{molecule}_{timestamp}.pdf"
            file_path = os.path.join(self.upload_dir, filename)
            
            file_obj.save(file_path)
            logger.info(f"File uploaded: {filename}")
            
            return file_path
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return None
    
    def get_upload_history(self, molecule=None):
        """Get history of uploaded documents"""
        try:
            uploads = []
            for filename in os.listdir(self.upload_dir):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(self.upload_dir, filename)
                    file_stat = os.stat(file_path)
                    
                    if molecule is None or molecule.lower() in filename.lower():
                        uploads.append({
                            "filename": filename,
                            "size": file_stat.st_size,
                            "uploaded": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                        })
            
            return sorted(uploads, key=lambda x: x['uploaded'], reverse=True)
        except Exception as e:
            logger.error(f"Error getting upload history: {str(e)}")
            return []
