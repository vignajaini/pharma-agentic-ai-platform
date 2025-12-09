from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.master_agent import MasterAgent

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

if __name__ == "__main__":
    app.run(debug=True, port=8000)

