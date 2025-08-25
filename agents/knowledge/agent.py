# Knowledge Agent
# Role: Educate and explain why something might be misinformation
# Provides educational content and misinformation awareness

import os
import sys
import random
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

class KnowledgeAgent:
    """
    Knowledge Agent
    Role: Educate users and explain misinformation patterns
    Provides educational content and awareness about misinformation
    """
    
    def __init__(self):
        self.name = "knowledge_agent"
        
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
        
        # Educational content database
        self.educational_content = {
            "source_credibility": {
                "title": "Evaluating Source Credibility",
                "key_points": [
                    "Check if the source has editorial oversight and fact-checking processes",
                    "Look for author credentials and expertise in the subject matter",
                    "Verify if the source cites credible references and primary sources",
                    "Be wary of sources with clear political or financial biases"
                ],
                "red_flags": [
                    "Anonymous authors or sources",
                    "Sensationalized headlines",
                    "No contact information or about page",
                    "Recent domain registration for news sites"
                ]
            },
            "logical_fallacies": {
                "title": "Common Logical Fallacies in Misinformation",
                "key_points": [
                    "Ad hominem: Attacking the person instead of the argument",
                    "False dichotomy: Presenting only two options when more exist",
                    "Straw man: Misrepresenting someone's argument to make it easier to attack",
                    "Appeal to emotion: Using emotions rather than logic to persuade"
                ],
                "examples": [
                    "False correlation: 'Ice cream sales and drowning deaths both increase in summer, so ice cream causes drowning'",
                    "Cherry picking: Selecting only data that supports your conclusion"
                ]
            },
            "statistical_manipulation": {
                "title": "How Statistics Can Mislead",
                "key_points": [
                    "Correlation does not imply causation",
                    "Sample size and selection bias affect validity",
                    "Relative vs absolute risk can be misleading",
                    "Graphs can be manipulated to exaggerate differences"
                ],
                "warning_signs": [
                    "Missing sample size information",
                    "Vague terms like 'studies show' without citations",
                    "Dramatic percentage changes from small baseline numbers"
                ]
            }
        }
        
        # Misinformation patterns
        self.misinformation_patterns = {
            "emotional_manipulation": [
                "Appeals to fear without evidence",
                "Uses outrage to bypass critical thinking",
                "Exploits personal insecurities or biases",
                "Creates urgency to prevent fact-checking"
            ],
            "false_authority": [
                "Quotes non-experts in relevant fields",
                "Uses credentials from unrelated areas",
                "Cites discredited or retracted studies",
                "Appeals to fake consensus"
            ],
            "conspiracy_thinking": [
                "Assumes malicious intent without evidence",
                "Dismisses contradictory evidence as part of conspiracy",
                "Uses circular reasoning to support claims",
                "Promotes distrust of legitimate institutions"
            ]
        }
        
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Main knowledge processing and education"""
        fact_check_result = input_data.get("fact_check_result", {})
        content = input_data.get("content", "")
        content_type = input_data.get("content_type", "text")
        
        try:
            # Determine if content is misinformation
            is_misinformation = fact_check_result.get("is_misinformation", False)
            credibility_score = fact_check_result.get("credibility_score", 0.5)
            overall_verdict = fact_check_result.get("overall_verdict", "uncertain")
            
            if is_misinformation or credibility_score < 0.4:
                return self.generate_misinformation_education(
                    fact_check_result, content, content_type
                )
            elif credibility_score > 0.7:
                return self.generate_verification_education(
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
        patterns = self.detect_misinformation_patterns(content, fact_check_result)
        
        # Generate explanations
        explanations = self.build_explanations(patterns, fact_check_result)
        
        # Select relevant educational content
        educational_content = self.select_educational_content(patterns)
        
        # Generate practical tips
        tips = self.generate_fact_checking_tips(patterns)
        
        return {
            "status": "completed",
            "education_type": "misinformation_detected",
            "verdict": fact_check_result.get("overall_verdict", "disputed"),
            "credibility_score": fact_check_result.get("credibility_score", 0.0),
            "explanation": {
                "summary": "This content shows characteristics of misinformation",
                "patterns_detected": patterns,
                "detailed_explanations": explanations
            },
            "educational_content": educational_content,
            "actionable_tips": tips,
            "recommended_actions": [
                "Do not share this content",
                "Check multiple reliable sources",
                "Look for official statements from authorities",
                "Be skeptical of sensational claims"
            ],
            "additional_resources": self.get_additional_resources(patterns),
            "timestamp": get_current_time()
        }
    
    def generate_verification_education(self, fact_check_result, content, content_type):
        """Generate educational content for verified information"""
        
        return {
            "status": "completed",
            "education_type": "information_verified",
            "verdict": fact_check_result.get("overall_verdict", "verified"),
            "credibility_score": fact_check_result.get("credibility_score", 0.8),
            "explanation": {
                "summary": "This content appears to be accurate based on available evidence",
                "verification_details": self.explain_verification_process(fact_check_result)
            },
            "educational_content": {
                "title": "Understanding Reliable Information",
                "key_points": [
                    "This information has been cross-verified with multiple credible sources",
                    "The sources cited appear to be legitimate and authoritative",
                    "The claims made align with expert consensus in the relevant field"
                ]
            },
            "good_practices": [
                "Continue to verify information from multiple sources",
                "Stay updated as new information becomes available",
                "Share responsibly with proper context"
            ],
            "timestamp": get_current_time()
        }
    
    def generate_general_education(self, fact_check_result, content, content_type):
        """Generate general educational content about fact-checking"""
        
        # Select random educational topic
        random_topic = random.choice(list(self.educational_content.keys()))
        topic_content = self.educational_content[random_topic]
        
        return {
            "status": "completed",
            "education_type": "general_awareness",
            "verdict": fact_check_result.get("overall_verdict", "uncertain"),
            "credibility_score": fact_check_result.get("credibility_score", 0.5),
            "explanation": {
                "summary": "The credibility of this content is uncertain. Here's some general guidance on evaluating information."
            },
            "educational_content": topic_content,
            "general_tips": [
                "Always check multiple sources before believing or sharing",
                "Look for primary sources and original research",
                "Be aware of your own biases and emotional reactions",
                "Consider the source's motivation and potential conflicts of interest"
            ],
            "fact_checking_steps": [
                "1. Check the source - Is it reputable and credible?",
                "2. Look for citations - Are claims backed by evidence?",
                "3. Cross-reference - Do other reliable sources report the same?",
                "4. Check the date - Is the information current?",
                "5. Consider context - Is information presented fairly?"
            ],
            "timestamp": get_current_time()
        }
    
    def detect_misinformation_patterns(self, content, fact_check_result):
        """Detect misinformation patterns in content"""
        patterns_found = []
        content_lower = content.lower()
        
        # Check for emotional manipulation
        emotional_triggers = ["shocking", "outrageous", "they don't want you to know", "secret", "hidden truth"]
        if any(trigger in content_lower for trigger in emotional_triggers):
            patterns_found.append({
                "type": "emotional_manipulation",
                "description": "Uses emotional language to bypass critical thinking",
                "severity": "medium"
            })
        
        # Check for false authority
        authority_patterns = ["doctors hate this", "experts don't want", "big pharma hides"]
        if any(pattern in content_lower for pattern in authority_patterns):
            patterns_found.append({
                "type": "false_authority",
                "description": "Makes claims about expert opinion without credible sources",
                "severity": "high"
            })
        
        # Check for conspiracy thinking
        conspiracy_words = ["cover-up", "conspiracy", "they're hiding", "wake up", "sheeple"]
        if any(word in content_lower for word in conspiracy_words):
            patterns_found.append({
                "type": "conspiracy_thinking",
                "description": "Promotes conspiracy theories without evidence",
                "severity": "high"
            })
        
        # Check for statistical manipulation
        if "%" in content or "times more likely" in content_lower:
            if not any(source in content_lower for source in ["study", "research", "published"]):
                patterns_found.append({
                    "type": "statistical_manipulation",
                    "description": "Uses statistics without citing credible sources",
                    "severity": "medium"
                })
        
        # Check for urgency without verification
        urgency_words = ["breaking", "urgent", "immediate", "act now", "before it's too late"]
        if any(word in content_lower for word in urgency_words):
            patterns_found.append({
                "type": "artificial_urgency",
                "description": "Creates false sense of urgency to prevent fact-checking",
                "severity": "medium"
            })
        
        return patterns_found
    
    def build_explanations(self, patterns, fact_check_result):
        """Build detailed explanations for detected patterns"""
        explanations = []
        
        for pattern in patterns:
            pattern_type = pattern["type"]
            
            if pattern_type == "emotional_manipulation":
                explanations.append({
                    "pattern": pattern_type,
                    "explanation": "This content uses emotional language designed to provoke strong reactions. "
                                 "Emotional manipulation can cloud judgment and make people less likely to "
                                 "fact-check information before sharing it."
                })
            
            elif pattern_type == "false_authority":
                explanations.append({
                    "pattern": pattern_type,
                    "explanation": "This content makes claims about what experts think without providing "
                                 "credible sources. Legitimate expert opinions are published in peer-reviewed "
                                 "journals or official statements from recognized institutions."
                })
            
            elif pattern_type == "conspiracy_thinking":
                explanations.append({
                    "pattern": pattern_type,
                    "explanation": "This content promotes conspiracy theories that assume coordinated deception "
                                 "without providing verifiable evidence. Real conspiracies are eventually "
                                 "exposed through investigative journalism and whistleblowers with documentation."
                })
            
            elif pattern_type == "statistical_manipulation":
                explanations.append({
                    "pattern": pattern_type,
                    "explanation": "This content uses statistics or percentages without citing the original "
                                 "research or study. Legitimate statistics should be traceable to peer-reviewed "
                                 "research with proper methodology and sample sizes."
                })
            
            elif pattern_type == "artificial_urgency":
                explanations.append({
                    "pattern": pattern_type,
                    "explanation": "This content creates artificial urgency to encourage immediate sharing "
                                 "without verification. Legitimate urgent information comes through official "
                                 "channels like government agencies or established news organizations."
                })
        
        return explanations
    
    def select_educational_content(self, patterns):
        """Select relevant educational content based on detected patterns"""
        if not patterns:
            return self.educational_content["source_credibility"]
        
        # Map patterns to educational content
        pattern_mapping = {
            "emotional_manipulation": "logical_fallacies",
            "false_authority": "source_credibility", 
            "conspiracy_thinking": "source_credibility",
            "statistical_manipulation": "statistical_manipulation",
            "artificial_urgency": "logical_fallacies"
        }
        
        # Select most relevant content
        primary_pattern = patterns[0]["type"]
        content_key = pattern_mapping.get(primary_pattern, "source_credibility")
        
        return self.educational_content[content_key]
    
    def generate_fact_checking_tips(self, patterns):
        """Generate specific fact-checking tips based on patterns"""
        tips = []
        
        pattern_types = [p["type"] for p in patterns]
        
        if "emotional_manipulation" in pattern_types:
            tips.append("When content makes you feel strongly (angry, scared, excited), take a pause before sharing")
        
        if "false_authority" in pattern_types:
            tips.append("Look up the credentials of anyone cited as an expert - are they qualified in this specific field?")
        
        if "conspiracy_thinking" in pattern_types:
            tips.append("Ask for evidence: What documentation supports these claims? Are there credible whistleblowers?")
        
        if "statistical_manipulation" in pattern_types:
            tips.append("Look for the original study behind any statistics - check the sample size and methodology")
        
        if "artificial_urgency" in pattern_types:
            tips.append("Urgent claims should be verified through multiple official sources before sharing")
        
        # Add general tips if no specific patterns
        if not tips:
            tips = [
                "Check if other reputable news sources are reporting the same information",
                "Look for official statements from relevant authorities or institutions",
                "Be skeptical of information that seems too good (or bad) to be true"
            ]
        
        return tips
    
    def explain_verification_process(self, fact_check_result):
        """Explain how the fact-checking verification was done"""
        sources_used = fact_check_result.get("sources_checked", [])
        
        explanation = f"This information was verified by checking {len(sources_used)} different types of sources"
        
        if sources_used:
            source_types = ", ".join(sources_used)
            explanation += f" including: {source_types}"
        
        explanation += ". The information was found to be consistent across these credible sources."
        
        return explanation
    
    def get_additional_resources(self, patterns):
        """Get additional educational resources based on patterns"""
        resources = [
            {
                "title": "How to Spot Misinformation",
                "description": "A guide to identifying common misinformation tactics",
                "type": "guide"
            },
            {
                "title": "Credible Fact-Checking Organizations",
                "description": "List of reputable fact-checking websites and organizations",
                "type": "resource_list"
            }
        ]
        
        pattern_types = [p["type"] for p in patterns]
        
        if "statistical_manipulation" in pattern_types:
            resources.append({
                "title": "Understanding Statistics in Media",
                "description": "How to evaluate statistical claims in news and social media",
                "type": "educational_guide"
            })
        
        if "conspiracy_thinking" in pattern_types:
            resources.append({
                "title": "Critical Thinking and Conspiracy Theories",
                "description": "How to apply critical thinking to extraordinary claims",
                "type": "educational_guide"
            })
        
        return resources
        
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
        educational_content = self.select_educational_content(education_type)
        
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
        tips = {
            "text": [
                "Check multiple sources before believing claims",
                "Look for citations and references to original sources",
                "Be skeptical of emotional or sensational language",
                "Verify author credentials and publication date"
            ],
            "image": [
                "Use reverse image search to check origins",
                "Look for signs of digital manipulation",
                "Check if the image context matches the claim",
                "Verify the source and date of the image"
            ],
            "video": [
                "Check video metadata and upload date",
                "Look for signs of editing or deepfakes",
                "Verify if audio matches video content",
                "Cross-reference with other sources"
            ]
        }
        return tips.get(content_type, tips["text"])
    
    def suggest_verification_methods(self, content_type):
        """Suggest specific verification methods"""
        methods = {
            "text": [
                "Cross-reference with established fact-checking sites",
                "Check primary sources and original research",
                "Look for scientific peer review if applicable",
                "Verify quotes and statistics independently"
            ],
            "image": [
                "Use Google Images or TinEye reverse search",
                "Check EXIF data for manipulation signs",
                "Consult image forensics tools",
                "Verify location and timing claims"
            ],
            "video": [
                "Check video metadata and timestamps",
                "Use video verification tools like InVID",
                "Analyze audio-visual synchronization",
                "Verify claims about location and time"
            ]
        }
        return methods.get(content_type, methods["text"])
    
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
