# V2 Multi-Agent Misinformation Detection System

## 🏗️ Architecture Overview

We've successfully created a 2-agent system following ADK multi-agent structure:

### 🎯 Agent Hierarchy
```
Root Agent (misinformation_detector)
├── Content Intake Agent
└── Preprocessing & Context Agent
```

### 📁 Directory Structure
```
agents/
├── .env                                    # Environment variables (GOOGLE_API_KEY)
├── agent.py                               # Root agent definition
├── __init__.py                            # Root package init
├── README.md                              # Documentation
├── test_structure.py                      # Structure validation
└── sub_agents/
    ├── __init__.py                        # Sub-agents package init
    ├── content_intake/
    │   ├── __init__.py                    # Agent package init
    │   └── agent.py                       # Content intake agent definition
    └── preprocessing_context/
        ├── __init__.py                    # Agent package init  
        └── agent.py                       # Preprocessing agent definition
```

## 🤖 Agent Specifications

### 1. Root Agent (`misinformation_detector`)
- **Role**: Main coordinator and orchestrator
- **Model**: gemini-2.0-flash
- **Function**: Delegates tasks to sub-agents in sequence and synthesizes results
- **Workflow**: Content Intake → Preprocessing & Context → Final Assessment

### 2. Content Intake Agent (`content_intake`)
- **Role**: Processes raw content into structured format
- **Capabilities**: 
  - Text processing and claim extraction
  - Image OCR and visual analysis
  - Audio transcription
  - Video frame extraction
  - Multi-format content handling
- **Output**: Structured content with metadata and extracted information

### 3. Preprocessing & Context Agent (`preprocessing_context`)
- **Role**: Summarizes and analyzes content context
- **Capabilities**:
  - Content summarization
  - Claim extraction and classification
  - Context analysis (audience, purpose, tone)
  - Content quality assessment
  - Red flag identification
- **Output**: Executive summary, key claims, context assessment, risk indicators

## 🚀 How to Use

### Starting the System
1. Navigate to the parent directory: `cd mumbaihacks`
2. Start ADK web server: `adk web`
3. Open browser to `http://127.0.0.1:8000`
4. Select "agents" from the dropdown

### Test Prompts
Try these prompts to test the multi-agent workflow:

1. **Text Analysis**:
   ```
   Analyze this text for misinformation: "BREAKING: Scientists discovered a shocking secret that big pharma doesn't want you to know! This miracle cure will change everything!"
   ```

2. **Content Processing**:
   ```
   Process this content and provide a summary with context analysis: "New study shows 90% improvement in health with this one simple trick that doctors hate."
   ```

3. **Workflow Test**:
   ```
   I have some content that needs to be analyzed for misinformation. Can you walk me through your process?
   ```

## 🔄 Agent Workflow

1. **User submits content** → Root Agent
2. **Root Agent** → Delegates to Content Intake Agent
3. **Content Intake** → Processes and structures the content
4. **Root Agent** → Delegates structured content to Preprocessing Agent  
5. **Preprocessing Agent** → Summarizes and analyzes context
6. **Root Agent** → Synthesizes results and provides final assessment

## ✅ Current Status

- ✅ ADK-compliant directory structure
- ✅ Root agent with proper sub-agent delegation
- ✅ Content intake agent with multi-format processing capabilities
- ✅ Preprocessing & context agent with summarization and analysis
- ✅ Proper Python package structure with `__init__.py` files
- ✅ Environment configuration (.env file)
- ✅ Ready for ADK web interface

## 🔮 Next Steps

Ready for additional agents:
- **Fact Check Agent**: Real API integrations for verification
- **Knowledge Agent**: Educational content about misinformation
- **Alert Agent**: Real-time monitoring and notifications
- **Feedback Agent**: Learning from user interactions

The foundation is solid and extensible for adding more specialized agents!
