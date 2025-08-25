# Preprocessing and Context Agent
# Summarizes context and analyzes content for fact-checking preparation

import os
import sys
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

from tools.context_analyzer import ContextAnalyzer
from tools.claim_extractor import ClaimExtractor
from tools.priority_calculator import PriorityCalculator

class PreprocessingContextAgent:
    """
    Preprocessing and Context Agent
    Role: Summarize context and prepare content for fact-checking
    Extracts claims, analyzes context, determines priority
    """
    
    def __init__(self):
        self.name = "preprocessing_context_agent"
        self.context_analyzer = ContextAnalyzer()
        self.claim_extractor = ClaimExtractor()
        self.priority_calculator = PriorityCalculator()
        
        # Context analysis settings
        self.max_context_length = 1000
        self.min_claim_confidence = 0.3
        
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Main preprocessing and context analysis"""
        processed_content = input_data.get("processed_content", {})
        content_type = input_data.get("content_type")
        urgency = input_data.get("urgency", "medium")
        
        try:
            # Analyze context
            context_analysis = self.context_analyzer.analyze_context(
                processed_content, content_type
            )
            
            # Extract claims for fact-checking
            extracted_claims = self.claim_extractor.extract_claims(
                processed_content, context_analysis
            )
            
            # Calculate priorities
            prioritized_claims = self.priority_calculator.calculate_priorities(
                extracted_claims, context_analysis, urgency
            )
            
            # Filter claims by confidence threshold
            valid_claims = [
                claim for claim in prioritized_claims 
                if claim.get("confidence", 0) >= self.min_claim_confidence
            ]
            
            # Prepare fact-check targets
            fact_check_targets = self.prepare_fact_check_targets(valid_claims)
            
            return {
                "status": "completed",
                "context_summary": context_analysis.get("summary"),
                "context_metadata": context_analysis.get("metadata"),
                "extracted_claims": len(extracted_claims),
                "valid_claims": len(valid_claims),
                "fact_check_targets": fact_check_targets,
                "content_insights": context_analysis.get("insights"),
                "recommended_checks": context_analysis.get("recommended_checks", []),
                "timestamp": get_current_time()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": get_current_time()
            }
    
    def prepare_fact_check_targets(self, prioritized_claims):
        """Prepare claims for fact-checking agent"""
        targets = []
        
        for i, claim in enumerate(prioritized_claims[:10]):  # Limit to top 10
            target = {
                "claim_id": i + 1,
                "claim_text": claim.get("text"),
                "claim_type": claim.get("type"),
                "priority": claim.get("priority", 0.5),
                "confidence": claim.get("confidence", 0.5),
                "check_methods": self.determine_check_methods(claim),
                "context": claim.get("context", ""),
                "urgency_level": claim.get("urgency_level", "medium")
            }
            targets.append(target)
        
        return targets
    
    def determine_check_methods(self, claim):
        """Determine appropriate fact-checking methods for a claim"""
        methods = []
        claim_type = claim.get("type", "general")
        claim_text = claim.get("text", "").lower()
        
        # Always check news sources
        methods.append("news_sources")
        
        # Health-related claims
        if any(keyword in claim_text for keyword in ["health", "medical", "vaccine", "disease", "drug"]):
            methods.extend(["government", "academic"])
        
        # Political claims
        if any(keyword in claim_text for keyword in ["government", "election", "policy", "president", "minister"]):
            methods.extend(["government", "fact_checkers"])
        
        # Scientific claims
        if any(keyword in claim_text for keyword in ["study", "research", "scientists", "discovery"]):
            methods.extend(["academic", "fact_checkers"])
        
        # Social media viral claims
        if claim.get("viral_potential", 0) > 0.7:
            methods.append("social_media")
        
        # Breaking news
        if claim.get("urgency_level") == "high":
            methods.extend(["fact_checkers", "social_media"])
        
        return list(set(methods))  # Remove duplicates
    
    def generate_context_summary(self, context_analysis):
        """Generate human-readable context summary"""
        summary_parts = []
        
        # Content type and source
        content_type = context_analysis.get("content_type", "unknown")
        summary_parts.append(f"Content type: {content_type}")
        
        # Key topics
        topics = context_analysis.get("topics", [])
        if topics:
            summary_parts.append(f"Main topics: {', '.join(topics[:3])}")
        
        # Sentiment and tone
        sentiment = context_analysis.get("sentiment", "neutral")
        tone = context_analysis.get("tone", "informative")
        summary_parts.append(f"Tone: {tone}, Sentiment: {sentiment}")
        
        # Potential issues
        red_flags = context_analysis.get("red_flags", [])
        if red_flags:
            summary_parts.append(f"Potential issues: {len(red_flags)} identified")
        
        return "; ".join(summary_parts)

# Example usage
if __name__ == "__main__":
    agent = PreprocessingContextAgent()
    
    # Mock input from content intake agent
    mock_input = {
        "processed_content": {
            "text": "Breaking: Scientists at leading university discover revolutionary cure for common cold. The breakthrough treatment shows 99% effectiveness in clinical trials.",
            "entities": ["scientists", "university", "cure", "common cold", "clinical trials"],
            "keywords": ["breaking", "revolutionary", "breakthrough", "99% effectiveness"],
            "sentiment": "positive",
            "urgency_indicators": ["breaking", "revolutionary"]
        },
        "content_type": "text",
        "urgency": "high"
    }
    
    result = agent(mock_input)
    print("Preprocessing Result:")
    print(result)
