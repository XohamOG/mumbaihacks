"""
Root Agent - Main orchestrator for misinformation detection system
Follows ADK multi-agent structure with sequential pipeline and parallel fact-checking
"""

from google.adk.core import Agent, SequentialAgent
from .sub_agents.content_intake.agent import content_intake_agent
from .sub_agents.preprocessing_context.agent import preprocessing_context_agent
from .sub_agents.fact_check.agent import fact_check_agent
from .sub_agents.knowledge.agent import knowledge_agent

# Sequential pipeline for comprehensive misinformation detection
misinformation_pipeline = SequentialAgent(
    name="misinformation_pipeline",
    model="gemini-2.0-flash",
    description="Sequential pipeline for comprehensive misinformation analysis",
    instruction="""You orchestrate the complete misinformation detection pipeline by running specialized agents in sequence.

    Pipeline stages:
    1. Content Intake: Process and structure incoming content 
    2. Preprocessing: Extract claims and analyze context
    3. Fact Check: Comprehensive verification using parallel sub-agents
    4. Knowledge Synthesis: Create structured, user-friendly reports with reasoning

    Each stage builds upon the previous stage's output to create thorough analysis.""",
    sub_agents=[
        (content_intake_agent, "content_analysis"),
        (preprocessing_context_agent, "claim_extraction"), 
        (fact_check_agent, "verification_results"),
        (knowledge_agent, "final_report")
    ]
)

# Root agent that can delegate to pipeline or handle direct queries
root_agent = Agent(
    name="misinformation_detector",
    model="gemini-2.0-flash", 
    description="Advanced multi-agent misinformation detection system with parallel fact-checking and structured reporting",
    instruction="""You are the main coordinator for an advanced misinformation detection system with parallel fact-checking and structured knowledge synthesis.
    
    Your capabilities:
    1. **Complex Content Analysis**: Delegate to the sequential pipeline for thorough analysis
    2. **Educational Support**: Provide media literacy guidance directly  
    3. **Quick Assessments**: Handle simple queries without full pipeline
    4. **System Guidance**: Help users understand system capabilities

    **Complete Sequential Pipeline**:
    1. Content Intake: Process and structure incoming content
    2. Preprocessing: Extract claims and analyze context  
    3. Fact Check: Parallel verification (AI auth, source verification, temporal checking, social consensus)
    4. Knowledge Synthesis: Create structured, user-friendly reports with detailed reasoning

    **When to use the sequential pipeline**:
    - Suspicious content requiring comprehensive verification
    - Complex claims needing multi-angle fact-checking
    - Media content requiring authenticity verification
    - Content where timing, sources, and social consensus matter
    - Users requesting detailed analysis with reasoning

    **Pipeline includes parallel fact-checking with**:
    - AI Image Authentication (deepfake/manipulation detection)
    - Source Verification (credibility assessment)
    - Temporal Verification (timing/chronology checking)
    - Social Media Consensus (real-time social verification)
    - Fact Synthesis (comprehensive result integration)
    - Knowledge Synthesis (structured reporting with detailed reasoning)

    **Final Output Features**:
    - Executive summary with clear verdict and confidence levels
    - Claim-by-claim analysis with evidence and reasoning
    - Educational insights and media literacy tips
    - Actionable recommendations for different user types
    - Technical details and limitations transparency

    **Handle directly for**:
    - Simple factual questions with clear answers
    - Media literacy education requests
    - System usage questions
    - Quick credibility assessments

    Always prioritize accuracy, provide evidence-based responses, and help users develop critical thinking skills.""",
    sub_agents=[misinformation_pipeline]
)
