# Feedback Agent
# Role: Learn from user feedback and improve (with malicious use protection)

import os
import re
import hashlib
from datetime import datetime, timedelta

def get_current_time():
    return datetime.now().isoformat()

class FeedbackAgent:
    """
    Feedback Agent
    Role: Learn from user feedback and improve system performance
    Includes protection against malicious use and manipulation
    """
    
    def __init__(self):
        self.name = "feedback_agent"
        
        # Security settings
        self.max_feedback_per_user_per_day = 50
        self.min_feedback_length = 10
        self.max_feedback_length = 1000
        
        # Feedback categories
        self.feedback_types = [
            "accuracy_feedback",
            "false_positive",
            "false_negative", 
            "source_suggestion",
            "general_improvement",
            "bug_report",
            "feature_request"
        ]
        
        # Malicious patterns to detect
        self.malicious_patterns = [
            r"ignore previous instructions",
            r"system prompt",
            r"jailbreak",
            r"bypass security",
            r"admin override",
            r"root access",
            r"sudo",
            r"delete all",
            r"drop table"
        ]
        
        # Quality indicators
        self.quality_indicators = {
            "constructive_words": ["improve", "suggest", "better", "helpful", "accurate", "correction"],
            "spam_patterns": [r"(.)\1{5,}", r"[A-Z]{10,}", r"www\.", r"http", r"click here"],
            "offensive_patterns": [r"f[*]+k", r"sh[*]+t", r"damn", r"hell", r"stupid", r"idiot"]
        }
        
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Main feedback processing with security validation"""
        user_feedback = input_data.get("user_feedback", {})
        content_id = input_data.get("content_id", "unknown")
        user_id = input_data.get("user_id", "anonymous")
        feedback_text = input_data.get("feedback_text", "")
        
        try:
            # Security validation first
            security_check = self.validate_feedback_security(
                user_feedback, user_id, content_id, feedback_text
            )
            
            if not security_check["is_valid"]:
                return {
                    "status": "rejected",
                    "reason": security_check["reason"],
                    "security_warning": security_check.get("warning", ""),
                    "timestamp": get_current_time()
                }
            
            # Process valid feedback
            processed_feedback = self.process_feedback(
                user_feedback, feedback_text, content_id, user_id
            )
            
            # Extract learning insights
            learning_insights = self.extract_learning_insights(processed_feedback)
            
            # Generate improvement suggestions
            improvement_suggestions = self.generate_improvement_suggestions(processed_feedback)
            
            return {
                "status": "processed",
                "feedback_id": self.generate_feedback_id(user_id, content_id),
                "feedback_summary": processed_feedback["summary"],
                "feedback_type": processed_feedback["type"],
                "quality_score": processed_feedback["quality_score"],
                "learning_insights": learning_insights,
                "improvement_suggestions": improvement_suggestions,
                "acknowledgment": "Thank you for your feedback! It helps improve our fact-checking accuracy.",
                "next_steps": processed_feedback["recommended_actions"],
                "timestamp": get_current_time()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": get_current_time()
            }
    
    def validate_feedback_security(self, user_feedback, user_id, content_id, feedback_text):
        """Validate feedback for security issues and malicious use"""
        
        # Check for malicious patterns
        combined_text = f"{user_feedback} {feedback_text}".lower()
        for pattern in self.malicious_patterns:
            if re.search(pattern, combined_text, re.IGNORECASE):
                return {
                    "is_valid": False,
                    "reason": "Potentially malicious content detected",
                    "warning": f"Pattern detected: {pattern}"
                }
        
        # Check text length
        if len(feedback_text) < self.min_feedback_length and feedback_text:
            return {
                "is_valid": False,
                "reason": "Feedback too short to be meaningful"
            }
        
        if len(feedback_text) > self.max_feedback_length:
            return {
                "is_valid": False,
                "reason": "Feedback exceeds maximum length"
            }
        
        # Check for spam patterns
        for pattern in self.quality_indicators["spam_patterns"]:
            if re.search(pattern, feedback_text, re.IGNORECASE):
                return {
                    "is_valid": False,
                    "reason": "Spam pattern detected"
                }
        
        # Rate limiting simulation (in production, would use actual database)
        # This is a simplified check
        user_hash = hashlib.md5(user_id.encode()).hexdigest()[:8]
        if user_id != "anonymous" and len(user_id) < 3:  # Very short user IDs might be suspicious
            return {
                "is_valid": False,
                "reason": "Suspicious user identifier"
            }
        
        return {"is_valid": True}
    
    def process_feedback(self, user_feedback, feedback_text, content_id, user_id):
        """Process validated feedback and extract insights"""
        
        # Determine feedback type
        feedback_type = self.classify_feedback_type(user_feedback, feedback_text)
        
        # Calculate quality score
        quality_score = self.calculate_feedback_quality(feedback_text, user_feedback)
        
        # Extract key information
        summary = self.summarize_feedback(user_feedback, feedback_text)
        
        # Determine recommended actions
        recommended_actions = self.determine_actions(feedback_type, user_feedback)
        
        return {
            "type": feedback_type,
            "quality_score": quality_score,
            "summary": summary,
            "recommended_actions": recommended_actions,
            "processed_at": get_current_time()
        }
    
    def classify_feedback_type(self, user_feedback, feedback_text):
        """Classify the type of feedback received"""
        feedback_lower = f"{user_feedback} {feedback_text}".lower()
        
        # Check for specific feedback types
        if any(word in feedback_lower for word in ["wrong", "incorrect", "false positive"]):
            return "false_positive"
        elif any(word in feedback_lower for word in ["missed", "false negative", "should have caught"]):
            return "false_negative"
        elif any(word in feedback_lower for word in ["source", "reference", "link", "citation"]):
            return "source_suggestion"
        elif any(word in feedback_lower for word in ["bug", "error", "broken", "not working"]):
            return "bug_report"
        elif any(word in feedback_lower for word in ["feature", "improvement", "suggestion", "could be better"]):
            return "feature_request"
        elif any(word in feedback_lower for word in ["accurate", "correct", "good", "helpful"]):
            return "positive_feedback"
        else:
            return "general_feedback"
    
    def calculate_feedback_quality(self, feedback_text, user_feedback):
        """Calculate quality score for feedback (0-1)"""
        score = 0.5  # Base score
        
        if not feedback_text:
            return 0.3  # Low score for empty feedback
        
        # Length bonus (reasonable length gets higher score)
        if 50 <= len(feedback_text) <= 500:
            score += 0.2
        
        # Constructive language bonus
        constructive_count = sum(1 for word in self.quality_indicators["constructive_words"] 
                                if word in feedback_text.lower())
        score += min(constructive_count * 0.1, 0.2)
        
        # Specific details bonus
        if any(word in feedback_text.lower() for word in ["because", "example", "specifically", "url", "source"]):
            score += 0.1
        
        # Penalty for offensive language
        offensive_count = sum(1 for pattern in self.quality_indicators["offensive_patterns"]
                             if re.search(pattern, feedback_text, re.IGNORECASE))
        score -= offensive_count * 0.2
        
        return max(0.0, min(1.0, score))
    
    def summarize_feedback(self, user_feedback, feedback_text):
        """Create a summary of the feedback"""
        if feedback_text:
            # Take first sentence or first 100 characters
            first_sentence = feedback_text.split('.')[0]
            if len(first_sentence) <= 100:
                return first_sentence.strip()
            else:
                return feedback_text[:100].strip() + "..."
        elif isinstance(user_feedback, dict):
            return f"Structured feedback: {list(user_feedback.keys())}"
        else:
            return str(user_feedback)[:100] + "..." if len(str(user_feedback)) > 100 else str(user_feedback)
    
    def determine_actions(self, feedback_type, user_feedback):
        """Determine recommended actions based on feedback type"""
        action_map = {
            "false_positive": [
                "Review fact-checking algorithms for this content type",
                "Adjust sensitivity thresholds",
                "Add content to whitelist if appropriate"
            ],
            "false_negative": [
                "Enhance detection patterns",
                "Review missed content for common characteristics",
                "Update training data"
            ],
            "source_suggestion": [
                "Evaluate suggested source for credibility",
                "Consider adding to trusted sources list",
                "Update source database"
            ],
            "bug_report": [
                "Log bug for developer review",
                "Test reproduction steps",
                "Prioritize based on impact"
            ],
            "feature_request": [
                "Evaluate feature feasibility",
                "Add to product roadmap consideration",
                "Gather more user feedback on feature"
            ],
            "positive_feedback": [
                "Log success metrics",
                "Identify successful patterns to replicate",
                "Share with development team"
            ]
        }
        
        return action_map.get(feedback_type, ["Review feedback for general improvements"])
    
    def extract_learning_insights(self, processed_feedback):
        """Extract learning insights from processed feedback"""
        insights = []
        
        feedback_type = processed_feedback["type"]
        quality_score = processed_feedback["quality_score"]
        
        if feedback_type == "false_positive" and quality_score > 0.6:
            insights.append({
                "type": "accuracy_issue",
                "description": "High-quality feedback indicates potential false positive",
                "priority": "high",
                "category": "fact_checking_accuracy"
            })
        
        elif feedback_type == "false_negative" and quality_score > 0.6:
            insights.append({
                "type": "detection_gap",
                "description": "Missed misinformation identified by user",
                "priority": "high",
                "category": "detection_improvement"
            })
        
        elif feedback_type == "source_suggestion":
            insights.append({
                "type": "source_enhancement",
                "description": "User provided additional source information",
                "priority": "medium",
                "category": "source_expansion"
            })
        
        return insights
    
    def generate_improvement_suggestions(self, processed_feedback):
        """Generate specific improvement suggestions"""
        suggestions = []
        
        feedback_type = processed_feedback["type"]
        
        if feedback_type == "false_positive":
            suggestions.append("Review the specific content patterns that triggered false detection")
            suggestions.append("Consider adjusting threshold parameters for similar content")
        
        elif feedback_type == "false_negative":
            suggestions.append("Analyze the missed content for new misinformation patterns")
            suggestions.append("Update detection algorithms to catch similar cases")
        
        elif feedback_type == "source_suggestion":
            suggestions.append("Verify the credibility of the suggested source")
            suggestions.append("If credible, add to fact-checking source database")
        
        elif feedback_type == "bug_report":
            suggestions.append("Reproduce the reported issue in testing environment")
            suggestions.append("Fix and test the resolution before deployment")
        
        else:
            suggestions.append("Review feedback for general system improvements")
        
        return suggestions
    
    def generate_feedback_id(self, user_id, content_id):
        """Generate unique feedback ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_hash = hashlib.md5(user_id.encode()).hexdigest()[:6]
        content_hash = hashlib.md5(str(content_id).encode()).hexdigest()[:6]
        
        return f"FB_{timestamp}_{user_hash}_{content_hash}"
    
    def process_quality_feedback(self, input_data):
        """Process feedback about system quality and accuracy"""
        quality_feedback = input_data.get("quality_feedback", {})
        fact_check_id = input_data.get("fact_check_id")
        
        # Validate quality feedback
        if not self.validate_quality_feedback(quality_feedback):
            return {
                "status": "invalid_feedback",
                "message": "Quality feedback must include rating and specific areas"
            }
        
        # Process quality improvements
        improvements = self.learning_engine.process_quality_feedback(
            quality_feedback, fact_check_id
        )
        
        return {
            "status": "quality_feedback_processed",
            "improvements_identified": improvements,
            "system_updates": self.get_system_updates(improvements),
            "timestamp": get_current_time()
        }
    
    def process_correction_feedback(self, input_data):
        """Process user corrections to fact-check results"""
        correction = input_data.get("correction", {})
        original_result = input_data.get("original_result", {})
        user_expertise = input_data.get("user_expertise", {})
        
        # Enhanced security for corrections (higher impact)
        security_check = self.security_validator.validate_correction(
            correction, user_expertise, original_result
        )
        
        if not security_check["is_valid"]:
            return {
                "status": "correction_rejected",
                "reason": security_check["rejection_reason"],
                "timestamp": get_current_time()
            }
        
        # Process correction with appropriate weighting
        correction_result = self.learning_engine.process_correction(
            correction, original_result, user_expertise
        )
        
        return {
            "status": "correction_processed",
            "correction_accepted": correction_result["accepted"],
            "confidence_impact": correction_result["confidence_change"],
            "model_updates": correction_result["updates"],
            "requires_human_review": correction_result.get("needs_review", False),
            "timestamp": get_current_time()
        }
    
    def generate_feedback_response(self, processed_feedback, learning_update):
        """Generate appropriate response to user feedback"""
        feedback_type = processed_feedback.get("type")
        sentiment = processed_feedback.get("sentiment", "neutral")
        
        responses = {
            "accuracy_feedback": {
                "positive": "Thank you for confirming our analysis was helpful. This reinforces our fact-checking methods.",
                "negative": "We appreciate your feedback about our accuracy. We're continuously improving our verification processes.",
                "neutral": "Thank you for your feedback about the fact-checking accuracy. Your input helps us improve."
            },
            "usefulness_feedback": {
                "positive": "We're glad our educational content was useful! This helps us provide better information.",
                "negative": "Thank you for letting us know our explanation wasn't helpful. We'll work to make our content clearer.",
                "neutral": "Thank you for rating the usefulness of our content. Your feedback guides our improvements."
            },
            "suggestion": {
                "positive": "Thank you for your constructive suggestion! We'll consider implementing this improvement.",
                "negative": "We appreciate your concern and will review our processes to address this issue.",
                "neutral": "Thank you for your suggestion. We review all user input to improve our system."
            }
        }
        
        response_template = responses.get(feedback_type, responses["usefulness_feedback"])
        acknowledgment = response_template.get(sentiment, response_template["neutral"])
        
        return {
            "acknowledgment": acknowledgment,
            "learning_noted": learning_update.get("impact", "minimal") != "minimal",
            "follow_up_needed": processed_feedback.get("requires_follow_up", False)
        }
    
    def validate_quality_feedback(self, quality_feedback):
        """Validate quality feedback structure"""
        required_fields = ["rating", "areas"]
        return all(field in quality_feedback for field in required_fields)
    
    def get_system_updates(self, improvements):
        """Get summary of system updates from improvements"""
        updates = []
        
        for improvement in improvements:
            improvement_type = improvement.get("type")
            if improvement_type == "accuracy_improvement":
                updates.append("Enhanced fact-checking accuracy algorithms")
            elif improvement_type == "source_expansion":
                updates.append("Expanded source verification database")
            elif improvement_type == "explanation_clarity":
                updates.append("Improved explanation clarity and detail")
            elif improvement_type == "speed_optimization":
                updates.append("Optimized processing speed")
        
        return updates
    
    def get_learning_stats(self):
        """Get statistics about learning from feedback"""
        return {
            "total_feedback_processed": self.learning_engine.get_feedback_count(),
            "accuracy_improvements": self.learning_engine.get_accuracy_improvements(),
            "user_satisfaction_trend": self.learning_engine.get_satisfaction_trend(),
            "common_improvement_areas": self.learning_engine.get_common_improvements(),
            "security_rejections": self.security_validator.get_rejection_stats(),
            "timestamp": get_current_time()
        }
    
    def export_learning_data(self, admin_key):
        """Export learning data for analysis (admin only)"""
        if not self.security_validator.validate_admin_access(admin_key):
            return {"error": "Unauthorized access"}
        
        return {
            "anonymized_feedback_data": self.learning_engine.get_anonymized_data(),
            "learning_model_performance": self.learning_engine.get_model_performance(),
            "security_incident_summary": self.security_validator.get_security_summary(),
            "timestamp": get_current_time()
        }

# Example usage
if __name__ == "__main__":
    agent = FeedbackAgent()
    
    # Mock feedback input
    mock_input = {
        "user_feedback": {
            "type": "accuracy_feedback",
            "rating": 4,
            "comment": "The fact-check was accurate and helpful",
            "specific_areas": ["source_quality", "explanation_clarity"]
        },
        "content_id": "content_12345",
        "user_id": "user_67890",
        "fact_check_result": {
            "verdict": "verified",
            "credibility_score": 0.8,
            "sources_checked": 5
        }
    }
    
    result = agent(mock_input)
    print("Feedback Agent Result:")
    print(result)
