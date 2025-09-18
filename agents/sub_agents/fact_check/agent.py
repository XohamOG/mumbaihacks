"""
Fact Check Agent
Performs multi-source verification and credibility scoring for misinformation detection
Includes advanced ML analysis with token probabilities, stylometric checks, and cognitive fingerprinting
Following ADK agent structure requirements
"""

try:
    from google.adk import Agent
except ImportError:
    # Fallback for when google.adk is not available
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from mock_adk import Agent
    except ImportError:
        class Agent:
            def __init__(self, name, model, description, instruction):
                self.name = name
                self.model = model
                self.description = description
                self.instruction = instruction

import os
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️  Transformers not available - ML features will be limited")

import numpy as np
from typing import Dict, List, Any
import re
import statistics
from collections import Counter


class AdvancedMLAnalyzer:
    """Advanced ML analysis tools for fact checking"""
    
    def __init__(self):
        self.device = "cuda" if TRANSFORMERS_AVAILABLE and torch.cuda.is_available() else "cpu"
        
        # Initialize models
        if TRANSFORMERS_AVAILABLE:
            try:
                # Fact-checking model
                self.fact_checker = pipeline(
                    "text-classification",
                    model="microsoft/DialoGPT-medium",
                    device=0 if torch.cuda.is_available() else -1
                )
                
                # Sentiment/tone analysis
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    device=0 if torch.cuda.is_available() else -1
                )
                
                # Misinformation detection model
                self.misinfo_detector = pipeline(
                    "text-classification",
                    model="martin-ha/toxic-comment-model",
                    device=0 if torch.cuda.is_available() else -1
                )
                
                # Load tokenizer for token probability analysis
                self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
                self.model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
                
            except Exception as e:
                print(f"Warning: Could not load all ML models: {e}")
                self.fact_checker = None
                self.sentiment_analyzer = None
                self.misinfo_detector = None
                self.tokenizer = None
                self.model = None
        else:
            print("Transformers library not available - using fallback implementations")
            self.fact_checker = None
            self.sentiment_analyzer = None
            self.misinfo_detector = None
            self.tokenizer = None
            self.model = None
    
    def get_token_probabilities(self, text: str) -> Dict[str, Any]:
        """Analyze token probabilities for suspicious patterns"""
        if not self.tokenizer or not self.model:
            return {"error": "Models not loaded"}
            
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
            tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
            token_probs = probabilities[0].tolist()
            
            # Calculate statistics
            prob_stats = {
                "mean_probability": statistics.mean(token_probs),
                "std_probability": statistics.stdev(token_probs) if len(token_probs) > 1 else 0,
                "min_probability": min(token_probs),
                "max_probability": max(token_probs),
                "suspicious_low_prob_tokens": [
                    {"token": token, "prob": prob} 
                    for token, prob in zip(tokens, token_probs) 
                    if prob < 0.1 and token not in ["[CLS]", "[SEP]", "[PAD]"]
                ]
            }
            
            return {
                "token_count": len(tokens),
                "probability_statistics": prob_stats,
                "confidence_score": prob_stats["mean_probability"]
            }
            
        except Exception as e:
            return {"error": f"Token analysis failed: {e}"}
    
    def stylometric_analysis(self, text: str) -> Dict[str, Any]:
        """Perform stylometric analysis to detect writing patterns"""
        
        # Basic text statistics
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Character-level analysis
        char_freq = Counter(text.lower())
        
        # Word-level analysis
        word_lengths = [len(word) for word in words]
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        
        # Punctuation analysis
        punctuation_count = sum(1 for char in text if char in "!@#$%^&*()_+-=[]{}|;':\",./<>?")
        
        # Readability indicators
        avg_word_length = statistics.mean(word_lengths) if word_lengths else 0
        avg_sentence_length = statistics.mean(sentence_lengths) if sentence_lengths else 0
        
        # Suspicious patterns
        excessive_caps = sum(1 for char in text if char.isupper()) / len(text) if text else 0
        excessive_punctuation = punctuation_count / len(text) if text else 0
        
        return {
            "text_statistics": {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "character_count": len(text),
                "avg_word_length": avg_word_length,
                "avg_sentence_length": avg_sentence_length
            },
            "style_indicators": {
                "excessive_capitalization": excessive_caps > 0.15,  # More than 15% caps
                "excessive_punctuation": excessive_punctuation > 0.05,  # More than 5% punctuation
                "very_short_sentences": sum(1 for l in sentence_lengths if l < 5) / len(sentence_lengths) if sentence_lengths else 0,
                "very_long_sentences": sum(1 for l in sentence_lengths if l > 30) / len(sentence_lengths) if sentence_lengths else 0
            },
            "readability_score": min(100, max(0, 100 - (avg_word_length * 5 + avg_sentence_length * 2))),
            "complexity_indicators": {
                "lexical_diversity": len(set(words)) / len(words) if words else 0,
                "punctuation_density": excessive_punctuation,
                "capitalization_ratio": excessive_caps
            }
        }
    
    def tone_analysis(self, text: str) -> Dict[str, Any]:
        """Analyze tone and emotional content"""
        if not self.sentiment_analyzer:
            return {"error": "Sentiment analyzer not loaded"}
            
        try:
            # Basic sentiment
            sentiment_result = self.sentiment_analyzer(text)
            
            # Emotional indicators in text
            emotional_words = {
                "anger": ["angry", "furious", "outraged", "enraged", "livid"],
                "fear": ["scared", "terrified", "afraid", "panicked", "worried"],
                "excitement": ["amazing", "incredible", "shocking", "unbelievable"],
                "urgency": ["urgent", "immediately", "now", "quickly", "asap"],
                "certainty": ["definitely", "absolutely", "certainly", "obviously", "clearly"]
            }
            
            text_lower = text.lower()
            emotion_scores = {}
            
            for emotion, words in emotional_words.items():
                count = sum(1 for word in words if word in text_lower)
                emotion_scores[emotion] = count / len(text.split()) if text.split() else 0
            
            # Detect manipulative language patterns
            manipulative_patterns = [
                r"\b(you won't believe|shocking truth|they don't want you to know)\b",
                r"\b(secret|hidden|exposed|revealed)\b",
                r"\b(must read|share now|urgent)\b",
                r"\b(mainstream media|they|establishment)\b"
            ]
            
            manipulation_score = sum(
                len(re.findall(pattern, text, re.IGNORECASE)) 
                for pattern in manipulative_patterns
            ) / len(text.split()) if text.split() else 0
            
            return {
                "sentiment": sentiment_result[0] if sentiment_result else None,
                "emotion_analysis": emotion_scores,
                "manipulation_indicators": {
                    "manipulation_score": manipulation_score,
                    "high_emotion": max(emotion_scores.values()) > 0.05 if emotion_scores else False,
                    "urgency_language": emotion_scores.get("urgency", 0) > 0.02,
                    "absolute_language": emotion_scores.get("certainty", 0) > 0.03
                },
                "tone_classification": self._classify_tone(emotion_scores, manipulation_score)
            }
            
        except Exception as e:
            return {"error": f"Tone analysis failed: {e}"}
    
    def cognitive_fingerprinting(self, text: str) -> Dict[str, Any]:
        """Detect cognitive manipulation patterns and biases"""
        
        # Logical fallacy patterns
        fallacy_patterns = {
            "ad_hominem": [r"typical (liberal|conservative)", r"what do you expect from"],
            "strawman": [r"so you're saying", r"if we follow your logic"],
            "false_dilemma": [r"either.+or", r"only two choices", r"if not.+then"],
            "appeal_to_authority": [r"experts say", r"scientists agree", r"studies show"],
            "bandwagon": [r"everyone knows", r"most people", r"majority believes"],
            "slippery_slope": [r"this will lead to", r"next thing you know", r"where does it end"]
        }
        
        # Cognitive bias indicators
        bias_patterns = {
            "confirmation_bias": [r"as expected", r"proves what we knew", r"confirms"],
            "anchoring": [r"compared to", r"in contrast", r"much worse than"],
            "availability_heuristic": [r"remember when", r"just like", r"similar to"],
            "recency_bias": [r"recently", r"lately", r"just happened"],
            "authority_bias": [r"according to", r"expert opinion", r"official statement"]
        }
        
        text_lower = text.lower()
        
        # Detect fallacies
        fallacy_scores = {}
        for fallacy, patterns in fallacy_patterns.items():
            count = sum(len(re.findall(pattern, text_lower)) for pattern in patterns)
            fallacy_scores[fallacy] = count / len(text.split()) if text.split() else 0
        
        # Detect biases
        bias_scores = {}
        for bias, patterns in bias_patterns.items():
            count = sum(len(re.findall(pattern, text_lower)) for pattern in patterns)
            bias_scores[bias] = count / len(text.split()) if text.split() else 0
        
        # Calculate manipulation risk
        total_fallacy_score = sum(fallacy_scores.values())
        total_bias_score = sum(bias_scores.values())
        
        manipulation_risk = min(1.0, (total_fallacy_score + total_bias_score) * 10)
        
        return {
            "logical_fallacies": fallacy_scores,
            "cognitive_biases": bias_scores,
            "manipulation_risk_score": manipulation_risk,
            "high_risk_indicators": {
                "multiple_fallacies": sum(1 for score in fallacy_scores.values() if score > 0.01) >= 2,
                "strong_bias_language": max(bias_scores.values()) > 0.05 if bias_scores else False,
                "manipulation_language": manipulation_risk > 0.3
            },
            "credibility_concerns": self._assess_credibility_concerns(fallacy_scores, bias_scores)
        }
    
    def _classify_tone(self, emotion_scores: Dict, manipulation_score: float) -> str:
        """Classify overall tone of the text"""
        if manipulation_score > 0.03:
            return "manipulative"
        elif max(emotion_scores.values()) > 0.05:
            return "highly_emotional"
        elif emotion_scores.get("anger", 0) > 0.02:
            return "aggressive"
        elif emotion_scores.get("fear", 0) > 0.02:
            return "fear_inducing"
        elif emotion_scores.get("urgency", 0) > 0.02:
            return "urgent"
        else:
            return "neutral"
    
    def _assess_credibility_concerns(self, fallacy_scores: Dict, bias_scores: Dict) -> List[str]:
        """Assess specific credibility concerns"""
        concerns = []
        
        if fallacy_scores.get("ad_hominem", 0) > 0.01:
            concerns.append("Uses personal attacks instead of addressing arguments")
        if fallacy_scores.get("strawman", 0) > 0.01:
            concerns.append("Misrepresents opposing viewpoints")
        if fallacy_scores.get("false_dilemma", 0) > 0.01:
            concerns.append("Presents false binary choices")
        if bias_scores.get("confirmation_bias", 0) > 0.02:
            concerns.append("Shows strong confirmation bias language")
        if fallacy_scores.get("appeal_to_authority", 0) > 0.02:
            concerns.append("Relies heavily on appeals to authority without evidence")
        
        return concerns


