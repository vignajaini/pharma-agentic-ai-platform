import json, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class IQVIAAgent:
    def fetch_market(self, molecule):
        path = os.path.join(DATA_DIR, "mock_iqvia.json")
        try:
            with open(path) as f:
                data = json.load(f)
            return data.get(molecule, data.get("default"))
        except:
            return {"market_size": 0, "cagr": 0}
