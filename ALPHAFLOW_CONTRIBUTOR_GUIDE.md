# 🚀 Jujutsu-Quants - Cursed-Tech AI for Markets

Welcome to **Jujutsu-Quants** — an anime-themed AI lab where specialized agents (sorcerers) exorcise noisy markets and cursed news flows. 🎯

## 🌟 What is Jujutsu-Quants?

Jujutsu-Quants is a modular AI platform that combines:
- **Real-time Market Analysis** 📊
- **Advanced News Sentiment Processing** 🧠
- **Intelligent Anomaly Detection** 🔍
- **Vector Search & RAG Technology** 🔎
- **Multi-Agent AI Orchestration** 🤖

## 🚀 Quick Start with UV

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend)
- Git

### Lightning-Fast Setup (uv-only)
```bash
# Clone the repository
git clone https://github.com/your-org/alphaflow.git
cd alphaflow

# Install uv (the fastest Python package manager)
pip install uv

# Create virtual environment and install dependencies with uv
uv venv
# Windows PowerShell
. .\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (optional for development)
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🏗️ Jujutsu-Quants Architecture

### Core Components

```
jujutsu-quants/
├── app/
│   ├── adk/                    # Agent Development Kit
│   │   ├── agents/            # AI Agents (Sentiment, Anomaly, Bias, etc.)
│   │   ├── orchestrator.py    # Multi-Agent Workflow Coordinator
│   │   └── main.py           # FastAPI Application
│   ├── config/               # Configuration & Security
│   ├── database/             # Database Models & CRUD
│   ├── services/             # External Service Integrations
│   └── tools/                # Utility Tools
├── frontend/                 # React Frontend
├── data_collection/          # Data Ingestion & Processing
└── deployment/               # Cloud Deployment Configs
```

### AI Agent Ecosystem (Python-based)
- **Sentiment Agent**: Advanced financial sentiment analysis
- **Anomaly Detector**: Market anomaly identification
- **Bias Detector**: News bias detection and analysis
- **Diversity Analyzer**: Source diversity assessment
- **Breaking News Alert**: Real-time news monitoring
- **QA Agent**: Intelligent question answering

All agents are plain Python modules for portability and easy contribution. You can optionally plug in frameworks:

- LangChain (tooling, routing, retrievers)
- LlamaIndex (indexing, RAG graphs)
- Google ADK (agent runtime; set `ADK_MODE=1`)

Keep PRs focused and dependency-light by default; place optional integrations behind flags.

## 🎯 Current Open Issues (with Levels & Points)

### 🚨 Critical Issues (Fix First!)

#### Mission: Unmask the Cursed Bias (Easy • 2 pts)
[Open brief](./ALPHAFLOW_ISSUE_1.md)
- Small change: accept `entities` param or use config; fallback to title tokens
- Scope: 30–45 mins

#### Mission: Interrogate the Whispering Scrolls (Easy/Medium • 2–4 pts)
[Open brief](./ALPHAFLOW_ISSUE_2.md)
- Implement tiny helper methods with given I/O; return top excerpts + sources
- Scope: ~1–2 hours

### 🔧 Enhancement Issues

#### Mission: Weigh the Cursed Mood (Easy • 2 pts)
[Open brief](./ALPHAFLOW_ISSUE_3.md)
- Add a new method that returns label + heuristic confidence + reason
- Scope: 20–30 mins

#### Mission: Harmonize the Sorcerers (Medium • 4 pts)
[Open brief](./ALPHAFLOW_ISSUE_4.md)
- Standardize outputs and add basic try/except around each agent in orchestrator
- Scope: 1–2 hours

### 🧠 Agents: Medium & Hard

#### Mission: Rank the Spirit Fragments (Medium • 4 pts)
[Open brief](./ALPHAFLOW_ISSUE_5.md)
- Implement BM25+ (or cosine on mini-embeddings) passage ranking over article chunks; return top-3 cited spans
- Scope: 3–4 hours

#### Mission: Forge the Domain Expansion (Hard • 8 pts)
[Open brief](./ALPHAFLOW_ISSUE_6.md)
- Build a summarizer agent that fuses: price movements, ranked passages, and bias flags; produce structured JSON with rationale and uncertainty
- Scope: 1–2 days

## 🧪 Development Workflow

### 1. Choose an Issue
- Look for issues labeled `good first issue` if you're new
- Comment on the issue to claim it
- Ask questions if anything is unclear

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Development
- Follow the existing code style
- Write tests for new functionality
- Update documentation as needed

### 4. Testing
```bash
# Run backend tests
python -m pytest tests/

