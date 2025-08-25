import os
import sys
from dotenv import load_dotenv
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

# Load environment variables
load_dotenv()

# Add parent directory to path for importing sub-agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import Google ADK components
try:
    from google.adk import Agent
    from google.adk.models import Gemini
    from google.adk.tools import FunctionTool
    ADK_AVAILABLE = True
    print("✅ Google ADK imported successfully")
except ImportError as e:
    print(f"⚠️ Google ADK not available: {e}")
    ADK_AVAILABLE = False

# Import sub-agent classes
try:
    from content_intake.agent import ContentIntakeAgent
    from preprocessing_context.agent import PreprocessingContextAgent  
    from fact_check.agent import FactCheckAgent
    from knowledge.agent import KnowledgeAgent
    from feedback.agent import FeedbackAgent
    from realtime_alert.agent import RealtimeAlertAgent
    print("✅ Sub-agents imported successfully")
except ImportError as e:
    print(f"❌ Could not import sub-agents: {e}")
    sys.exit(1)

# Initialize sub-agents globally
content_intake = ContentIntakeAgent()
preprocessing = PreprocessingContextAgent()
fact_checker = FactCheckAgent()
knowledge = KnowledgeAgent()
feedback = FeedbackAgent()
realtime_alert = RealtimeAlertAgent()

def analyze_misinformation(content: str, content_type: str = "text") -> dict:
    """Sequential misinformation analysis pipeline using sub-agents"""
    print(f"🎯 ORCHESTRATOR: Delegating {content_type} content to sub-agents...")
    
    # Step 1: Content Intake
    intake_result = content_intake({
        "content": content,
        "content_type": content_type,
        "timestamp": get_current_time()
    })
    
    if intake_result.get("status") != "processed":
        return {"error": "Content intake failed", "details": intake_result}
    
    # Step 2: Preprocessing & Context Analysis
    preprocessing_result = preprocessing({
        "content": content,
        "content_type": content_type,
        "intake_data": intake_result
    })
    
    if preprocessing_result.get("status") not in ["processed", "completed"]:
        return {"error": "Preprocessing failed", "details": preprocessing_result}
    
    # Step 3: Fact Checking
    fact_result = fact_checker({
        "content": content,
        "content_type": content_type,
        "context_data": preprocessing_result
    })
    
    if fact_result.get("status") != "completed":
        return {"error": "Fact checking failed", "details": fact_result}
    
    # Step 4: Knowledge & Education
    knowledge_result = knowledge({
        "fact_check_result": fact_result,
        "content": content,
        "content_type": content_type
    })
    
    if knowledge_result.get("status") != "completed":
        return {"error": "Knowledge generation failed", "details": knowledge_result}
    
    # Compile final result
    return {
        "status": "analysis_complete",
        "timestamp": get_current_time(),
        "content_analysis": {
            "content_type": content_type,
            "word_count": intake_result.get("metadata", {}).get("word_count", 0),
            "claims_found": len(intake_result.get("extracted_claims", [])),
            "entities_detected": len(intake_result.get("entities", {}))
        },
        "credibility_assessment": {
            "score": fact_result.get("credibility_score", 0.5),
            "verdict": fact_result.get("overall_verdict", "uncertain"),
            "confidence": fact_result.get("confidence", 0.5)
        },
        "education": {
            "type": knowledge_result.get("education_type", "general"),
            "has_educational_content": bool(knowledge_result.get("educational_content")),
            "patterns_detected": len(knowledge_result.get("explanation", {}).get("patterns_detected", [])),
            "tips_provided": len(knowledge_result.get("actionable_tips", []))
        },
        "recommendations": knowledge_result.get("actionable_tips", [])[:3],  # Top 3 recommendations
        "pipeline_summary": f"Analyzed {content_type} content with {fact_result.get('credibility_score', 0.5):.1f} credibility score"
    }

def store_feedback(user_feedback: str, content_id: str = "", rating: int = 0) -> dict:
    """Store user feedback using feedback agent"""
    final_content_id = content_id if content_id else f"content_{get_current_time()}"
    final_rating = rating if rating > 0 else None
    
    return feedback({
        "user_feedback": {"rating": final_rating, "text": user_feedback},
        "content_id": final_content_id,
        "feedback_text": user_feedback,
        "timestamp": get_current_time()
    })

def check_alerts(content: str, urgency_level: str = "medium") -> dict:
    """Check for real-time alerts using realtime alert agent"""
    return realtime_alert({
        "action": "create_alert",
        "content": content,
        "urgency_level": urgency_level,
        "timestamp": get_current_time()
    })

# Create ADK tools
misinformation_tool = FunctionTool(analyze_misinformation)
feedback_tool = FunctionTool(store_feedback)  
alert_tool = FunctionTool(check_alerts)

# Create the ADK agent
if ADK_AVAILABLE and os.getenv('GOOGLE_API_KEY'):
    root_agent = Agent(
        name="misinformation_orchestrator",
        description="Sequential misinformation detection system that delegates to specialized sub-agents",
        model=Gemini(api_key=os.getenv('GOOGLE_API_KEY')),
        tools=[misinformation_tool, feedback_tool, alert_tool],
        instruction="""
You are a misinformation detection orchestrator that MUST use the provided tools to analyze content.

For misinformation analysis:
1. ALWAYS use analyze_misinformation tool with user's content
2. Present the results clearly with credibility score and recommendations
3. Explain what each step of the analysis found

For feedback:
1. Use store_feedback tool when users provide feedback
2. Acknowledge their input and explain how it helps improve the system

For alerts:
1. Use check_alerts tool for urgent or suspicious content
2. Explain the alert status to the user

NEVER analyze content yourself - always delegate to the tools which use specialized sub-agents.
        """.strip()
    )
    print("✅ ADK Agent created successfully with Gemini model")
else:
    print("❌ ADK Agent creation failed - missing API key or ADK unavailable")
    root_agent = None