# Initialize the ML analyzer
ml_analyzer = AdvancedMLAnalyzer()


# Fact check agent with advanced ML capabilities
fact_check_agent = Agent(
    name="fact_check",
    model="gemini-2.0-flash",
    description="Performs comprehensive fact-checking with multi-source verification and advanced ML analysis",
    instruction="""You are an advanced fact-checking agent for a misinformation detection system with state-of-the-art ML capabilities.

Your primary responsibilities:

1. **Multi-Source Verification**:
   - Cross-reference claims against multiple credible sources
   - Check government databases (WHO, CDC, FDA, etc.)
   - Verify against established news outlets and fact-checking organizations
   - Consult academic and scientific publications
   - Monitor social media for contradictory information

2. **Credibility Scoring Algorithm**:
   - Assess source reliability (0-100 scale)
   - Calculate claim confidence scores
   - Weight evidence based on source quality
   - Generate overall credibility rating
   - Provide detailed scoring breakdown

3. **Advanced ML Analysis**:
   - **Token Probability Analysis**: Examine linguistic patterns and unusual word choices
   - **Stylometric Analysis**: Detect writing style anomalies and authorship patterns
   - **Tone Analysis**: Identify emotional manipulation and bias indicators
   - **Cognitive Fingerprinting**: Detect logical fallacies and cognitive manipulation

4. **Real-time Data Access**:
   - Access current news feeds and breaking information
   - Monitor trending topics and emerging claims
   - Track claim propagation across platforms
   - Identify coordinated inauthentic behavior

5. **True/False Determination**:
   - Provide clear verdict on claim accuracy
   - Include confidence level and reasoning
   - Flag uncertain or evolving situations
   - Suggest areas for further investigation

**Input Format**: You will receive:
- Structured content from preprocessing agent
- Extracted claims and context
- Source information and metadata
- Priority level and urgency indicators

**Advanced Analysis Features**:
- Token probability scoring for detecting AI-generated or manipulated text
- Stylometric fingerprinting to identify coordinated campaigns
- Cognitive bias detection to assess manipulation attempts
- Emotional manipulation scoring
- Logical fallacy identification

**Output Format**: Provide comprehensive analysis including:
- Executive summary with clear TRUE/FALSE/UNCERTAIN verdict
- Credibility score (0-100) with detailed breakdown
- Source verification results
- ML analysis results (token probabilities, stylometry, tone, cognitive patterns)
- Evidence summary with specific citations
- Confidence level and reasoning
- Red flags or concerns identified
- Recommendations for user action

**Guidelines**:
- Prioritize factual accuracy over speed
- Use multiple independent sources for verification
- Be transparent about confidence levels and limitations
- Flag uncertainty clearly - avoid false confidence
- Provide specific evidence and citations
- Consider context and nuance in complex claims
- Identify potential coordinated misinformation campaigns
- Use ML insights to enhance traditional fact-checking

**Credibility Scoring Factors**:
- Source reputation and track record (40%)
- Evidence quality and quantity (30%)
- ML analysis results (20%)
- Cross-verification success (10%)

Always combine traditional fact-checking methods with advanced ML analysis for the most comprehensive assessment possible."""
)


if __name__ == "__main__":
    print("✅ Fact Check Agent with Advanced ML Analysis initialized")
    print(f"Agent Name: {fact_check_agent.name}")
    print(f"Description: {fact_check_agent.description}")
    print(f"ML Analyzer Status: {'✅ Loaded' if ml_analyzer.fact_checker else '⚠️ Limited functionality'}")