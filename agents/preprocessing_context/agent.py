# Preprocessing and Context Agent
# Summarizes context and analyzes content for fact-checking preparation

import os
import sys
import re
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

class PreprocessingContextAgent:
    """
    Preprocessing and Context Agent
    Role: Summarize context and prepare content for fact-checking
    Extracts claims, analyzes context, determines priority
    """
    
    def __init__(self):
        self.name = "preprocessing_context_agent"
        
        # Context analysis settings
        self.max_context_length = 1000
        self.min_claim_confidence = 0.3
        
        # Content categories for context analysis
        self.content_categories = {
            "health": ["vaccine", "medicine", "cure", "treatment", "disease", "virus", "covid", "cancer"],
            "political": ["election", "government", "politician", "vote", "policy", "president", "minister"],
            "scientific": ["study", "research", "scientist", "discovery", "breakthrough", "experiment"],
            "financial": ["stock", "market", "economy", "investment", "crypto", "bitcoin", "money"],
            "social": ["facebook", "twitter", "viral", "trending", "social media", "influencer"],
            "emergency": ["breaking", "urgent", "alert", "crisis", "disaster", "emergency"]
        }
        
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Main preprocessing and context analysis"""
        # Handle different input formats from content intake agent
        if "processed_content" in input_data:
            processed_content = input_data["processed_content"]
            content_type = input_data.get("content_type", "text")
            raw_content = processed_content if isinstance(processed_content, str) else processed_content.get("content", "")
        else:
            # Direct content processing
            raw_content = input_data.get("content", "")
            content_type = input_data.get("content_type", "text")
            processed_content = input_data
        
        try:
            # Analyze context
            context_analysis = self.analyze_context(processed_content, content_type, raw_content)
            
            # Extract claims for fact-checking
            extracted_claims = self.extract_claims(processed_content, context_analysis)
            
            # Calculate priorities
            prioritized_claims = self.calculate_priorities(extracted_claims, context_analysis)
            
            # Filter claims by confidence threshold
            valid_claims = [
                claim for claim in prioritized_claims 
                if claim.get("confidence", 0) >= self.min_claim_confidence
            ]
            
            # Prepare fact-check targets
            fact_check_targets = self.prepare_fact_check_targets(valid_claims)
            
            return {
                "status": "completed",
                "context_summary": self.generate_context_summary(context_analysis),
                "context_metadata": context_analysis.get("metadata", {}),
                "extracted_claims": len(extracted_claims),
                "valid_claims": len(valid_claims),
                "fact_check_targets": fact_check_targets,
                "content_insights": context_analysis.get("insights", []),
                "recommended_checks": context_analysis.get("recommended_checks", []),
                "priority_score": context_analysis.get("priority_score", 0.5),
                "timestamp": get_current_time()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": get_current_time()
            }
    
    def analyze_context(self, processed_content, content_type, raw_content=""):
        """Analyze content context and characteristics"""
        # Handle different content structures
        if isinstance(processed_content, dict):
            text_content = processed_content.get("processed_content", processed_content.get("content", raw_content))
            entities = processed_content.get("entities", {})
            metadata = processed_content.get("metadata", {})
        else:
            text_content = str(processed_content)
            entities = {}
            metadata = {}
        
        if not text_content:
            text_content = raw_content
        
        # Categorize content
        categories = self.categorize_content(text_content)
        
        # Detect sentiment and tone
        sentiment = self.detect_sentiment(text_content)
        tone = self.detect_tone(text_content)
        
        # Identify red flags
        red_flags = self.identify_red_flags(text_content)
        
        # Calculate urgency and viral potential
        urgency_score = self.calculate_urgency_score(text_content, metadata)
        viral_potential = self.assess_viral_potential(text_content, metadata)
        
        # Extract key topics
        topics = self.extract_topics(text_content)
        
        return {
            "content_type": content_type,
            "categories": categories,
            "sentiment": sentiment,
            "tone": tone,
            "red_flags": red_flags,
            "urgency_score": urgency_score,
            "viral_potential": viral_potential,
            "topics": topics,
            "metadata": {
                "word_count": len(text_content.split()) if text_content else 0,
                "has_numbers": bool(re.search(r'\d+', text_content)),
                "has_urls": bool(re.search(r'https?://', text_content)),
                "all_caps_ratio": self.calculate_caps_ratio(text_content),
                **metadata
            },
            "insights": self.generate_insights(categories, red_flags, urgency_score),
            "recommended_checks": self.get_recommended_checks(categories, red_flags),
            "priority_score": self.calculate_content_priority(categories, red_flags, urgency_score)
        }
    
    def categorize_content(self, text):
        """Categorize content based on keywords"""
        categories = []
        text_lower = text.lower()
        
        for category, keywords in self.content_categories.items():
            keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
            if keyword_count > 0:
                categories.append({
                    "category": category,
                    "relevance": keyword_count / len(keywords),
                    "keywords_found": keyword_count
                })
        
        return sorted(categories, key=lambda x: x["relevance"], reverse=True)
    
    def detect_sentiment(self, text):
        """Simple sentiment analysis"""
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "breakthrough", "success"]
        negative_words = ["bad", "terrible", "awful", "disaster", "crisis", "failure", "dangerous"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def detect_tone(self, text):
        """Detect tone of content"""
        urgent_patterns = [r'\b(urgent|breaking|alert|immediate)\b', r'!!+', r'\bNOW\b']
        formal_patterns = [r'\b(according to|research shows|study finds)\b']
        sensational_patterns = [r'\b(shocking|amazing|incredible|unbelievable)\b', r'YOU WON\'T BELIEVE']
        
        text_lower = text.lower()
        
        urgent_score = sum(1 for pattern in urgent_patterns if re.search(pattern, text_lower))
        formal_score = sum(1 for pattern in formal_patterns if re.search(pattern, text_lower))
        sensational_score = sum(1 for pattern in sensational_patterns if re.search(pattern, text_lower))
        
        if sensational_score > max(urgent_score, formal_score):
            return "sensational"
        elif urgent_score > formal_score:
            return "urgent"
        elif formal_score > 0:
            return "formal"
        else:
            return "informal"
    
    def identify_red_flags(self, text):
        """Identify potential misinformation red flags"""
        red_flag_patterns = [
            {"pattern": r"doctors hate this", "type": "clickbait_medical"},
            {"pattern": r"they don't want you to know", "type": "conspiracy"},
            {"pattern": r"100% natural", "type": "unsubstantiated_claim"},
            {"pattern": r"miracle cure", "type": "false_medical"},
            {"pattern": r"big pharma", "type": "conspiracy_theory"},
            {"pattern": r"\d+% effective", "type": "unverified_statistic"},
            {"pattern": r"leaked documents", "type": "unverified_source"},
            {"pattern": r"exclusive footage", "type": "sensational_claim"}
        ]
        
        red_flags = []
        text_lower = text.lower()
        
        for flag_info in red_flag_patterns:
            if re.search(flag_info["pattern"], text_lower):
                red_flags.append({
                    "type": flag_info["type"],
                    "pattern": flag_info["pattern"],
                    "severity": self.get_flag_severity(flag_info["type"])
                })
        
        return red_flags
    
    def get_flag_severity(self, flag_type):
        """Get severity level for different red flag types"""
        severity_map = {
            "false_medical": "high",
            "conspiracy_theory": "high",
            "unverified_statistic": "medium",
            "clickbait_medical": "medium",
            "conspiracy": "medium",
            "unsubstantiated_claim": "medium",
            "unverified_source": "low",
            "sensational_claim": "low"
        }
        return severity_map.get(flag_type, "low")
    
    def calculate_urgency_score(self, text, metadata):
        """Calculate urgency score based on content and metadata"""
        urgency_score = 0.0
        
        # Check urgency indicators from metadata
        if isinstance(metadata, dict):
            urgency_indicators = metadata.get("urgency_indicators", {})
            if isinstance(urgency_indicators, dict):
                urgency_score += urgency_indicators.get("score", 0) * 0.5
        
        # Check for time-sensitive keywords
        urgent_keywords = ["breaking", "urgent", "now", "immediate", "alert", "emergency"]
        text_lower = text.lower()
        for keyword in urgent_keywords:
            if keyword in text_lower:
                urgency_score += 0.15
        
        return min(urgency_score, 1.0)
    
    def assess_viral_potential(self, text, metadata):
        """Assess potential for content to go viral"""
        viral_indicators = 0.0
        text_lower = text.lower()
        
        # Emotional content
        emotional_words = ["shocking", "amazing", "unbelievable", "incredible", "outrageous"]
        emotional_score = sum(1 for word in emotional_words if word in text_lower)
        viral_indicators += min(emotional_score * 0.1, 0.3)
        
        # Share-worthy phrases
        share_phrases = ["you won't believe", "share if you agree", "tag someone", "must see"]
        for phrase in share_phrases:
            if phrase in text_lower:
                viral_indicators += 0.2
        
        # Controversy potential
        controversial_topics = ["vaccine", "election", "celebrity", "government"]
        for topic in controversial_topics:
            if topic in text_lower:
                viral_indicators += 0.1
        
        return min(viral_indicators, 1.0)
    
    def extract_topics(self, text):
        """Extract main topics from content"""
        topics = []
        
        # Check against content categories
        for category, keywords in self.content_categories.items():
            if any(keyword in text.lower() for keyword in keywords):
                topics.append(category)
        
        # Extract entity-based topics (simple approach)
        text_words = text.lower().split()
        common_topics = ["covid", "vaccine", "election", "climate", "economy", "technology", "health"]
        
        for topic in common_topics:
            if topic in text_words:
                topics.append(topic)
        
        return list(set(topics))[:5]  # Return unique topics, max 5
    
    def calculate_caps_ratio(self, text):
        """Calculate ratio of capital letters"""
        if not text:
            return 0.0
        
        caps_count = sum(1 for char in text if char.isupper())
        total_letters = sum(1 for char in text if char.isalpha())
        
        return caps_count / total_letters if total_letters > 0 else 0.0
    
    def extract_claims(self, processed_content, context_analysis):
        """Extract factual claims from processed content"""
        # Get text content
        if isinstance(processed_content, dict):
            text_content = processed_content.get("processed_content", processed_content.get("content", ""))
            existing_claims = processed_content.get("extracted_claims", [])
        else:
            text_content = str(processed_content)
            existing_claims = []
        
        claims = []
        
        # Use existing claims if available
        if existing_claims:
            for claim in existing_claims:
                if isinstance(claim, dict):
                    claims.append({
                        "text": claim.get("text", ""),
                        "confidence": claim.get("confidence", 0.5),
                        "type": self.classify_claim_type(claim.get("text", "")),
                        "context": context_analysis.get("categories", [])
                    })
        else:
            # Extract claims from text
            sentences = re.split(r'[.!?]+', text_content)
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20:  # Skip short sentences
                    claim_confidence = self.assess_claim_confidence(sentence)
                    if claim_confidence >= 0.3:  # Minimum threshold
                        claims.append({
                            "text": sentence,
                            "confidence": claim_confidence,
                            "type": self.classify_claim_type(sentence),
                            "context": context_analysis.get("categories", [])
                        })
        
        return claims
    
    def classify_claim_type(self, claim_text):
        """Classify the type of claim"""
        text_lower = claim_text.lower()
        
        if any(word in text_lower for word in ["study", "research", "scientist", "experiment"]):
            return "scientific"
        elif any(word in text_lower for word in ["vaccine", "medicine", "treatment", "health"]):
            return "medical"
        elif any(word in text_lower for word in ["election", "government", "politician", "policy"]):
            return "political"
        elif any(word in text_lower for word in ["%", "percent", "statistics", "data"]):
            return "statistical"
        else:
            return "general"
    
    def assess_claim_confidence(self, claim_text):
        """Assess confidence that this is a factual claim"""
        confidence = 0.3  # Base confidence
        
        # Factual indicators
        factual_patterns = [
            r'\d+%', r'\d+ (people|cases|studies|times)',
            r'(study|research) (shows|finds|reveals)',
            r'according to', r'scientists (say|found|discovered)'
        ]
        
        for pattern in factual_patterns:
            if re.search(pattern, claim_text, re.IGNORECASE):
                confidence += 0.2
        
        # Reduce confidence for opinion indicators
        opinion_patterns = [r'I think', r'in my opinion', r'I believe', r'seems like']
        for pattern in opinion_patterns:
            if re.search(pattern, claim_text, re.IGNORECASE):
                confidence -= 0.3
        
        return max(0.1, min(1.0, confidence))
    
    def calculate_priorities(self, claims, context_analysis):
        """Calculate priority scores for claims"""
        prioritized_claims = []
        
        for claim in claims:
            priority_score = self.calculate_claim_priority(claim, context_analysis)
            prioritized_claim = claim.copy()
            prioritized_claim["priority"] = priority_score
            prioritized_claims.append(prioritized_claim)
        
        return sorted(prioritized_claims, key=lambda x: x["priority"], reverse=True)
    
    def calculate_claim_priority(self, claim, context_analysis):
        """Calculate priority score for individual claim"""
        priority = claim.get("confidence", 0.5)  # Start with confidence
        
        # Boost priority based on claim type
        claim_type = claim.get("type", "general")
        type_weights = {
            "medical": 0.3,
            "scientific": 0.25,
            "political": 0.2,
            "statistical": 0.15,
            "general": 0.1
        }
        priority += type_weights.get(claim_type, 0.1)
        
        # Boost priority for urgent content
        urgency_score = context_analysis.get("urgency_score", 0)
        priority += urgency_score * 0.2
        
        # Boost priority for content with red flags
        red_flags = context_analysis.get("red_flags", [])
        high_severity_flags = [flag for flag in red_flags if flag.get("severity") == "high"]
        priority += len(high_severity_flags) * 0.1
        
        return min(priority, 1.0)
    
    def generate_insights(self, categories, red_flags, urgency_score):
        """Generate insights about the content"""
        insights = []
        
        if categories:
            top_category = categories[0]["category"]
            insights.append(f"Primary topic: {top_category}")
        
        if red_flags:
            high_severity_flags = [flag for flag in red_flags if flag.get("severity") == "high"]
            if high_severity_flags:
                insights.append(f"High-risk content detected: {len(high_severity_flags)} serious red flags")
        
        if urgency_score > 0.7:
            insights.append("High urgency content - requires immediate attention")
        
        return insights
    
    def get_recommended_checks(self, categories, red_flags):
        """Get recommended fact-checking approaches"""
        checks = ["standard_verification"]  # Always do standard checks
        
        if categories:
            top_category = categories[0]["category"]
            
            if top_category == "health":
                checks.extend(["medical_authority_check", "academic_source_verification"])
            elif top_category == "political":
                checks.extend(["government_source_check", "fact_checker_verification"])
            elif top_category == "scientific":
                checks.extend(["peer_review_check", "academic_source_verification"])
        
        if red_flags:
            checks.append("enhanced_scrutiny")
        
        return list(set(checks))
    
    def calculate_content_priority(self, categories, red_flags, urgency_score):
        """Calculate overall content priority for processing"""
        priority = 0.5  # Base priority
        
        # Category-based priority
        if categories:
            category_priorities = {
                "health": 0.3,
                "political": 0.25,
                "emergency": 0.4,
                "scientific": 0.2
            }
            top_category = categories[0]["category"]
            priority += category_priorities.get(top_category, 0.1)
        
        # Red flag impact
        priority += len(red_flags) * 0.1
        
        # Urgency impact
        priority += urgency_score * 0.2
        
        return min(priority, 1.0)
    
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