# Run frontend tests
cd frontend && npm test

# Run linting
python -m flake8 app/
cd frontend && npm run lint
```

### 5. Submit PR
- Push your branch: `git push origin your-branch-name`
- Create a Pull Request with:
  - Clear description of changes
  - Reference to the issue
  - Screenshots if UI changes
  - Test results

## 📝 Code Style Guidelines

### Python
- Follow PEP 8
- Use type hints where possible
- Docstrings for all public methods
- Maximum line length: 88 characters

### JavaScript/React
- Use Prettier for formatting
- Follow React best practices
- Use functional components with hooks
- ESLint configuration enforced

### Agent Development
- Keep agents focused and single-purpose
- Use descriptive method names
- Include error handling
- Follow the established configuration pattern

Optional frameworks (when justified):
- LangChain retrievers or tools inside agents
- LlamaIndex for document stores and RAG graphs
- Google ADK for streaming agent execution (enable with `ADK_MODE=1`)

## 🔧 Configuration

### Environment Variables
```bash
# Optional API keys for enhanced functionality
ALPHA_VANTAGE_API_KEY=your_key_here
FMP_API_KEY=your_key_here
PROJECT_ID=your_gcp_project
REGION=us-central1
ADK_MODE=0  # Set to 1 for Google ADK mode

# Required for database operations
DB_PASSWORD=your_secure_password
DB_USER=postgres
```

### Agent Configuration
Add new agents to `app/config/adk_config.py`:

```python
AGENT_CONFIGS = {
    "your_agent": {
        "name": "your_agent",
        "description": "Brief description of what it does",
        "model": "gemini-2.0-flash",
        "temperature": 0.2,
    },
}
```

## 🚀 Running Jujutsu-Quants (uv-only)

### Backend
```bash
# Ensure venv is active, then run dev server
uv venv  # safe if already created
# Windows PowerShell
. .\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

uv pip install -r requirements.txt

uvicorn app.adk.main:app --host 0.0.0.0 --port 8000 --reload

# Access API docs at http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm start
# Access at http://localhost:3000
```

### Full Stack
```bash
# Terminal 1: Backend
uvicorn app.adk.main:app --reload

# Terminal 2: Frontend  
cd frontend && npm start
```

## 📚 API Usage Examples

### Simple Report
```bash
curl "http://localhost:8000/api/v2/report/simple?symbols=AAPL,TSLA&urls=https://example.com/news"
```

### JSON Report
```bash
curl -X POST "http://localhost:8000/api/v2/report" \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": ["AAPL", "TSLA"],
    "news_urls": ["https://example.com/news"],
    "question": "Any notable market movements?"
  }'
```

## 🐛 Debugging

### Common Issues

1. **Import Errors**: Ensure you're in the correct virtual environment
2. **API Key Issues**: Check environment variables are set correctly
3. **Port Conflicts**: Change ports in uvicorn command if 8000 is occupied
4. **Frontend Build Issues**: Clear node_modules and reinstall

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn app.adk.main:app --reload --log-level debug
```

## 🤝 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Discord**: [Join our AlphaFlow community](https://discord.gg/alphaflow)
- **Email**: contributors@alphaflow.ai

## 📋 Contribution Checklist

Before submitting a PR:

- [ ] Code follows style guidelines
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] No linting errors
- [ ] Issue is referenced in PR description
- [ ] Screenshots included for UI changes

## 🏆 Recognition

AlphaFlow contributors will be:
- Listed in our README
- Mentioned in release notes
- Invited to our contributor Discord
- Eligible for swag and recognition
- Featured in our contributor spotlight

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to exorcise cursed markets? Join the Jujutsu-Quants! 🧿🚀**

Questions? Don't hesitate to reach out. We're here to help you succeed!
