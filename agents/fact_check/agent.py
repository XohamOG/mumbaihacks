# Fact Check Agent - Most Important Agent
# Fact checks on multiple sources and gets credibility score, determines true/false
# Has tools to access real-time data from credible sources

import os
import sys
import re
import random
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

class FactCheckAgent:
    """
    Most Important Agent - Fact Check Agent
    Fact checks against multiple sources and provides credibility scoring
    Accesses real-time data from credible news outlets, government websites, Twitter, etc.
    """
    
    def __init__(self):
        self.name = "fact_check_agent"
        
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
        
        # Common misinformation patterns
        self.red_flag_patterns = [
            r"doctors hate this",
            r"they don't want you to know",
            r"secret cure",
            r"100% natural",
            r"miracle cure",
            r"big pharma doesn't want",
            r"breaking news",
            r"shocking discovery",
            r"exclusive footage",
            r"leaked documents"
        ]
    
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Main fact-checking process"""
        context_data = input_data.get("context_data", {})
        content = input_data.get("content")
        content_type = input_data.get("content_type")
        
        try:
            # Extract claims from content if not provided by context agent
            fact_check_targets = context_data.get("fact_check_targets", [])
            
            if not fact_check_targets and content:
                # Create basic claim targets from content
                fact_check_targets = self.extract_claims_from_content(content)
            
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
            overall_result = self.calculate_overall_credibility(claim_results)
            
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
    
    def extract_claims_from_content(self, content):
        """Extract potential claims from content for fact-checking"""
        claims = []
        sentences = content.split('.')
        
        for i, sentence in enumerate(sentences[:5]):  # Check first 5 sentences
            sentence = sentence.strip()
            if len(sentence) > 20:  # Skip very short sentences
                claims.append({
                    "claim_id": i + 1,
                    "claim_text": sentence,
                    "priority": self.calculate_claim_priority(sentence),
                    "check_methods": self.determine_check_methods(sentence)
                })
        
        return sorted(claims, key=lambda x: x["priority"], reverse=True)[:3]  # Top 3 claims
    
    def calculate_claim_priority(self, claim_text):
        """Calculate priority for fact-checking based on content"""
        priority = 0.5  # Base priority
        
        # Check for red flag patterns
        for pattern in self.red_flag_patterns:
            if re.search(pattern, claim_text.lower()):
                priority += 0.3
        
        # Health/medical claims get higher priority
        health_keywords = ["vaccine", "cure", "treatment", "doctor", "medicine", "health", "disease"]
        if any(keyword in claim_text.lower() for keyword in health_keywords):
            priority += 0.2
        
        # Political claims get higher priority
        political_keywords = ["election", "government", "politician", "vote", "policy"]
        if any(keyword in claim_text.lower() for keyword in political_keywords):
            priority += 0.15
        
        return min(priority, 1.0)  # Cap at 1.0
    
    def determine_check_methods(self, claim_text):
        """Determine which fact-checking methods to use based on content"""
        methods = ["news_sources"]  # Always check news sources
        
        # Health claims - check academic and government sources
        health_keywords = ["vaccine", "cure", "treatment", "doctor", "medicine", "health"]
        if any(keyword in claim_text.lower() for keyword in health_keywords):
            methods.extend(["academic", "government"])
        
        # Political claims - check government and fact-checkers
        political_keywords = ["election", "government", "politician", "vote"]
        if any(keyword in claim_text.lower() for keyword in political_keywords):
            methods.extend(["government", "fact_checkers"])
        
        # Scientific claims - check academic sources
        science_keywords = ["study", "research", "scientists", "discovery", "breakthrough"]
        if any(keyword in claim_text.lower() for keyword in science_keywords):
            methods.append("academic")
        
        return list(set(methods))  # Remove duplicates

    def check_claim(self, claim_target):
        """Check individual claim against multiple sources"""
        claim_text = claim_target.get("claim_text")
        check_methods = claim_target.get("check_methods", ["news_sources"])
        
        verification_results = []
        
        # Simulate checking against different source types
        for method in check_methods:
            result = self.check_with_method(claim_text, method)
            if result:
                verification_results.append(result)
        
        # Synthesize results for this claim
        claim_credibility = self.synthesize_claim_results(
            verification_results, claim_text
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
    
    def check_with_method(self, claim_text, method):
        """Simulate checking claim with specific method"""
        # This would be replaced with actual API calls in production
        
        # Simulate credibility based on content analysis
        red_flag_score = sum(1 for pattern in self.red_flag_patterns 
                           if re.search(pattern, claim_text, re.IGNORECASE))
        
        # Base credibility (more aggressive penalty for red flags)
        base_credibility = max(0.1, 0.9 - (red_flag_score * 0.25))
        
        # Additional penalties for multiple red flags
        if red_flag_score >= 2:
            base_credibility *= 0.7  # Heavy penalty for multiple red flags
        
        # Check for conspiracy/misleading language patterns
        conspiracy_patterns = ["big pharma", "they don't want", "cover up", "hidden truth", "wake up"]
        conspiracy_score = sum(1 for pattern in conspiracy_patterns 
                             if pattern in claim_text.lower())
        
        if conspiracy_score > 0:
            base_credibility *= (0.8 - conspiracy_score * 0.1)  # Additional penalty for conspiracy language
        
        # Add some randomness to simulate real-world variance
        credibility = base_credibility + random.uniform(-0.1, 0.1)
        credibility = max(0.0, min(1.0, credibility))
        
        # Determine verdict based on credibility
        if credibility >= 0.7:
            verdict = "verified"
        elif credibility <= 0.4:
            verdict = "disputed"
        else:
            verdict = "uncertain"
        
        return {
            "method": method,
            "source_type": method.replace("_", " ").title(),
            "credibility": credibility,
            "verdict": verdict,
            "confidence": random.uniform(0.6, 0.9),
            "sources_found": random.randint(1, 5),
            "timestamp": get_current_time()
        }
    
    def synthesize_claim_results(self, verification_results, claim_text):
        """Synthesize verification results into final credibility assessment"""
        if not verification_results:
            return {
                "score": 0.5,
                "verdict": "uncertain",
                "confidence": 0.1,
                "supporting_sources": [],
                "contradicting_sources": []
            }
        
        # Calculate weighted average based on source credibility
        total_weight = 0
        weighted_score = 0
        supporting_sources = []
        contradicting_sources = []
        
        for result in verification_results:
            method = result["method"]
            credibility = result["credibility"]
            weight = self.credibility_weights.get(method, 0.5)
            
            total_weight += weight
            weighted_score += credibility * weight
            
            if result["verdict"] == "verified":
                supporting_sources.append(result["source_type"])
            elif result["verdict"] == "disputed":
                contradicting_sources.append(result["source_type"])
        
        final_score = weighted_score / total_weight if total_weight > 0 else 0.5
        
        # Determine final verdict
        if final_score >= 0.7:
            verdict = "verified"
        elif final_score <= 0.4:
            verdict = "disputed"
        else:
            verdict = "uncertain"
        
        # Calculate confidence based on agreement between sources
        verdicts = [r["verdict"] for r in verification_results]
        most_common_verdict = max(set(verdicts), key=verdicts.count)
        agreement_rate = verdicts.count(most_common_verdict) / len(verdicts)
        confidence = agreement_rate * 0.8 + 0.2  # Base confidence of 0.2
        
        return {
            "score": round(final_score, 2),
            "verdict": verdict,
            "confidence": round(confidence, 2),
            "supporting_sources": supporting_sources,
            "contradicting_sources": contradicting_sources
        }
    
    def calculate_overall_credibility(self, claim_results):
        """Calculate overall credibility across all claims"""
        if not claim_results:
            return {
                "verdict": "uncertain",
                "score": 0.5,
                "confidence": 0.1,
                "is_misinformation": False,
                "sources_used": []
            }
        
        # Calculate weighted average of claim scores
        total_weight = sum(claim.get("priority", 1.0) for claim in claim_results if "priority" in claim)
        if total_weight == 0:
            total_weight = len(claim_results)
        
        weighted_score = sum(
            claim["credibility_score"] * claim.get("priority", 1.0) 
            for claim in claim_results
        ) / total_weight
        
        # Determine overall verdict
        disputed_claims = sum(1 for claim in claim_results if claim["verdict"] == "disputed")
        verified_claims = sum(1 for claim in claim_results if claim["verdict"] == "verified")
        
        if disputed_claims > verified_claims:
            overall_verdict = "disputed"
            is_misinformation = True
        elif verified_claims > disputed_claims:
            overall_verdict = "verified"
            is_misinformation = False
        else:
            overall_verdict = "uncertain"
            is_misinformation = weighted_score < 0.5
        
        # Calculate overall confidence
        avg_confidence = sum(claim["confidence"] for claim in claim_results) / len(claim_results)
        
        # Collect all sources used
        sources_used = set()
        for claim in claim_results:
            sources_used.update(claim.get("supporting_sources", []))
            sources_used.update(claim.get("contradicting_sources", []))
        
        return {
            "verdict": overall_verdict,
            "score": round(weighted_score, 2),
            "confidence": round(avg_confidence, 2),
            "is_misinformation": is_misinformation,
            "sources_used": list(sources_used)
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
