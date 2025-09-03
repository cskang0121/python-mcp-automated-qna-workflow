# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python MCP (Model Context Protocol) learning project that demonstrates building MCP servers for automated Q&A systems. It consists of two MCP servers:
1. **Google Sheets MCP**: Handles CRUD operations on Google Sheets
2. **Knowledge Base MCP**: Serves local text documentation

## Development Commands

### Environment Setup
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment at project root
uv venv
source .venv/bin/activate

# Install all dependencies
uv pip install mcp aiofiles google-api-python-client google-auth python-dotenv
```

### Running Servers
```bash
# Always activate virtual environment first
source .venv/bin/activate

# Run Knowledge Base server
cd knowledge_base_mcp
python src/server.py

# Run Google Sheets server (in separate terminal)
source .venv/bin/activate
cd google_sheets_mcp
python src/server.py
```

### Testing
```bash
# Test Knowledge Base server setup
cd knowledge_base_mcp
python test_server.py

# The servers are simple enough that manual testing is sufficient
# Use Claude Desktop to test the actual MCP communication
```

## Code Architecture

### MCP Server Structure
Each MCP server is kept simple:
```
server-name-mcp/
├── src/
│   └── server.py       # Single file containing the MCP server
├── data/               # (Knowledge Base only) Text documents
├── pyproject.toml      # Dependencies and package config
└── .env.example        # (Google Sheets only) Environment template
```

### Key MCP Concepts
- **Tools**: Functions exposed to Claude (e.g., `list_questions`, `search_documents`)
- **Resources**: Data sources the server provides access to
- **Async Operations**: All MCP operations use Python's asyncio

### Google Sheets Server Architecture
- Uses Google API Python client library
- Implements OAuth2 authentication flow
- Tools: `list_questions`, `get_question`, `post_answer`, `update_status`
- Handles Google Sheets as a Q&A queue

### Knowledge Base Server Architecture  
- Reads `.txt` files from `data/` directory
- Organizes documents by category (products, support, policies)
- Tools: `list_documents`, `read_document`, `search_documents`
- Implements async file operations with `aiofiles`

## Implementation Guidelines

### When Adding New Tools
1. Define tool in `server.py` using MCP's `@server.tool()` decorator
2. Implement business logic as async function
3. Add appropriate error handling
4. Update server README with tool documentation

### Error Handling Pattern
```python
try:
    result = await operation()
    return {"status": "success", "data": result}
except Exception as e:
    return {"status": "error", "message": str(e)}
```

### Testing Approach
- Unit tests for individual tool functions
- Integration tests for MCP server communication
- Mock external dependencies (Google API, file system)

## Common Tasks

### Adding a New Document Category
1. Create new subdirectory in `knowledge_base_mcp/data/`
2. Add `.txt` files to the directory
3. No code changes needed - server auto-discovers

### Configuring Google Sheets Access
1. Create service account in Google Cloud Console
2. Download JSON credentials
3. Share target sheet with service account email
4. Set environment variables in `.env` file

### Debugging MCP Servers
```bash
# Run with verbose logging
MCP_DEBUG=true python src/server.py

# Test individual tools
python -c "import asyncio; from src.server import tool_name; asyncio.run(tool_name())"
```

## Important Notes

- MCP servers communicate via JSON-RPC over stdio
- Claude Desktop manages server lifecycle
- Servers should be stateless between tool calls
- Use environment variables for configuration, not hardcoded values
- Keep tool responses under 50KB for optimal performance

## File Paths

All paths in this project are relative to the repository root:
- `/google_sheets_mcp/` - Google Sheets server
- `/knowledge_base_mcp/` - Documentation server
- `/business_scenarios/` - Sample data and workflows