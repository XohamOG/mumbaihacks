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
    from google.adk.models import Gemini, LlmRequest
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
except ImportError as e:
    print(f"Warning: Could not import sub-agents: {e}")
    # Create placeholder classes for missing agents
    class ContentIntakeAgent:
        def __call__(self, data): return {"status": "not_implemented", "agent": "content_intake"}
    class PreprocessingContextAgent:
        def __call__(self, data): return {"status": "not_implemented", "agent": "preprocessing_context"}
    class FactCheckAgent:
        def __call__(self, data): return {"status": "not_implemented", "agent": "fact_check"}
    class KnowledgeAgent:
        def __call__(self, data): return {"status": "not_implemented", "agent": "knowledge"}
    class FeedbackAgent:
        def __call__(self, data): return {"status": "not_implemented", "agent": "feedback"}
    class RealtimeAlertAgent:
        def __call__(self, data): return {"status": "not_implemented", "agent": "realtime_alert"}

# Create tools for the orchestrator agent
def create_content_intake_tool():
    """Tool to process content intake"""
    def content_intake_handler(content: str, content_type: str = "text") -> dict:
        """Process content through content intake agent"""
        try:
            intake_agent = ContentIntakeAgent()
            return intake_agent({
                "content": content,
                "content_type": content_type,
                "timestamp": get_current_time()
            })
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    if ADK_AVAILABLE:
        return FunctionTool(content_intake_handler)
    else:
        return content_intake_handler

def create_fact_check_tool():
    """Tool to perform fact checking"""
    def fact_check_handler(content: str, context_data: dict = None) -> dict:
        """Perform fact checking on content"""
        try:
            fact_check_agent = FactCheckAgent()
            return fact_check_agent({
                "content": content,
                "context_data": context_data or {},
                "content_type": "text"
            })
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    if ADK_AVAILABLE:
        return FunctionTool(fact_check_handler)
    else:
        return fact_check_handler

def create_knowledge_tool():
    """Tool to provide educational content"""
    def knowledge_handler(fact_check_result: dict, content: str) -> dict:
        """Generate educational content about misinformation"""
        try:
            knowledge_agent = KnowledgeAgent()
            return knowledge_agent({
                "fact_check_result": fact_check_result,
                "content": content,
                "content_type": "text"
            })
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    if ADK_AVAILABLE:
        return FunctionTool(knowledge_handler)
    else:
        return knowledge_handler
    """Base Agent class template"""
    
    def __init__(self, name, description, instruction):
        self.name = name
        self.description = description
        self.instruction = instruction
        
    def __call__(self, input_data):
        """Process input - to be implemented based on your logic"""
        return self.process(input_data)
    
    def process(self, input_data):
        """Template method - implement your processing logic here"""
        return {
            "status": "processed",
            "agent": self.name,
            "input": input_data,
            "output": "Processing logic to be implemented",
            "timestamp": get_current_time()
        }

