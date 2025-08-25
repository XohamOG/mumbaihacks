"""
Root Agent - Main orchestrator for misinformation detection system
Follows ADK multi-agent structure with sub-agent delegation
"""

from google.adk import Agent
from .sub_agents.content_intake.agent import content_intake_agent


# Root agent that delegates to specialized sub-agents
root_agent = Agent(
    name="misinformation_detector",
    model="gemini-2.0-flash", 
    description="Multi-agent misinformation detection system",
    instruction="""You are the main coordinator for a misinformation detection system.
    
    Your role is to:
    1. Analyze incoming content (text, images, audio, video) for potential misinformation
    2. Delegate content processing to specialized sub-agents based on content type
    3. Coordinate the overall analysis workflow
    4. Provide comprehensive misinformation assessment results
    
    When users submit content for analysis:
    - First delegate to the content intake agent to process and structure the content
    - Then proceed with fact-checking and credibility assessment
    - Provide clear, actionable results about the content's reliability
    
    Always be thorough but concise in your analysis. Focus on providing evidence-based 
    assessments while explaining your reasoning clearly.""",
    sub_agents=[content_intake_agent],
)
