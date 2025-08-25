# Misinformation Detection System

An advanced AI-powered system for detecting and analyzing misinformation across multiple content types using Google ADK and LLM technology.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Google API Key for Gemini

### Setup
1. **Clone and Navigate**:
   ```bash
   git clone <repository-url>
   cd mumbaihacks
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**:
   ```bash
   cd agents
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   - Add your Google API key to `agents/.env`:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

### Running the System

#### Option 1: ADK CLI (Recommended)
```bash
cd agents
adk run root_orchestrator
```

#### Option 2: ADK Web Interface
```bash
cd agents
adk web
# Visit http://127.0.0.1:8000
```

#### Option 3: Direct Python (Development)
```bash
cd agents
python -c "from root_orchestrator.agent import orchestrator; print(orchestrator.process_content('Your content here', 'text'))"
```

## 🏗️ Architecture

### Root Orchestrator Agent
- **LLM-Powered**: Uses Google Gemini for intelligent responses
- **6-Phase Analysis Pipeline**: 
  1. Content Intake → 2. Preprocessing → 3. Fact Check → 4. Knowledge → 5. Feedback → 6. Alerts
- **ADK Compatible**: Full Google ADK integration

### Sub-Agents (6 Specialized Agents)
1. **Content Intake** (`content_intake/`) - Processes text, media, URLs
2. **Preprocessing Context** (`preprocessing_context/`) - Analyzes and summarizes content  
3. **Fact Check** (`fact_check/`) - Cross-references against reliable sources
4. **Knowledge** (`knowledge/`) - Provides educational content about misinformation
5. **Feedback** (`feedback/`) - Learns from user input and improves accuracy
6. **Realtime Alert** (`realtime_alert/`) - Handles urgent misinformation alerts

## 📁 Project Structure

```
mumbaihacks/
├── agents/                          # Main agents directory
│   ├── .env                        # Environment variables (Google API key)
│   ├── requirements.txt            # Python dependencies
│   ├── README.md                   # Agents documentation
│   ├── root_orchestrator/          # Main LLM agent
│   │   └── agent.py               # Orchestrator implementation
│   ├── content_intake/             # Content processing agent
│   │   ├── agent.py
│   │   └── tools/
│   ├── preprocessing_context/      # Context analysis agent
│   │   ├── agent.py
│   │   └── tools/
│   ├── fact_check/                # Fact-checking agent
│   │   ├── agent.py
│   │   └── tools/
│   ├── knowledge/                 # Educational content agent
│   │   ├── agent.py
│   │   └── tools/
│   ├── feedback/                  # User feedback agent
│   │   ├── agent.py
│   │   └── tools/
│   └── realtime_alert/           # Alert system agent
│       ├── agent.py
│       └── tools/
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🎯 Example Usage

### CLI Example:
```
[user]: fact check did modi say ban veda
[misinformation_orchestrator]: There's no reliable evidence to support the claim that Narendra Modi ever called for a ban on the Vedas. This statement appears to be false and likely constitutes misinformation.

My analysis follows these steps:
1. Content Intake and Processing
2. Context Analysis and Preprocessing  
3. Fact Checking Against Reliable Sources
4. Educational Content Generation
5. Feedback Processing
6. Real-time Alert Assessment

Conclusion: The claim is FALSE - no credible evidence supports this assertion.
```

## 🔧 Development

### Adding New Features
1. **Sub-Agent Enhancement**: Implement actual functionality in individual agent `tools/` folders
2. **New Content Types**: Add support for images, videos, audio in content_intake
3. **Database Integration**: Add persistent storage for results and learning
4. **Advanced Analytics**: Implement pattern detection and trend analysis

### Testing
```bash
cd agents
python -c "from root_orchestrator.agent import orchestrator; result = orchestrator.process_content('Test content', 'text'); print(result['status'])"
```

## 📋 Features

- ✅ **LLM-Powered Analysis**: Google Gemini integration
- ✅ **Multi-Agent Architecture**: 6 specialized sub-agents
- ✅ **ADK Integration**: Full Google ADK support
- ✅ **Interactive Interface**: CLI and Web options
- ✅ **Comprehensive Analysis**: 6-phase processing pipeline
- ✅ **Educational Content**: Helps users understand misinformation patterns
- 🔄 **Extensible Design**: Easy to add new content types and features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes in the appropriate agent folders
4. Test with `adk run root_orchestrator`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