class MisinformationOrchestrator:
    """Main orchestrator for misinformation detection and analysis"""
    
    def __init__(self, model=None):
        self.model = model
        self.sub_agents = {
            "content_intake": ContentIntakeAgent(),
            "preprocessing_context": PreprocessingContextAgent(),
            "fact_check": FactCheckAgent(),
            "knowledge": KnowledgeAgent(),
            "feedback": FeedbackAgent(),
            "realtime_alert": RealtimeAlertAgent()
        }
        
    def __call__(self, content, content_type="text"):
        """Process content through the misinformation detection pipeline"""
        return self.process_content(content, content_type)
        
    def process_content(self, content, content_type="text"):
        """Main processing pipeline"""
        try:
            pipeline_data = {
                "original_content": content,
                "content_type": content_type,
                "timestamp": get_current_time()
            }
            
            print(f"🎯 ORCHESTRATOR: Processing {content_type} content...")
            
            # Step 1: Content Intake
            print("📥 Phase 1: Content Intake")
            intake_result = self.route_to_agent("content_intake", {
                "content": content,
                "content_type": content_type,
                "timestamp": pipeline_data["timestamp"]
            })
            pipeline_data["intake_result"] = intake_result
            
            # Step 2: Preprocessing & Context Analysis
            print("🔍 Phase 2: Preprocessing & Context Analysis")
            context_result = self.route_to_agent("preprocessing_context", {
                "content": content,
                "content_type": content_type,
                "intake_data": intake_result
            })
            pipeline_data["context_result"] = context_result
            
            # Step 3: Fact Checking (Most Important)
            print("✅ Phase 3: Fact Checking")
            fact_result = self.route_to_agent("fact_check", {
                "content": content,
                "content_type": content_type,
                "context_data": context_result
            })
            pipeline_data["fact_result"] = fact_result
            
            # Step 4: Knowledge & Education
            print("🎓 Phase 4: Knowledge & Education")
            knowledge_result = self.route_to_agent("knowledge", {
                "fact_check_result": fact_result,
                "content": content,
                "content_type": content_type
            })
            pipeline_data["knowledge_result"] = knowledge_result
            
            # Step 5: Feedback Processing (if applicable)
            print("🔄 Phase 5: Feedback Processing")
            feedback_result = self.route_to_agent("feedback", {
                "pipeline_data": pipeline_data,
                "user_feedback": None  # Will be updated when user provides feedback
            })
            pipeline_data["feedback_result"] = feedback_result
            
            # Step 6: Real-time Alert (if needed)
            print("🚨 Phase 6: Real-time Alert Check")
            alert_result = self.route_to_agent("realtime_alert", {
                "fact_result": fact_result,
                "content": content,
                "urgency_level": fact_result.get("credibility_score", 0.5)
            })
            pipeline_data["alert_result"] = alert_result
            
            # Generate final report
            final_result = self.generate_final_report(pipeline_data)
            print("🎯 ORCHESTRATOR: Pipeline completed successfully!")
            return final_result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error": str(e),
                "phase": "orchestrator_processing",
                "timestamp": get_current_time()
            }
            print(f"❌ ORCHESTRATOR ERROR: {str(e)}")
            return error_result
    
    def route_to_agent(self, agent_name, data):
        """Route data to specific sub-agent"""
        try:
            agent = self.sub_agents.get(agent_name)
            if not agent:
                return {"status": "error", "error": f"Agent {agent_name} not found"}
            
            print(f"   → Routing to {agent_name.replace('_', ' ').title()} Agent")
            result = agent(data)
            print(f"   ✓ {agent_name.replace('_', ' ').title()} completed")
            return result
            
        except Exception as e:
            return {"status": "error", "error": str(e), "agent": agent_name}
    
    def generate_final_report(self, pipeline_data):
        """Generate comprehensive final report"""
        fact_result = pipeline_data.get("fact_result", {})
        knowledge_result = pipeline_data.get("knowledge_result", {})
        
        return {
            "status": "completed",
            "timestamp": pipeline_data["timestamp"],
            "content_type": pipeline_data.get("content_type", "text"),
            "credibility_assessment": {
                "score": fact_result.get("credibility_score", 0.5),
                "classification": fact_result.get("classification", "unknown"),
                "confidence": fact_result.get("confidence", 0.5)
            },
            "educational_content": knowledge_result.get("educational_content", ""),
            "misinformation_patterns": knowledge_result.get("patterns_detected", []),
            "recommendations": knowledge_result.get("recommendations", []),
            "pipeline_results": {
                "intake": pipeline_data.get("intake_result", {}),
                "context": pipeline_data.get("context_result", {}),
                "fact_check": pipeline_data.get("fact_result", {}),
                "knowledge": pipeline_data.get("knowledge_result", {}),
                "feedback": pipeline_data.get("feedback_result", {}),
                "alerts": pipeline_data.get("alert_result", {})
            }
        }

# Create the orchestrator agent instance
orchestrator = MisinformationOrchestrator()

# Create simple root_agent for ADK
if ADK_AVAILABLE:
    root_agent = Agent(
        name="misinformation_orchestrator",
        description="AI agent for detecting and analyzing misinformation across multiple content types",
        model=Gemini(api_key=os.getenv('GOOGLE_API_KEY')) if os.getenv('GOOGLE_API_KEY') else None,
        instruction="""
        You are a misinformation detection and analysis agent. When users provide content, you analyze it through multiple phases:
        1. Content intake and processing
        2. Context analysis and preprocessing
        3. Fact checking against reliable sources
        4. Educational content generation
        5. Feedback processing
        6. Real-time alert assessment
        
        Provide clear, helpful responses about content credibility and educational insights.
        """
    )
else:
    # For direct usage without ADK
    root_agent = orchestrator

# Example usage
if __name__ == "__main__":
    # Test with sample content
    test_content = "Sample news article or social media post to fact-check"
    
    result = orchestrator.process_content(test_content, "text")
    print("Orchestrator Result:")
    print(result)
