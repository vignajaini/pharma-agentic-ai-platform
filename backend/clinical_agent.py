import json, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class ClinicalTrialsAgent:
    def search_trials(self, molecule):
        path = os.path.join(DATA_DIR, "mock_trials.json")
        try:
            with open(path) as f:
                data = json.load(f)
            return data.get(molecule, [])
        except:
            return []
