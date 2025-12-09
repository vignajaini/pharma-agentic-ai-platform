from .iqvia_agent import IQVIAAgent
from .exim_agent import EXIMAgent
from .patent_agent import PatentAgent
from .clinical_agent import ClinicalTrialsAgent
from .web_agent import WebAgent
from .internal_insights_agent import InternalInsightsAgent
from .report_generator_agent import ReportGeneratorAgent
from ..mit.mit_builder import MITBuilder

class MasterAgent:
    def __init__(self):
        self.iqvia = IQVIAAgent()
        self.exim = EXIMAgent()
        self.patent = PatentAgent()
        self.clinical = ClinicalTrialsAgent()
        self.web = WebAgent()
        self.internal = InternalInsightsAgent()
        self.reporter = ReportGeneratorAgent()
        self.mit_builder = MITBuilder()
        self.mit_store = {}

    def handle_query(self, prompt, molecule):
        molecule = molecule or self.extract_molecule(prompt) or "Unknown Molecule"

        market = self.iqvia.fetch_market(molecule)
        trade = self.exim.fetch_trade(molecule)
        patents = self.patent.search_patents(molecule)
        trials = self.clinical.search_trials(molecule)
        web = self.web.search(molecule)
        internal = self.internal.summarize_docs(molecule)

        mit = self.mit_builder.build(molecule, market, trade, patents, trials, web, internal)
        self.mit_store[molecule] = mit

        return {
            "molecule": molecule,
            "market": market,
            "trade": trade,
            "patents": patents,
            "trials": trials,
            "web": web,
            "internal": internal,
            "mit": mit,
            "report": self.reporter.generate_pdf_summary(mit)
        }

    def get_mit(self, molecule):
        return self.mit_store.get(molecule)

    def extract_molecule(self, prompt):
        tokens = prompt.split()
        for i, t in enumerate(tokens):
            if t.lower() == "for" and i + 1 < len(tokens):
                return tokens[i+1]
        return None
