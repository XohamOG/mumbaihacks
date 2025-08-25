# Knowledge Agent
# Role: Educate and explain why something might be misinformation
# Provides educational content and misinformation awareness

import os
import sys
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

from tools.education_generator import EducationGenerator
from tools.misinformation_detector import MisinformationDetector
from tools.explanation_builder import ExplanationBuilder

class KnowledgeAgent:
    """
    Knowledge Agent
    Role: Educate users and explain misinformation patterns
    Provides educational content and awareness about misinformation
    """
    
    def __init__(self):
        self.name = "knowledge_agent"
        self.education_generator = EducationGenerator()
        self.misinformation_detector = MisinformationDetector()
        self.explanation_builder = ExplanationBuilder()
        
        # Knowledge categories
        self.knowledge_areas = [
            "source_credibility",
            "logical_fallacies",
            "statistical_manipulation", 
            "emotional_manipulation",
            "confirmation_bias",
            "echo_chambers",
            "deepfakes_detection",
            "fact_checking_methods"
        ]
        
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Main knowledge processing and education"""
        fact_check_result = input_data.get("fact_check_result", {})
        content = input_data.get("content")
        content_type = input_data.get("content_type")
        
        try:
            # Determine if content is misinformation
            is_misinformation = fact_check_result.get("is_misinformation", False)
            credibility_score = fact_check_result.get("credibility_score", 0.5)
            
            if is_misinformation:
                return self.generate_misinformation_education(
                    fact_check_result, content, content_type
                )
            else:
                return self.generate_general_education(
                    fact_check_result, content, content_type
                )
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": get_current_time()
            }
    
    def generate_misinformation_education(self, fact_check_result, content, content_type):
        """Generate educational content for identified misinformation"""
        
        # Detect misinformation patterns
        patterns = self.misinformation_detector.detect_patterns(
            content, fact_check_result
        )
        
        # Generate explanations
        explanations = self.explanation_builder.build_explanations(
            patterns, fact_check_result
        )
        
        # Generate educational content
        educational_content = self.education_generator.generate_education(
            patterns, explanations, "misinformation"
        )
        
        # Create learning resources
        learning_resources = self.create_learning_resources(patterns)
        
        return {
            "status": "misinformation_detected",
            "verdict": "This content contains misinformation",
            "credibility_score": fact_check_result.get("credibility_score", 0.0),
            "misinformation_patterns": patterns,
            "explanations": explanations,
            "educational_content": educational_content,
            "learning_resources": learning_resources,
            "red_flags_identified": self.identify_red_flags(content),
            "how_to_verify": self.generate_verification_guide(content_type),
            "similar_debunked_claims": self.find_similar_debunked_claims(content),
            "expert_consensus": self.get_expert_consensus_info(fact_check_result),
            "timestamp": get_current_time()
        }
    
    def generate_general_education(self, fact_check_result, content, content_type):
        """Generate educational content for verified or uncertain content"""
        
        credibility_score = fact_check_result.get("credibility_score", 0.5)
        
        # Generate educational content based on score
        if credibility_score >= 0.7:
            education_type = "verification_success"
            message = "This content appears to be credible"
        elif credibility_score >= 0.4:
            education_type = "critical_thinking"
            message = "This content requires careful evaluation"
        else:
            education_type = "skepticism_needed"
            message = "This content should be viewed with skepticism"
        
        # Generate relevant educational content
        educational_content = self.education_generator.generate_education(
            [], {}, education_type
        )
        
        # Provide general media literacy tips
        media_literacy_tips = self.generate_media_literacy_tips(content_type)
        
        return {
            "status": "educational_content_provided",
            "verdict": message,
            "credibility_score": credibility_score,
            "educational_content": educational_content,
            "media_literacy_tips": media_literacy_tips,
            "verification_methods": self.suggest_verification_methods(content_type),
            "critical_thinking_questions": self.generate_critical_questions(content),
            "source_evaluation_guide": self.get_source_evaluation_guide(),
            "timestamp": get_current_time()
        }
    
    def identify_red_flags(self, content):
        """Identify red flags in content for educational purposes"""
        return self.misinformation_detector.identify_red_flags(content)
    
    def generate_verification_guide(self, content_type):
        """Generate step-by-step verification guide"""
        guides = {
            "text": [
                "1. Check the original source and date",
                "2. Look for author credentials and expertise",
                "3. Cross-reference with credible news sources",
                "4. Search for fact-checking websites",
                "5. Examine supporting evidence and citations"
            ],
            "image": [
                "1. Reverse image search to find original source",
                "2. Check metadata and creation date",
                "3. Look for signs of manipulation or editing",
                "4. Verify the context and location",
                "5. Cross-reference with reliable news sources"
            ],
            "video": [
                "1. Check upload date and original source",
                "2. Analyze video quality and potential editing",
                "3. Verify location and timestamp",
                "4. Cross-reference events with news sources",
                "5. Look for creator's credibility and history"
            ],
            "audio": [
                "1. Identify the speaker and verify authenticity",
                "2. Check recording quality and potential manipulation",
                "3. Verify context and date of recording",
                "4. Cross-reference claims with credible sources",
                "5. Look for official statements or confirmations"
            ]
        }
        
        return guides.get(content_type, guides["text"])
    
    def find_similar_debunked_claims(self, content):
        """Find similar claims that have been debunked"""
        # This would connect to a database of debunked claims in production
        return [
            {
                "claim": "Similar misleading claim about the same topic",
                "status": "debunked",
                "source": "factcheck.org",
                "explanation": "Why this similar claim was false"
            }
        ]
    
    def get_expert_consensus_info(self, fact_check_result):
        """Get information about expert consensus"""
        sources = fact_check_result.get("sources_checked", 0)
        
        if sources >= 5:
            return {
                "level": "strong",
                "description": f"Multiple credible sources ({sources}) were consulted",
                "reliability": "high"
            }
        elif sources >= 3:
            return {
                "level": "moderate", 
                "description": f"Several sources ({sources}) were consulted",
                "reliability": "medium"
            }
        else:
            return {
                "level": "limited",
                "description": f"Few sources ({sources}) were available",
                "reliability": "low"
            }
    
    def generate_media_literacy_tips(self, content_type):
        """Generate media literacy tips"""
        return self.education_generator.get_media_literacy_tips(content_type)
    
    def suggest_verification_methods(self, content_type):
        """Suggest specific verification methods"""
        return self.education_generator.get_verification_methods(content_type)
    
    def generate_critical_questions(self, content):
        """Generate critical thinking questions"""
        return [
            "Who created this content and what are their credentials?",
            "What is the original source of this information?",
            "Are there any obvious biases or agenda?",
            "What evidence supports the claims made?",
            "Do other credible sources report similar information?",
            "Is this information recent and relevant?",
            "Does this content appeal more to emotion than logic?",
            "What might be missing from this story?"
        ]
    
    def get_source_evaluation_guide(self):
        """Get guide for evaluating sources"""
        return {
            "credible_indicators": [
                "Author expertise and credentials listed",
                "Publication date clearly stated",
                "Sources and references provided",
                "Contact information available",
                "Professional editorial standards",
                "Transparent funding and ownership"
            ],
            "red_flag_indicators": [
                "Anonymous or unknown authors",
                "No publication date or sources",
                "Sensational headlines or language",
                "Poor grammar and spelling",
                "Obvious bias or agenda",
                "Requests for money or personal information"
            ]
        }
    
    def create_learning_resources(self, patterns):
        """Create additional learning resources"""
        resources = []
        
        for pattern in patterns:
            pattern_type = pattern.get("type")
            if pattern_type == "statistical_manipulation":
                resources.append({
                    "title": "Understanding Statistical Manipulation",
                    "type": "guide",
                    "content": "Learn how statistics can be misleading and how to spot manipulation"
                })
            elif pattern_type == "emotional_manipulation":
                resources.append({
                    "title": "Recognizing Emotional Manipulation", 
                    "type": "guide",
                    "content": "Understand how emotions are used to bypass critical thinking"
                })
        
        return resources

# Example usage
if __name__ == "__main__":
    agent = KnowledgeAgent()
    
    # Mock input from fact check agent
    mock_input = {
        "fact_check_result": {
            "is_misinformation": True,
            "credibility_score": 0.2,
            "verdict": "disputed",
            "sources_checked": 3
        },
        "content": "Scientists discover miracle cure that doctors don't want you to know about!",
        "content_type": "text"
    }
    
    result = agent(mock_input)
    print("Knowledge Agent Result:")
    print(result)
