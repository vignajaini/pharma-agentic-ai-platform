import sys
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from master_agent import MasterAgent

app = Flask(__name__)
CORS(app)

master = MasterAgent()

@app.route("/")
def home():
    return {"status": "Flask backend running"}

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    prompt = data.get("prompt")
    molecule = data.get("molecule")

    result = master.handle_query(prompt, molecule)
    return jsonify(result)

@app.route("/mit/<molecule>", methods=["GET"])
def get_mit(molecule):
    mit = master.get_mit(molecule)
    if not mit:
        return jsonify({"error": "MIT not found"}), 404
    return jsonify(mit)

@app.route("/report/<molecule>", methods=["GET"])
def download_report(molecule):
    """Download PDF report for a molecule"""
    try:
        mit = master.get_mit(molecule)
        if not mit:
            return jsonify({"error": "MIT not found for molecule"}), 404
        
        # Generate the PDF
        pdf_path = master.reporter.generate_pdf_summary(mit)
        
        # Send the file
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{molecule}_report.pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)

