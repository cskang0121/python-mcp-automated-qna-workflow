# Python MCP Automated Q&A Workflow

> An open source hands-on learning project for Model Context Protocol (MCP). Build two MCP servers that enable Claude Desktop to automatically answer customer questions by searching context in relevant documentation and managing Q&A workflows through Google Sheets setup.

**Repository**: https://github.com/cskang0121/python-mcp-automated-qna-workflow

## 🎯 Project Overview

This is an open-source learning project for understanding **Model Context Protocol (MCP)** - the protocol that enables AI assistants like Claude to interact with external systems and data sources.

### The Business Problem We're Solving

Businesses spend countless hours answering repetitive customer questions on forums and support channels. This project demonstrates how MCP can automate this process by:

1. **Connecting AI to multiple data sources** (Google Sheets + local documentation)
2. **Automating repetitive Q&A** while maintaining human oversight
3. **Creating a scalable support system** that learns from documentation

### How It Works

```
┌─────────────────┐
│  Claude Desktop │  (MCP Client)
│       (AI)      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────────────┐
│Google │ │ Knowledge Base  │
│Sheets │ │   MCP Server    │
│ MCP   │ │                 │
│Server │ │ Serves local    │
│       │ │ documentation   │
└───┬───┘ └──────┬───────────┘
    │            │
┌───▼───────────▼───┐
│   Data Sources    │
├───────────────────┤
│• Google Sheet     │
│  (Q&A Queue)      │
│• Text Documents   │
│  (Product Docs)   │
└───────────────────┘
```
**Workflow:**
1. User questions arrive in Google Sheet
2. AI reads questions via Google Sheets MCP server
3. AI searches documentation via Knowledge Base MCP server
4. AI drafts answers for review
5. Approved answers are posted back to Google Sheet

## 🏗️ Project Structure

```
python-mcp-automated-qna-workflow/
├── google_sheets_mcp/          # Google Sheets integration server
│   ├── src/                    # Server source code
│   ├── pyproject.toml         # Dependencies and configuration
│   └── README.md              # Server-specific documentation
│
├── knowledge_base_mcp/         # Local document server
│   ├── src/                    # Server source code
│   ├── data/                   # Sample documentation included
│   │   ├── products/          # pricing.txt (plans & costs)
│   │   ├── support/           # faq.txt (common questions)
│   │   └── policies/          # refund-policy.txt (terms)
│   ├── pyproject.toml         # Dependencies and configuration
│   └── README.md              # Server-specific documentation
│
├── business_scenarios/         # Sample files and demos
│   ├── sample-workflow.md     # Example Q&A workflow
│   └── sample-questions.csv   # 10 test questions for Google Sheets
│
└── claude_desktop_config.example.json  # Template for Claude Desktop setup
```

## 🛠️ Technology Stack

- **Python 3.11+** - Core programming language
- **uv** - Fast Python package manager
- **MCP SDK** - Protocol implementation
- **Google APIs** - Sheets integration
- **asyncio** - Asynchronous operations

## 📋 Prerequisites

1. **Python 3.11 or higher**
   ```bash
   python --version  # Should show 3.11+
   ```

2. **uv package manager**
   ```bash
   # Install uv (macOS/Linux)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Or with pip
   pip install uv
   ```

