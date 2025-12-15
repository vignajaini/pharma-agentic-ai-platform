import sys
import os
import logging
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from master_agent import MasterAgent
from utils import CacheManager, RequestValidator, ResponseFormatter, handle_errors
from config import API_CONFIG, STORAGE_PATHS

# Setup logging
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# File upload config
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}

# Initialize services
master = MasterAgent()
cache = CacheManager(ttl=API_CONFIG.get('CACHE_TTL', 3600))
validator = RequestValidator()
formatter = ResponseFormatter()

# API Version
API_VERSION = "1.0.0"

@app.route("/", methods=["GET"])
def home():
    """Health check and API info endpoint"""
    return formatter.success({
        "service": "Pharma Agentic AI Platform Backend",
        "version": API_VERSION,
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }, "Backend is operational")

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/api/v1/query", methods=["POST"])
@app.route("/query", methods=["POST"])  # Backward compatibility
@handle_errors
def query():
    """
    Analyze a molecule across all agents
    
    Request body:
    {
        "molecule": "string (required)",
        "prompt": "string (required)"
    }
    """
    # Validate request
    data = request.get_json()
    
    # Request validation
    validation_errors = validator.validate_query(data)
    if validation_errors:
        return formatter.validation_error(validation_errors)
    
    molecule = data.get("molecule")
    prompt = data.get("prompt")
    
    # Log request
    if API_CONFIG.get('LOG_REQUESTS'):
        logger.info(f"Query received - Molecule: {molecule}, Prompt length: {len(prompt)}")
    
    # Check cache
    if API_CONFIG.get('CACHE_ENABLED'):
        cached_result = cache.get(molecule, prompt)
        if cached_result:
            return formatter.success(cached_result, "Results from cache")
    
    try:
        # Process query
        result = master.handle_query(prompt, molecule)
        
        # Cache result
        if API_CONFIG.get('CACHE_ENABLED'):
            cache.set(molecule, prompt, result)
        
        logger.info(f"Query successful - Molecule: {molecule}")
        return formatter.success(result, "Analysis complete")
    
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        return formatter.error(f"Failed to process query: {str(e)}", 500)

@app.route("/api/v1/mit/<molecule>", methods=["GET"])
@app.route("/mit/<molecule>", methods=["GET"])  # Backward compatibility
@handle_errors
def get_mit(molecule):
    """
    Retrieve MIT (Molecule Innovation Twin) for a molecule
    
    Parameters:
    - molecule: string (required)
    """
    # Validate molecule name
    if not validator.validate_molecule_name(molecule):
        return formatter.error("Invalid molecule name format", 400)
    
    logger.info(f"MIT retrieval requested - Molecule: {molecule}")
    
    mit = master.get_mit(molecule)
    if not mit:
        logger.warning(f"MIT not found for molecule: {molecule}")
        return formatter.error(f"No MIT found for molecule: {molecule}", 404)
    
    return formatter.success(mit, f"MIT retrieved for {molecule}")

@app.route("/api/v1/report/<molecule>", methods=["GET"])
@app.route("/report/<molecule>", methods=["GET"])  # Backward compatibility
@handle_errors
def download_report(molecule):
    """
    Download PDF report for a molecule
    
    Parameters:
    - molecule: string (required)
    """
    # Validate molecule name
    if not validator.validate_molecule_name(molecule):
        return formatter.error("Invalid molecule name format", 400)
    
    logger.info(f"Report download requested - Molecule: {molecule}")
    
    try:
        mit = master.get_mit(molecule)
        if not mit:
            return formatter.error(f"No MIT found for molecule: {molecule}", 404)
        
        # Generate the PDF
        pdf_path = master.reporter.generate_pdf_summary(mit)
        
        if not os.path.exists(pdf_path):
            return formatter.error("Failed to generate report", 500)
        
        logger.info(f"Report generated successfully - Molecule: {molecule}")
        
        # Send the file
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{molecule}_report.pdf'
        )
    except Exception as e:
        logger.error(f"Report generation error: {str(e)}")
        return formatter.error(f"Failed to generate report: {str(e)}", 500)

@app.route("/api/v1/cache/stats", methods=["GET"])
def cache_stats():
    """Get cache statistics"""
    return formatter.success(cache.get_stats(), "Cache statistics")

@app.route("/api/v1/cache/clear", methods=["POST"])
def clear_cache():
    """Clear all cached results"""
    cache.clear()
    logger.info("Cache cleared via API")
    return formatter.success({"cleared": True}, "Cache cleared successfully")

@app.route("/api/v1/agents", methods=["GET"])
def list_agents():
    """List all available agents"""
    agents = {
        "market": "IQVIA Agent - Market data and size",
        "trade": "EXIM Agent - Import/export flows",
        "patents": "Patent Agent - Patent information",
        "trials": "Clinical Trials Agent - Research status",
        "web": "Web Agent - External research",
        "internal": "Internal Insights Agent - Company knowledge",
        "report": "Report Generator - PDF generation"
    }
    return formatter.success(agents, "Available agents")

# Error handlers
@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return formatter.error("Endpoint not found", 404)

