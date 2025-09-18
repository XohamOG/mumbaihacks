"""
Mock Google ADK for testing purposes when the actual library is not available
"""

class Agent:
    """Mock Agent class that mimics the google.adk.Agent interface"""
    
    def __init__(self, name, model, description, instruction):
        self.name = name
        self.model = model
        self.description = description
        self.instruction = instruction
        
    def __call__(self, input_data):
        """Mock implementation of agent execution"""
        return {
            "agent": self.name,
            "model": self.model,
            "input": input_data,
            "output": f"Mock response from {self.name} agent",
            "status": "mock_execution"
        }
    
    def __repr__(self):
        return f"Agent(name='{self.name}', model='{self.model}')"