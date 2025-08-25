# Fact Check Agent - Most Important Agent
# Fact checks on multiple sources and gets credibility score, determines true/false
# Has tools to access real-time data from credible sources

import os
import sys
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

from tools.source_checker import SourceChecker
from tools.credibility_calculator import CredibilityCalculator

class FactCheckAgent:
    """
    Most Important Agent - Fact Check Agent
    Fact checks against multiple sources and provides credibility scoring
    Accesses real-time data from credible news outlets, government websites, Twitter, etc.
    """
    
    def __init__(self):
        self.name = "fact_check_agent"
        self.source_checker = SourceChecker()
        self.credibility_calculator = CredibilityCalculator()
        
        self.credible_sources = {
            "news_outlets": [
                "reuters.com", "ap.org", "bbc.com", "npr.org", "pbs.org"
            ],
            "government": [
                "who.int", "cdc.gov", "fda.gov", "whitehouse.gov", "gov.uk"
            ],
            "fact_checkers": [
                "snopes.com", "factcheck.org", "politifact.com", "fullfact.org"
            ],
            "academic": [
                "pubmed.ncbi.nlm.nih.gov", "scholar.google.com", "arxiv.org"
            ],
            "social_verification": [
                "twitter.com/verified", "facebook.com/factcheck"
            ]
        }
        
        self.credibility_weights = {
            "government": 0.9,
            "academic": 0.85,
            "news_outlets": 0.8,
            "fact_checkers": 0.75,
            "social_verification": 0.6
        }
    
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Main fact-checking process"""
        context_data = input_data.get("context_data", {})
        content = input_data.get("content")
        content_type = input_data.get("content_type")
        
        try:
            # Get fact-check targets from context agent
            fact_check_targets = context_data.get("fact_check_targets", [])
            
            if not fact_check_targets:
                return {
                    "status": "no_checkable_claims",
                    "message": "No specific claims identified for fact-checking",
                    "timestamp": get_current_time()
                }
            
            # Process each claim
            claim_results = []
            for target in fact_check_targets:
                claim_result = self.check_claim(target)
                claim_results.append(claim_result)
            
            # Calculate overall credibility
            overall_result = self.credibility_calculator.calculate_overall_credibility(claim_results)
            
            return {
                "status": "completed",
                "overall_verdict": overall_result["verdict"],
                "credibility_score": overall_result["score"],
                "confidence": overall_result["confidence"],
                "is_misinformation": overall_result["is_misinformation"],
                "claim_results": claim_results,
                "sources_checked": overall_result["sources_used"],
                "summary": self.generate_summary(claim_results),
                "timestamp": get_current_time()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": get_current_time()
            }
    
    def check_claim(self, claim_target):
        """Check individual claim against multiple sources"""
        claim_text = claim_target.get("claim_text")
        check_methods = claim_target.get("check_methods", [])
        
        verification_results = []
        
        # Check against different source types
        for method in check_methods:
            result = self.source_checker.check_with_method(claim_text, method)
            if result:
                verification_results.append(result)
        
        # Synthesize results for this claim
        claim_credibility = self.credibility_calculator.synthesize_claim_results(
            verification_results, self.credibility_weights
        )
        
        return {
            "claim_id": claim_target.get("claim_id"),
            "claim_text": claim_text,
            "verification_results": verification_results,
            "credibility_score": claim_credibility["score"],
            "verdict": claim_credibility["verdict"],
            "confidence": claim_credibility["confidence"],
            "supporting_sources": claim_credibility["supporting_sources"],
            "contradicting_sources": claim_credibility["contradicting_sources"]
        }
    
    def generate_summary(self, claim_results):
        """Generate human-readable summary of fact-check results"""
        if not claim_results:
            return "No claims were fact-checked."
        
        verified_claims = sum(1 for claim in claim_results if claim.get("verdict") == "verified")
        disputed_claims = sum(1 for claim in claim_results if claim.get("verdict") == "disputed")
        uncertain_claims = len(claim_results) - verified_claims - disputed_claims
        
        summary = f"Fact-checked {len(claim_results)} claims: "
        summary += f"{verified_claims} verified, {disputed_claims} disputed, {uncertain_claims} uncertain."
        
        return summary

# Example usage
if __name__ == "__main__":
    agent = FactCheckAgent()
    
    # Mock input from preprocessing agent
    mock_input = {
        "context_data": {
            "fact_check_targets": [
                {
                    "claim_id": 1,
                    "claim_text": "Scientists discover breakthrough cure for common cold",
                    "priority": 0.8,
                    "check_methods": ["news_sources", "academic"]
                }
            ]
        },
        "content": "Breaking: Scientists discover breakthrough cure for common cold!",
        "content_type": "text"
    }
    
    result = agent(mock_input)
    print("Fact Check Result:")
    print(result)
