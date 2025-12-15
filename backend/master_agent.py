from iqvia_agent import IQVIAAgent
from exim_agent import EXIMAgent
from patent_agent import PatentAgent
from clinical_agent import ClinicalTrialsAgent
from web_agent import WebAgent
from internal_insights_agent import InternalInsightsAgent
from report_generator_agent import ReportGeneratorAgent

# Import MITBuilder by directly importing the class and its dependency
import sys
import os
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

# Add MIT directory to path
mit_path = os.path.join(os.path.dirname(__file__), 'mit')
sys.path.insert(0, mit_path)

from innovation_score import compute_innovation_score

class MITBuilder:
    """Builds comprehensive Molecule Innovation Twin profiles"""
    
    def build(self, molecule, market, trade, patents, trials, web, internal):
        """
        Build a complete MIT profile from all agent data
        
        Args:
            molecule: Molecule name
            market: Market data from IQVIA agent
            trade: Trade data from EXIM agent
            patents: Patent data from Patent agent
            trials: Clinical trial data
            web: Web research data
            internal: Internal insights
        
        Returns:
            Dictionary containing complete MIT profile
        """
        profile = {
            "molecule": molecule,
            "market": market,
            "trade": trade,
            "patents": patents,
            "trials": trials,
            "web": web,
            "internal": internal,
            "highlights": [],
            "metadata": {
                "created_at": datetime.utcnow().isoformat(),
                "agents_used": 7
            }
        }

        # Build highlights from available data
        if market:
            if isinstance(market, dict) and market.get('market_size'):
                profile["highlights"].append(f"Market size: ${market.get('market_size'):,.0f}")
            
            if isinstance(market, dict) and market.get('cagr'):
                profile["highlights"].append(f"CAGR: {market.get('cagr'):.1f}%")

        if patents and len(patents) > 0:
            profile["highlights"].append(f"{len(patents)} patent documents identified")
            active_patents = [p for p in patents if isinstance(p, dict) and p.get('status') != 'expired']
            profile["highlights"].append(f"{len(active_patents)} active patents")

        if trials and len(trials) > 0:
            profile["highlights"].append(f"{len(trials)} clinical trials found")
            phases = set()
            for trial in trials:
                if isinstance(trial, dict) and trial.get('phase'):
                    phases.add(trial.get('phase'))
            if phases:
                profile["highlights"].append(f"Phases: {', '.join(sorted(phases))}")

        if web:
            web_items = web.get('top_papers', []) if isinstance(web, dict) else []
            if len(web_items) > 0:
                profile["highlights"].append(f"{len(web_items)} research papers found")

        # Compute innovation score
        profile["innovation_score"] = compute_innovation_score(profile)
        
        return profile


class MasterAgent:
    """Master orchestration agent coordinating all worker agents"""
    
    def __init__(self):
        """Initialize all worker agents"""
        self.iqvia = IQVIAAgent()
        self.exim = EXIMAgent()
        self.patent = PatentAgent()
        self.clinical = ClinicalTrialsAgent()
        self.web = WebAgent()
        self.internal = InternalInsightsAgent()
        self.reporter = ReportGeneratorAgent()
        self.mit_builder = MITBuilder()
        
        # Storage for MIT results
        self.mit_store = {}
        self.query_history = []
        
        logger.info("MasterAgent initialized with all worker agents")

    def handle_query(self, prompt, molecule):
        """
        Handle a complete molecule analysis query
        
        Args:
            prompt: User query/prompt
            molecule: Molecule name to analyze
        
        Returns:
            Dictionary with analysis results from all agents
        """
        start_time = time.time()
        
        # Extract molecule if not provided
        if not molecule:
            molecule = self.extract_molecule(prompt) or "Unknown Molecule"
        
        logger.info(f"Processing query for molecule: {molecule}")
        
        # Sanitize molecule name
        molecule = molecule.strip().title()
        
        try:
            # Fetch data from all agents in parallel fashion
            market = self._safe_call(self.iqvia.fetch_market, molecule, agent_name="IQVIA Market")
            trade = self._safe_call(self.exim.fetch_trade, molecule, agent_name="EXIM Trade")
            patents = self._safe_call(self.patent.search_patents, molecule, agent_name="Patent")
            trials = self._safe_call(self.clinical.search_trials, molecule, agent_name="Clinical")
            web = self._safe_call(self.web.search, molecule, agent_name="Web")
            internal = self._safe_call(self.internal.summarize_docs, molecule, agent_name="Internal")

            # Build MIT profile
            mit = self.mit_builder.build(molecule, market, trade, patents, trials, web, internal)
            
            # Store MIT for later retrieval
            self.mit_store[molecule] = mit
            
            # Generate report
            report_path = self._safe_call(
                self.reporter.generate_pdf_summary, 
                mit, 
                "Report Generation"
            )
            
            # Compile results
            result = {
                "molecule": molecule,
                "market": market or {},
                "trade": trade or {},
                "patents": patents or [],
                "trials": trials or [],
                "web": web or {},
                "internal": internal or {},
                "mit": mit,
                "report": report_path,
                "processing_time_seconds": round(time.time() - start_time, 2),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Store in history
            self.query_history.append({
                "molecule": molecule,
                "prompt": prompt[:100],  # Store first 100 chars
                "timestamp": result["timestamp"],
                "processing_time": result["processing_time_seconds"]
            })
            
            logger.info(f"Query completed for {molecule} in {result['processing_time_seconds']}s")
            return result
            
        except Exception as e:
            logger.error(f"Error processing query for {molecule}: {str(e)}")
            raise

    def get_mit(self, molecule):
        """
        Retrieve stored MIT for a molecule
        
        Args:
            molecule: Molecule name
        
        Returns:
            MIT profile dictionary or None
        """
        molecule = molecule.strip().title()
        return self.mit_store.get(molecule)

    def get_query_history(self):
        """Get analysis history"""
        return self.query_history

    def clear_history(self):
        """Clear analysis history and storage"""
        self.mit_store.clear()
        self.query_history.clear()
        logger.info("History and storage cleared")

    def extract_molecule(self, prompt):
        """
        Extract molecule name from prompt using simple NLP
        
        Args:
            prompt: User prompt text
        
        Returns:
            Extracted molecule name or None
        """
        keywords = ["for", "about", "molecule", "drug", "compound"]
        tokens = prompt.split()
        
        for i, token in enumerate(tokens):
            if token.lower() in keywords and i + 1 < len(tokens):
                return tokens[i + 1]
        
        return None

    def _safe_call(self, func, *args, agent_name="Unknown"):
        """
        Safely call an agent function with error handling
        
        Args:
            func: Function to call
            args: Arguments to pass
            agent_name: Name of the agent for logging
        
        Returns:
            Function result or None if error occurs
        """
        try:
            logger.debug(f"Calling {agent_name} agent")
            result = func(*args)
            logger.debug(f"{agent_name} agent completed successfully")
            return result
        except Exception as e:
            logger.warning(f"Error in {agent_name} agent: {str(e)}")
            return None
