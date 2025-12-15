"""
FTO Risk Assessor - Freedom to Operate patent analysis
"""
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FTOAssessor:
    """Assesses Freedom to Operate risks based on patent landscape"""
    
    def __init__(self):
        self.risk_thresholds = {
            'high': (70, 100),
            'medium': (40, 69),
            'low': (0, 39)
        }
    
    def assess_fto_risk(self, molecule, patent_data, trade_data=None):
        """
        Assess Freedom to Operate risks
        
        Args:
            molecule: Molecule name
            patent_data: Patent information from Patent Agent
            trade_data: Trade data for market context
            
        Returns:
            Dictionary with FTO risk assessment
        """
        fto_analysis = {
            "molecule": molecule,
            "overall_fto_risk_score": 0,
            "risk_level": "Unknown",
            "patent_threats": [],
            "expiry_timeline": {},
            "recommendations": [],
            "confidence": 85
        }
        
        if patent_data and len(patent_data) > 0:
            # Analyze patent landscape
            fto_analysis["patent_threats"] = self._identify_patent_threats(patent_data)
            fto_analysis["expiry_timeline"] = self._analyze_expiry_timeline(patent_data)
            fto_analysis["overall_fto_risk_score"] = self._calculate_risk_score(
                patent_data,
                fto_analysis["patent_threats"]
            )
        else:
            # If no patent data, assume moderate risk
            fto_analysis["overall_fto_risk_score"] = 45
        
        # Determine risk level
        risk_score = fto_analysis["overall_fto_risk_score"]
        for level, (min_val, max_val) in self.risk_thresholds.items():
            if min_val <= risk_score <= max_val:
                fto_analysis["risk_level"] = level.upper()
                break
        
        # Generate recommendations
        fto_analysis["recommendations"] = self._generate_recommendations(
            fto_analysis["risk_level"],
            fto_analysis["patent_threats"]
        )
        
        logger.info(f"FTO Assessment for {molecule}: Risk Score {risk_score}, Level {fto_analysis['risk_level']}")
        return fto_analysis
    
    def _identify_patent_threats(self, patent_data):
        """Identify active patent threats"""
        threats = []
        
        today = datetime.now()
        
        for i, patent in enumerate(patent_data):
            if not isinstance(patent, dict):
                continue
            
            patent_id = patent.get('patent_id', f'Patent_{i}')
            expiry = patent.get('expiry_date')
            status = patent.get('status', 'Unknown')
            claims = patent.get('claims', [])
            
            # Check if patent is still active
            is_active = status.lower() in ['active', 'granted', 'in force']
            
            # Parse expiry date
            if expiry:
                try:
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                    years_remaining = (expiry_date - today).days / 365.25
                    is_expired = years_remaining <= 0
                except:
                    is_expired = False
                    years_remaining = 0
            else:
                is_expired = False
                years_remaining = 0
            
            if is_active and not is_expired and years_remaining > 0:
                threat_severity = 'HIGH' if years_remaining > 3 else 'MEDIUM'
                
                threats.append({
                    "patent_id": patent_id,
                    "owner": patent.get('owner', 'Unknown'),
                    "expiry_date": expiry,
                    "years_remaining": round(years_remaining, 1),
                    "threat_severity": threat_severity,
                    "claims_count": len(claims) if claims else 0,
                    "risk_overlap": self._assess_claim_overlap(claims)
                })
        
        return sorted(threats, key=lambda x: x['years_remaining'], reverse=True)
    
    def _assess_claim_overlap(self, claims):
        """Assess how much patent claims overlap with our molecule"""
        if not claims:
            return "Unknown"
        
        # Simulate claim overlap assessment
        overlap_score = min(len(claims) * 15, 100)  # Higher claims = higher risk
        
        if overlap_score > 70:
            return "HIGH"
        elif overlap_score > 40:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _analyze_expiry_timeline(self, patent_data):
        """Analyze patent expiry timeline"""
        timeline = {
            "near_term": [],  # 0-3 years
            "medium_term": [],  # 3-7 years
            "long_term": []  # 7+ years
        }
        
        today = datetime.now()
        
        for patent in patent_data:
            if not isinstance(patent, dict):
                continue
            
            expiry = patent.get('expiry_date')
            if not expiry:
                continue
            
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                years_remaining = (expiry_date - today).days / 365.25
                
                patent_summary = {
                    "patent_id": patent.get('patent_id', 'Unknown'),
                    "expiry_date": expiry,
                    "years_remaining": round(years_remaining, 1)
                }
                
                if 0 <= years_remaining <= 3:
                    timeline["near_term"].append(patent_summary)
                elif 3 < years_remaining <= 7:
                    timeline["medium_term"].append(patent_summary)
                else:
                    timeline["long_term"].append(patent_summary)
            except:
                pass
        
        return timeline
    
    def _calculate_risk_score(self, patent_data, threats):
        """Calculate overall FTO risk score (0-100)"""
        score = 20  # Base score (default risk)
        
        # Add risk from active threats
        score += len(threats) * 8
        
        # Add risk from patents with high claim counts
        for patent in patent_data:
            if isinstance(patent, dict):
                claims = patent.get('claims', [])
                if len(claims) > 20:
                    score += 5
        
        # Reduce risk if patents expiring soon
        for threat in threats:
            if threat.get('years_remaining', 0) < 2:
                score -= 5
        
        # Cap at 100
        score = min(max(score, 0), 100)
        return score
    
    def _generate_recommendations(self, risk_level, threats):
        """Generate FTO mitigation recommendations"""
        recommendations = []
        
        if risk_level == "HIGH":
            recommendations = [
                "High FTO Risk Detected - Recommend immediate patent counsel review",
                "Consider designing around key patents",
                "Evaluate licensing agreements with patent holders",
                "Monitor patent prosecution for prosecution history",
                "Develop contingency formulation strategies"
            ]
        elif risk_level == "MEDIUM":
            recommendations = [
                "Moderate FTO Risk - Recommend patent landscape monitoring",
                "Consider cross-licensing opportunities",
                "Develop alternative formulation backup",
                "Track competitor product launches",
                "Plan for potential patent challenges"
            ]
        else:  # LOW
            recommendations = [
                "Low FTO Risk - Proceed with development",
                "Continue patent monitoring for new filings",
                "Consider filing own patents for improvement",
                "Evaluate blocking patent opportunities",
                "Document prior art and design rationale"
            ]
        
        # Add specific threat-based recommendations
        if threats and len(threats) > 0:
            longest_patent = threats[0]
            recommendations.append(
                f"Key Patent Threat: {longest_patent['patent_id']} expires in "
                f"{longest_patent['years_remaining']} years"
            )
        
        return recommendations
    
    def get_fto_summary(self, fto_analysis):
        """Generate executive summary of FTO assessment"""
        return {
            "molecule": fto_analysis.get('molecule'),
            "risk_score": fto_analysis.get('overall_fto_risk_score'),
            "risk_level": fto_analysis.get('risk_level'),
            "active_threats": len(fto_analysis.get('patent_threats', [])),
            "recommendation": fto_analysis.get('recommendations', [])[0] if fto_analysis.get('recommendations') else "No recommendation",
            "next_steps": [
                "Conduct detailed patent landscaping analysis",
                "Engage patent counsel for FTO opinion",
                "Develop mitigation strategy",
                "Plan design-around options if needed"
            ]
        }
