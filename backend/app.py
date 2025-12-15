import sys
import os
import logging
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime

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