3. **Claude Desktop App**
   - Download from [Claude.ai](https://claude.ai/download)
   - Required for MCP client functionality

4. **Google Cloud Account** (for Google Sheets integration)
   - Free tier is sufficient
   - Setup instructions in `google_sheets_mcp/README.md`

## 🚀 Quick Start

### Step 1: Clone the Repository
```bash
git clone https://github.com/cskang0121/python-mcp-automated-qna-workflow.git
cd python-mcp-automated-qna-workflow
```

### Step 2: Set Up Virtual Environment
```bash
# Create virtual environment at project root
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all dependencies
uv pip install mcp aiofiles  # For Knowledge Base server
uv pip install google-api-python-client google-auth python-dotenv  # For Google Sheets
```

### Step 3: Set Up Google Sheets Authentication
```bash
# Create .env file in google_sheets_mcp/
cd google_sheets_mcp
cp .env.example .env
# Edit .env with your Google Sheet ID and credentials path

# Note: Sample questions for your Google Sheet are in business_scenarios/sample-questions.csv
```

### Step 4: Configure Claude Desktop
1. Copy the example config file to Claude Desktop's config location:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Edit the config file and replace `/YOUR/PROJECT/PATH/` with your actual project path

See `claude_desktop_config.example.json` for the template configuration.

### Step 5: Prepare Test Data
```bash
# Sample documentation already exists in knowledge_base_mcp/data/
# Sample questions are available in business_scenarios/sample-questions.csv
# Copy them to your Google Sheet for testing
```

### Step 6: Run the Servers
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Terminal 1: Knowledge Base Server
cd knowledge_base_mcp
python src/server.py

# Terminal 2: Google Sheets Server (in new terminal)
source .venv/bin/activate
cd google_sheets_mcp
python src/server.py
```

## 💡 Usage Examples

### Scenario 1: Questions Answerable from Documentation
1. **Business Owner**: "Claude, check the unanswered questions in the sheet"
2. **Claude**: *Reads questions from Google Sheet via MCP*
3. **Claude**: "I found 5 new questions. Let me search our documentation..."
4. **Claude**: *Searches knowledge base for answers*
5. **Claude**: "I can answer 4 questions from the documentation with high confidence"
6. **Business Owner**: "Show me the answers"
7. **Claude**: *Drafts answers from documentation*
8. **Business Owner**: "Looks good, post them"
9. **Claude**: *Updates Google Sheet with approved answers*

### Scenario 2: Questions Needing Human Input
1. **Claude**: "Question Q004 asks about student discounts, but I don't find specific information"
2. **Business Owner**: "We offer 40% off for students. Post this answer: 'Yes, students get 40% off with valid .edu email'"
3. **Claude**: *Posts the custom answer to the sheet*

See `business_scenarios/sample-workflow.md` for detailed workflow examples.

## 🎓 Learning Objectives

By working with this project, you'll learn:

1. **MCP Fundamentals**
   - How MCP servers expose tools to AI
   - Client-server communication patterns
   - Protocol message structure

2. **Building MCP Servers**
   - Creating custom tools
   - Handling async operations
   - Error handling and validation

3. **Real-World Integration**
   - OAuth2 authentication (Google)
   - API integration patterns
   - File system operations

4. **AI Orchestration**
   - Multi-source data aggregation
   - Human-in-the-loop workflows
   - Confidence-based decision making

## 📚 Documentation

- [MCP Specification](https://modelcontextprotocol.io/docs)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)

## 🤝 Contributing

This is a learning project! Contributions are welcome:
- Add new MCP server examples
- Improve documentation
- Share learning experiences
- Report issues

## 📄 License

MIT License - Use freely for learning and teaching

## 🚧 Project Status

**Current Phase**: MCP Servers Implemented ✅

- [x] Project structure defined
- [x] Documentation created
- [x] Knowledge Base MCP server implementation
- [x] Google Sheets MCP server implementation
- [ ] Claude Desktop integration
- [ ] Example workflows tested
- [ ] Google Sheets authentication setup

## 🎯 Common Challenges & Solutions

When working through this project, here are key points that will save you time:

### Virtual Environment Setup
- **Important**: Create the virtual environment at the project root, not in individual server directories
- Always activate the environment before running servers: `source .venv/bin/activate`
- If you see "command not found: python", use `python3` instead

### Claude Desktop Configuration
- **The config file doesn't exist by default** - use `claude_desktop_config.example.json` as a template
- **Config location varies by OS**:
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
  - Linux: `~/.config/Claude/claude_desktop_config.json`
- **Must use absolute paths** in the config, not relative paths
- **Completely restart Claude Desktop** after changing the config (Cmd+Q, not just closing the window)
- **Start a new conversation** to test MCP servers - old conversations won't see them

### Google Sheets Setup Tips
- **Service Account Email**: Find it in your `google-credentials.json` file under `"client_email"`
- **Sheet ID**: It's the long string in the URL between `/d/` and `/edit` 
  - Example: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
- **Critical Step**: You MUST share your Google Sheet with the service account email (like sharing with a person)
- **Uncheck "Notify people"** when sharing - service accounts don't have email

### Testing Your Setup
- **Test without Claude first**: Run the test scripts to verify connections work
- **If MCP servers don't appear in Claude**:
  1. Check you fully restarted Claude Desktop
  2. Verify you're in a NEW conversation
  3. Confirm paths in config are absolute and correct
  4. Try asking "What MCP tools do you have access to?"

### Python Environment Issues
- **uv not found**: Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Module not found errors**: Make sure you activated the virtual environment
- **Permission denied**: The paths in Claude config might be wrong

### Debugging MCP Servers
- Servers run silently - no output means they're working
- To see debug output: `MCP_DEBUG=true python src/server.py`
- Check if server imports work: `python -c "from src.server import server"`

## 💬 Support

- Open an issue for questions
- Share your learning experience
- Suggest improvements

---

**Remember**: This is a learning project designed to teach MCP concepts through practical implementation. Start simple, experiment, and build your understanding step by step!