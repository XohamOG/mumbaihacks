from google.adk.core import Agent, SequentialAgent, ParallelAgent
from .subagents.ai_image_authentication.agent import ai_image_auth_agent
from .subagents.source_verification.agent import source_verification_agent
from .subagents.temporal_verification.agent import temporal_verification_agent
from .subagents.socialmedia_consensus.agent import socialmedia_consensus_agent
from .subagents.fact_synthesis.agent import fact_synthesis_agent

# Parallel agent for concurrent fact-checking operations
fact_verification_pipeline = ParallelAgent(
    name="fact_verification_pipeline",
    model="gemini-2.0-flash",
    description="Parallel pipeline for comprehensive fact verification",
    instruction="""You coordinate parallel fact-checking operations to verify content from multiple angles simultaneously.

    Your parallel verification process runs these agents concurrently:
    1. AI Image Authentication: Detects deepfakes and AI-generated media
    2. Source Verification: Evaluates credibility and reliability of sources
    3. Temporal Verification: Confirms timing and chronological accuracy
    4. Social Media Consensus: Checks real-time social media data and trends

    All agents run independently and simultaneously to maximize efficiency.""",
    sub_agents=[
        (ai_image_auth_agent, "ai_authenticity_check"),
        (source_verification_agent, "source_credibility"),
        (temporal_verification_agent, "temporal_accuracy"),
        (socialmedia_consensus_agent, "social_consensus")
    ]
)

# Sequential agent that first runs parallel verification, then synthesis
fact_check_agent = SequentialAgent(
    name="fact_check",
    model="gemini-2.0-flash",
    description="Comprehensive fact-checking system with parallel verification and synthesis",
    instruction="""You are the main fact-checking agent that orchestrates comprehensive verification.

    Your workflow:
    1. PARALLEL VERIFICATION: Run multiple verification checks simultaneously
    2. SYNTHESIS: Combine all verification results into final assessment

    You receive processed claims from the preprocessing agent and must:
    - Coordinate parallel verification across multiple domains
    - Synthesize results into coherent, actionable conclusions
    - Provide confidence scores and evidence trails
    - Identify contradictions and resolve conflicts in findings

    Access previous pipeline outputs: {content_analysis} and {claim_extraction}""",
    sub_agents=[
        (fact_verification_pipeline, "verification_results"),
        (fact_synthesis_agent, "final_fact_check")
    ]
)
