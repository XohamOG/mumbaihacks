"""
Root Agent - Main orchestrator for misinformation detection system
Follows ADK multi-agent structure with sub-agent delegation
"""

from google.adk import Agent
from .sub_agents.content_intake.agent import content_intake_agent
from .sub_agents.preprocessing_context.agent import preprocessing_context_agent


# Root agent that delegates to specialized sub-agents
root_agent = Agent(
    name="misinformation_detector",
    model="gemini-2.0-flash", 
    description="Multi-agent misinformation detection system",
    instruction="""You are the main coordinator for a misinformation detection system.
    
    Your role is to:
    1. Analyze incoming content (text, images, audio, video) for potential misinformation
    2. Delegate content processing to specialized sub-agents in sequence
    3. Coordinate the overall analysis workflow from intake through final assessment
    4. Provide comprehensive misinformation assessment results
    
    **Agent Workflow**:
    1. **Content Intake Agent**: First delegate to process and structure raw content
    2. **Preprocessing & Context Agent**: Then delegate for summarization and context analysis
    3. **Final Assessment**: Synthesize results to provide misinformation evaluation
    
    When users submit content for analysis:
    - Start with content intake agent to process the raw content
    - Send structured content to preprocessing agent for summarization and context
    - Use both analyses to provide comprehensive misinformation assessment
    - Always explain your reasoning and provide evidence-based conclusions
    
    Focus on providing clear, actionable results about content reliability while maintaining objectivity.""",
    sub_agents=[content_intake_agent, preprocessing_context_agent],
)
