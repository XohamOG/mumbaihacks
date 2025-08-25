"""
Test script to verify ADK multi-agent structure
Run this to ensure all agents are properly imported and structured
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_agent_structure():
    """Test that all agents can be imported correctly"""
    print("🧪 Testing ADK Multi-Agent Structure")
    print("=" * 50)
    
    try:
        # Test root agent import
        print("📍 Testing root agent import...")
        from agent import root_agent
        print(f"✅ Root agent imported: {root_agent.name}")
        print(f"   Description: {root_agent.description}")
        print(f"   Model: {root_agent.model}")
        print(f"   Sub-agents: {len(root_agent.sub_agents)}")
        
        # Test sub-agent imports
        print("\n📍 Testing sub-agent imports...")
        from sub_agents.content_intake.agent import content_intake_agent
        print(f"✅ Content intake agent imported: {content_intake_agent.name}")
        print(f"   Description: {content_intake_agent.description}")
        
        # Test package imports
        print("\n📍 Testing package imports...")
        from sub_agents.content_intake import content_intake_agent as cia_package
        print(f"✅ Package import successful: {cia_package.name}")
        
        print("\n" + "=" * 50)
        print("✅ ALL IMPORTS SUCCESSFUL!")
        print("\nYou can now run: adk web")
        print("The multi-agent system should appear in the dropdown.")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("Check the agent structure and imports.")

if __name__ == "__main__":
    test_agent_structure()
