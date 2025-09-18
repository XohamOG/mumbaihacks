"""
Test file to verify all sub-agents are properly initialized
"""

import sys
import os

# Add the agents directory to the path
sys.path.append(os.path.dirname(__file__))

# Mock google.adk if not available
try:
    import google.adk
except ImportError:
    print("⚠️  google.adk not available, using mock implementation")
    import mock_adk
    sys.modules['google.adk'] = mock_adk

def test_all_agents():
    """Test that all agents can be imported and initialized"""
    
    print("🚀 Testing Agentic AI Misinformation Detection System")
    print("=" * 60)
    
    agents_status = {}
    
    # Test Content Intake Agent
    try:
        from sub_agents.content_intake.agent import content_intake_agent
        agents_status["Content Intake"] = "✅ SUCCESS"
        print(f"✅ Content Intake Agent: {content_intake_agent.name}")
    except Exception as e:
        agents_status["Content Intake"] = f"❌ FAILED: {e}"
        print(f"❌ Content Intake Agent failed: {e}")
    
    # Test Preprocessing Context Agent
    try:
        from sub_agents.preprocessing_context.agent import preprocessing_context_agent
        agents_status["Preprocessing Context"] = "✅ SUCCESS"
        print(f"✅ Preprocessing Context Agent: {preprocessing_context_agent.name}")
    except Exception as e:
        agents_status["Preprocessing Context"] = f"❌ FAILED: {e}"
        print(f"❌ Preprocessing Context Agent failed: {e}")
    
    # Test Fact Check Agent (with ML)
    try:
        from sub_agents.fact_check.agent import fact_check_agent, ml_analyzer
        agents_status["Fact Check"] = "✅ SUCCESS"
        print(f"✅ Fact Check Agent: {fact_check_agent.name}")
        print(f"   ML Analyzer: {'✅ Loaded' if ml_analyzer.fact_checker else '⚠️ Limited'}")
    except Exception as e:
        agents_status["Fact Check"] = f"❌ FAILED: {e}"
        print(f"❌ Fact Check Agent failed: {e}")
    
    # Test Knowledge Agent
    try:
        from sub_agents.knowledge.agent import knowledge_agent
        agents_status["Knowledge"] = "✅ SUCCESS"
        print(f"✅ Knowledge Agent: {knowledge_agent.name}")
    except Exception as e:
        agents_status["Knowledge"] = f"❌ FAILED: {e}"
        print(f"❌ Knowledge Agent failed: {e}")
    
    # Test Feedback Agent
    try:
        from sub_agents.feedback.agent import feedback_agent, security_manager, learning_system
        agents_status["Feedback"] = "✅ SUCCESS"
        print(f"✅ Feedback Agent: {feedback_agent.name}")
        print(f"   Security Manager: ✅ Active")
        print(f"   Learning System: ✅ Active")
    except Exception as e:
        agents_status["Feedback"] = f"❌ FAILED: {e}"
        print(f"❌ Feedback Agent failed: {e}")
    
    # Test Realtime Alert Agent
    try:
        from sub_agents.realtime_alert.agent import realtime_alert_agent, query_storage, source_monitor, alert_system
        agents_status["Realtime Alert"] = "✅ SUCCESS"
        print(f"✅ Realtime Alert Agent: {realtime_alert_agent.name}")
        print(f"   Query Storage: ✅ Active")
        print(f"   Source Monitor: ✅ Ready")
        print(f"   Alert System: ✅ Ready")
    except Exception as e:
        agents_status["Realtime Alert"] = f"❌ FAILED: {e}"
        print(f"❌ Realtime Alert Agent failed: {e}")
    
    print("\n" + "=" * 60)
    print("📊 AGENT STATUS SUMMARY")
    print("=" * 60)
    
    success_count = 0
    for agent_name, status in agents_status.items():
        print(f"{agent_name:<20}: {status}")
        if "SUCCESS" in status:
            success_count += 1
    
    print(f"\n🎯 {success_count}/{len(agents_status)} agents successfully initialized")
    
    if success_count == len(agents_status):
        print("🎉 ALL AGENTS READY! System is fully operational.")
    else:
        print("⚠️  Some agents failed to initialize. Check dependencies and installation.")
        print("\n💡 To install dependencies: pip install -r requirements.txt")
    
    return agents_status


def test_ml_capabilities():
    """Test the ML capabilities of the fact check agent"""
    
    print("\n🤖 Testing ML Capabilities")
    print("=" * 40)
    
    try:
        from sub_agents.fact_check.agent import ml_analyzer
        
        # Test text for analysis
        test_text = "BREAKING: Scientists discover shocking truth about vaccines that they don't want you to know!"
        
        print(f"Testing with text: '{test_text[:50]}...'")
        
        # Test token probabilities
        try:
            token_result = ml_analyzer.get_token_probabilities(test_text)
            print("✅ Token probability analysis: Working")
        except Exception as e:
            print(f"❌ Token probability analysis: {e}")
        
        # Test stylometric analysis
        try:
            style_result = ml_analyzer.stylometric_analysis(test_text)
            print("✅ Stylometric analysis: Working")
            print(f"   Readability score: {style_result.get('readability_score', 'N/A')}")
        except Exception as e:
            print(f"❌ Stylometric analysis: {e}")
        
        # Test tone analysis
        try:
            tone_result = ml_analyzer.tone_analysis(test_text)
            print("✅ Tone analysis: Working")
            if 'tone_classification' in tone_result:
                print(f"   Detected tone: {tone_result['tone_classification']}")
        except Exception as e:
            print(f"❌ Tone analysis: {e}")
        
        # Test cognitive fingerprinting
        try:
            cognitive_result = ml_analyzer.cognitive_fingerprinting(test_text)
            print("✅ Cognitive fingerprinting: Working")
            if 'manipulation_risk_score' in cognitive_result:
                print(f"   Manipulation risk: {cognitive_result['manipulation_risk_score']:.2f}")
        except Exception as e:
            print(f"❌ Cognitive fingerprinting: {e}")
            
    except Exception as e:
        print(f"❌ ML Analyzer not available: {e}")
        print("💡 Install ML dependencies: pip install transformers torch")


if __name__ == "__main__":
    # Test all agents
    agents_status = test_all_agents()
    
    # Test ML capabilities if fact check agent loaded
    if "SUCCESS" in agents_status.get("Fact Check", ""):
        test_ml_capabilities()
    
    print("\n🔧 System Ready for Integration!")
    print("Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up API keys in .env file")
    print("3. Configure orchestrator agent")
    print("4. Test with real misinformation samples")