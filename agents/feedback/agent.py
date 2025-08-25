# Feedback Agent
# Role: Learn from user feedback and improve (with malicious use protection)

from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

from tools.feedback_processor import FeedbackProcessor
from tools.security_validator import SecurityValidator, LearningEngine

class FeedbackAgent:
    """
    Feedback Agent
    Role: Learn from user feedback and improve system performance
    Includes protection against malicious use and manipulation
    """
    
    def __init__(self):
        self.name = "feedback_agent"
        self.feedback_processor = FeedbackProcessor()
        self.security_validator = SecurityValidator()
        self.learning_engine = LearningEngine()
        
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Main feedback processing with security validation"""
        user_feedback = input_data.get("user_feedback", {})
        content_id = input_data.get("content_id")
        user_id = input_data.get("user_id", "anonymous")
        
        try:
            # Security validation
            security_check = self.security_validator.validate_feedback(
                user_feedback, user_id, content_id
            )
            
            if not security_check["is_valid"]:
                return {
                    "status": "rejected",
                    "reason": "Security validation failed",
                    "timestamp": get_current_time()
                }
            
            # Process feedback
            processed_feedback = self.feedback_processor.process_feedback(
                user_feedback, {}, content_id
            )
            
            # Update learning
            learning_update = self.learning_engine.update_from_feedback(
                processed_feedback, {}
            )
            
            return {
                "status": "accepted",
                "feedback_processed": True,
                "learning_impact": learning_update.get("impact", "minimal"),
                "timestamp": get_current_time()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": get_current_time()
            }
    
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
