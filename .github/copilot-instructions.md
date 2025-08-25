# Copilot Instructions for Agentic AI Misinformation Project

## Project Status: ✅ COMPLETE ARCHITECTURE IMPLEMENTED

### 🎯 System Overview
Multi-agent AI system for combating misinformation with 6 specialized agents:

1. **Root Orchestrator** - Delegates tasks and manages workflow
2. **Content Intake** - Processes all content types (text, image, video, audio)  
3. **Preprocessing & Context** - Analyzes context and extracts claims
4. **Fact Check** - Multi-source verification with credibility scoring (MOST IMPORTANT)
5. **Knowledge** - Educates users about misinformation patterns
6. **Feedback** - Learns from user input with malicious use protection
7. **Realtime Alert** - Monitors unsolved queries and sends alerts

### 📁 Current Structure
```
agents/
├── orchestrator_agent.py              # ✅ Main orchestrator 
├── sub_agents/
│   ├── content_intake_agent.py         # ✅ Multi-format processing
│   ├── preprocessing_context_agent.py  # ✅ Context analysis
│   ├── fact_check_agent.py            # ✅ Multi-source verification
│   ├── knowledge_agent.py             # ✅ Education system
│   ├── feedback_agent.py              # ✅ Learning with security
│   └── realtime_alert_agent.py        # ✅ Alert management
├── tools/tools.py                     # ✅ Utilities
├── .env                               # ✅ Environment config
└── requirements.txt                   # ✅ Dependencies
```

### 🚀 Next Development Phase
- **API Integrations**: NewsAPI, WHO, CDC, fact-checking APIs
- **ML Models**: NLP for claim extraction, image analysis
- **Database**: Persistent storage for queries and feedback
- **UI Development**: Browser extension, WhatsApp bot, web app
- **Real-time Monitoring**: Implement actual source monitoring

### 💡 Development Guidelines
- Each agent is modular and independently testable
- Security-first approach with malicious use protection
- Template-based architecture allows easy customization
- Comprehensive error handling and logging included
- Ready for real API integration when needed
