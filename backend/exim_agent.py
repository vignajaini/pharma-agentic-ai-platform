import json, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class EXIMAgent:
    def fetch_trade(self, molecule):
        path = os.path.join(DATA_DIR, "mock_exim.json")
        try:
            with open(path) as f:
                data = json.load(f)
            return data.get(molecule, data.get("default"))
        except:
            return {"exports": 0, "imports": 0}
