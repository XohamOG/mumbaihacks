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

class Agent:
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
    """Root Orchestrator Agent - Delegates tasks to specialized sub-agents"""
    
    def __init__(self):
        self.root_agent = Agent(
            name="root_orchestrator",
            description="Root agent that delegates tasks to specialized sub-agents",
            instruction="""
            You are the root orchestrator agent responsible for delegating tasks to specialized sub-agents.
            Your workflow:
            1. Receive user input/content
            2. Determine content type and route to Content Intake Agent
            3. Route processed content through the analysis pipeline
            4. Coordinate between agents and synthesize final results
            5. Handle unsolved queries via Realtime FactCheck Alert Agent
            """
        )
        
        # Initialize all sub-agents with actual instances
        self.sub_agents = {
            "content_intake": ContentIntakeAgent(),           # Processes all content forms 
            "preprocessing_context": PreprocessingContextAgent(),    # Summarizes context
            "fact_check": FactCheckAgent(),              # Most important - fact checks
            "knowledge": KnowledgeAgent(),               # Educates about misinformation
            "feedback": FeedbackAgent(),                # Learns from user feedback
            "realtime_alert": RealtimeAlertAgent()           # Handles unsolved queries
        }
        
        # Database for unsolved queries (to be implemented)
        self.unsolved_queries_db = []
        
    def process_content(self, content, content_type="text", user_id=None):
        """
        Main orchestration workflow
        """
        try:
            # Step 1: Content Intake - Process all forms of content
            intake_result = self.route_to_agent("content_intake", {
                "content": content,
                "content_type": content_type,
                "timestamp": get_current_time()
            })
            
            # Step 2: Preprocessing & Context - Summarize and prepare for analysis
            context_result = self.route_to_agent("preprocessing_context", {
                "processed_content": intake_result,
                "original_content": content
            })
            
            # Step 3: Fact Check - Most critical step with credibility scoring
            fact_check_result = self.route_to_agent("fact_check", {
                "context_data": context_result,
                "content": content,
                "content_type": content_type
            })
            
            # Step 4: Knowledge Agent - Education if misinformation detected
            knowledge_result = None
            if fact_check_result and fact_check_result.get("is_misinformation", False):
                knowledge_result = self.route_to_agent("knowledge", {
                    "fact_check_data": fact_check_result,
                    "content": content
                })
            
            # Step 5: Handle unsolved queries
            if fact_check_result and fact_check_result.get("status") == "unsolved":
                self.handle_unsolved_query(content, content_type, user_id, fact_check_result)
            
            # Synthesize final results
            final_result = self.synthesize_results({
                "intake": intake_result,
                "context": context_result,
                "fact_check": fact_check_result,
                "knowledge": knowledge_result,
                "timestamp": get_current_time()
            })
            
            return final_result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": get_current_time()
            }
    
    def route_to_agent(self, agent_name, data):
        """Route data to specific sub-agent"""
        if agent_name in self.sub_agents and self.sub_agents[agent_name]:
            try:
                # Delegate to the actual sub-agent
                result = self.sub_agents[agent_name](data)
                return result
            except Exception as e:
                return {
                    "status": "agent_error",
                    "agent": agent_name,
                    "error": str(e),
                    "message": f"Error occurred while processing with {agent_name} agent",
                    "data": data
                }
        else:
            return {
                "status": "agent_not_available",
                "agent": agent_name,
                "message": f"{agent_name} agent is not available or initialized",
                "data": data
            }
    
    def handle_unsolved_query(self, content, content_type, user_id, fact_check_result):
        """Handle queries that couldn't be definitively classified"""
        unsolved_query = {
            "id": f"unsolved_{len(self.unsolved_queries_db)}_{get_current_time()}",
            "content": content,
            "content_type": content_type,
            "user_id": user_id,
            "fact_check_result": fact_check_result,
            "timestamp": get_current_time(),
            "status": "pending_resolution"
        }
        
        self.unsolved_queries_db.append(unsolved_query)
        
        # Route to Realtime Alert Agent for monitoring and future resolution
        return self.route_to_agent("realtime_alert", {
            "query": unsolved_query,
            "action": "store_and_monitor"
        })
    
    def resolve_unsolved_query(self, query_id, resolution_data):
        """Resolve a previously unsolved query and alert the user"""
        for query in self.unsolved_queries_db:
            if query["id"] == query_id:
                query["status"] = "resolved"
                query["resolution"] = resolution_data
                query["resolved_at"] = get_current_time()
                
                # Alert the user via Realtime Alert Agent
                return self.route_to_agent("realtime_alert", {
                    "query": query,
                    "action": "send_alert",
                    "resolution": resolution_data
                })
        
        return {"status": "query_not_found", "query_id": query_id}
    
    def process_feedback(self, feedback_data, user_id):
        """Process user feedback through Feedback Agent with malicious use protection"""
        return self.route_to_agent("feedback", {
            "feedback": feedback_data,
            "user_id": user_id,
            "timestamp": get_current_time(),
            "security_check": True  # Enable malicious use protection
        })
    
    def synthesize_results(self, agent_results):
        """Combine results from multiple agents into final response"""
        fact_check = agent_results.get("fact_check", {})
        knowledge = agent_results.get("knowledge", {})
        
        # Determine final verdict
        is_misinformation = fact_check.get("is_misinformation", False)
        credibility_score = fact_check.get("credibility_score", 0.5)
        
        return {
            "status": "completed",
            "verdict": {
                "is_misinformation": is_misinformation,
                "credibility_score": credibility_score,
                "confidence": fact_check.get("confidence", 0.0)
            },
            "analysis": {
                "fact_check_summary": fact_check.get("summary", ""),
                "sources_checked": fact_check.get("sources", []),
                "education": knowledge.get("explanation", "") if knowledge else ""
            },
            "agent_results": agent_results,
            "timestamp": get_current_time()
        }

# Example usage
if __name__ == "__main__":
    orchestrator = MisinformationOrchestrator()
    
    # Test with sample content
    test_content = "Sample news article or social media post to fact-check"
    
    result = orchestrator.process_content(test_content, "text", user_id="user123")
    print("Orchestrator Result:")
    print(result)