@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 errors"""
    return formatter.error("Method not allowed", 405)

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(e)}")
    return formatter.error("Internal server error", 500)

# ========== FILE UPLOAD ENDPOINTS ==========

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/v1/upload", methods=["POST"])
@app.route("/upload", methods=["POST"])
@handle_errors
def upload_file():
    """
    Upload internal document (PDF/TXT) for analysis
    
    Request:
    - multipart/form-data with:
      - file: PDF or document file
      - molecule: (optional) molecule name for context
    """
    # Check if file is in request
    if 'file' not in request.files:
        return formatter.error("No file part in request", 400)
    
    file = request.files['file']
    molecule = request.form.get('molecule', 'Unknown')
    
    if file.filename == '':
        return formatter.error("No file selected", 400)
    
    if not allowed_file(file.filename):
        return formatter.error("File type not allowed. Allowed: PDF, TXT, DOC, DOCX", 400)
    
    try:
        # Save file
        filename = secure_filename(f"{molecule}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse PDF
        parsed_insights = master.pdf_parser.parse_pdf(filepath, molecule)
        
        logger.info(f"File uploaded and parsed: {filename}")
        return formatter.success({
            "filename": filename,
            "molecule": molecule,
            "insights": parsed_insights
        }, "File uploaded and analyzed successfully")
        
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        return formatter.error(f"File upload failed: {str(e)}", 500)

@app.route("/api/v1/uploads/<molecule>", methods=["GET"])
@app.route("/uploads/<molecule>", methods=["GET"])
@handle_errors
def get_uploads(molecule):
    """Get upload history for a molecule"""
    try:
        uploads = master.pdf_parser.get_upload_history(molecule)
        return formatter.success({
            "molecule": molecule,
            "uploads": uploads,
            "total": len(uploads)
        }, f"Upload history for {molecule}")
    except Exception as e:
        logger.error(f"Error retrieving uploads: {str(e)}")
        return formatter.error(f"Failed to retrieve uploads: {str(e)}", 500)

# ========== UNMET NEEDS ENDPOINTS ==========

@app.route("/api/v1/unmet-needs/<molecule>", methods=["GET"])
@app.route("/unmet-needs/<molecule>", methods=["GET"])
@handle_errors
def analyze_unmet_needs(molecule):
    """Get unmet needs analysis for a molecule"""
    try:
        # Get existing MIT data or perform fresh analysis
        if molecule in master.mit_store:
            mit = master.mit_store[molecule]
            unmet_needs = master.unmet_needs_analyzer.analyze_unmet_needs(
                mit.get('market'),
                mit.get('trials'),
                mit.get('patents'),
                mit.get('web')
            )
            summary = master.unmet_needs_analyzer.get_opportunity_summary(unmet_needs)
            
            return formatter.success({
                "molecule": molecule,
                "unmet_needs": unmet_needs,
                "opportunity_summary": summary
            }, "Unmet needs analysis complete")
        else:
            return formatter.error(f"No data found for {molecule}. Run query first.", 404)
    
    except Exception as e:
        logger.error(f"Unmet needs analysis error: {str(e)}")
        return formatter.error(f"Analysis failed: {str(e)}", 500)

# ========== FTO RISK ENDPOINTS ==========

@app.route("/api/v1/fto-risk/<molecule>", methods=["GET"])
@app.route("/fto-risk/<molecule>", methods=["GET"])
@handle_errors
def assess_fto_risk(molecule):
    """Get FTO risk assessment for a molecule"""
    try:
        # Get existing MIT data
        if molecule in master.mit_store:
            mit = master.mit_store[molecule]
            fto_analysis = master.fto_assessor.assess_fto_risk(
                molecule,
                mit.get('patents', []),
                mit.get('trade')
            )
            summary = master.fto_assessor.get_fto_summary(fto_analysis)
            
            return formatter.success({
                "molecule": molecule,
                "fto_analysis": fto_analysis,
                "fto_summary": summary
            }, "FTO risk assessment complete")
        else:
            return formatter.error(f"No data found for {molecule}. Run query first.", 404)
    
    except Exception as e:
        logger.error(f"FTO risk assessment error: {str(e)}")
        return formatter.error(f"Assessment failed: {str(e)}", 500)

# ========== BATCH ANALYSIS ENDPOINTS ==========

@app.route("/api/v1/batch-analyze", methods=["POST"])
@app.route("/batch-analyze", methods=["POST"])
@handle_errors
def batch_analyze():
    """
    Analyze multiple molecules at once
    
    Request body:
    {
        "molecules": ["mol1", "mol2", "mol3"],
        "prompt": "analysis prompt"
    }
    """
    data = request.get_json()
    molecules = data.get('molecules', [])
    prompt = data.get('prompt', 'Analyze molecule')
    
    if not molecules or not isinstance(molecules, list):
        return formatter.error("molecules must be a non-empty list", 400)
    
    if len(molecules) > 10:
        return formatter.error("Maximum 10 molecules per batch", 400)
    
    try:
        results = []
        for molecule in molecules:
            result = master.handle_query(prompt, molecule)
            results.append({
                "molecule": molecule,
                "innovation_score": result.get('mit', {}).get('innovation_score', 0),
                "status": "completed"
            })
        
        logger.info(f"Batch analysis completed for {len(molecules)} molecules")
        return formatter.success({
            "total_molecules": len(molecules),
            "results": results
        }, "Batch analysis complete")
        
    except Exception as e:
        logger.error(f"Batch analysis error: {str(e)}")
        return formatter.error(f"Batch analysis failed: {str(e)}", 500)

# Request/Response logging middleware
@app.before_request
def log_request():
    """Log incoming requests"""
    if API_CONFIG.get('LOG_REQUESTS'):
        logger.debug(f"Request: {request.method} {request.path}")

@app.after_request
def log_response(response):
    """Log outgoing responses"""
    if API_CONFIG.get('LOG_REQUESTS'):
        logger.debug(f"Response: {response.status_code} {request.path}")
    return response

if __name__ == "__main__":
    logger.info("Starting Pharma Agentic AI Platform Backend")
    app.run(debug=True, port=8000)

