# Testing Guide

This guide shows how to test and run the MCP servers.

## Prerequisites

Make sure you've completed:
- ✅ Virtual environment setup
- ✅ Dependencies installed
- ✅ Google Sheets API configured (for Google Sheets server)

## Testing Knowledge Base Server

### 1. Quick Test
```bash
# From project root
source .venv/bin/activate
cd knowledge_base_mcp
python test_server.py
```

Expected output:
```
✅ MCP SDK is installed
✅ Server module imports successfully
📄 Found 3 text files
```

### 2. Run the Server
```bash
# Still in knowledge_base_mcp directory
python src/server.py
```

The server will start and wait for MCP connections. You'll see no output initially - this is normal.

### 3. Test with Claude Desktop
1. Configure Claude Desktop (see claude-config/config.json)
2. Start a new conversation in Claude
3. Ask: "List all available documents"
4. Claude should be able to see your knowledge base files

## Testing Google Sheets Server

### 1. Verify Google Setup
```bash
# From project root
source .venv/bin/activate
cd google_sheets_mcp

# Make sure credentials exist
ls google-credentials.json

# Check .env is configured
cat .env
```

### 2. Test Connection
```bash
# Create and run test script
python << 'EOF'
import os
from dotenv import load_dotenv
load_dotenv()

print(f"Sheet ID: {os.getenv('GOOGLE_SHEETS_ID')}")
print(f"Credentials: {os.getenv('GOOGLE_CREDENTIALS_PATH')}")

if os.path.exists(os.getenv('GOOGLE_CREDENTIALS_PATH', '')):
    print("✅ Credentials file found")
else:
    print("❌ Credentials file not found")
EOF
```

### 3. Run the Server
```bash
python src/server.py
```

## Running Both Servers Together

### Terminal 1 - Knowledge Base Server
```bash
cd /path/to/python-model-context-protocol
source .venv/bin/activate
cd knowledge_base_mcp
python src/server.py
```

### Terminal 2 - Google Sheets Server
```bash
cd /path/to/python-model-context-protocol
source .venv/bin/activate
cd google_sheets_mcp
python src/server.py
```

## Configuring Claude Desktop

1. Find your Claude Desktop config:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Update it with absolute paths:
```json
{
  "mcpServers": {
    "knowledge-base": {
      "command": "/path/to/python-model-context-protocol/.venv/bin/python",
      "args": [
        "/path/to/python-model-context-protocol/knowledge_base_mcp/src/server.py"
      ]
    },
    "google-sheets": {
      "command": "/path/to/python-model-context-protocol/.venv/bin/python",
      "args": [
        "/path/to/python-model-context-protocol/google_sheets_mcp/src/server.py"
      ],
      "env": {
        "GOOGLE_SHEETS_ID": "your-sheet-id",
        "GOOGLE_CREDENTIALS_PATH": "/path/to/google_sheets_mcp/google-credentials.json"
      }
    }
  }
}
```

3. Restart Claude Desktop

## Testing in Claude

### Test Knowledge Base Server
Ask Claude:
- "What MCP tools are available?"
- "List all documents in the knowledge base"
- "What's in the pricing document?"
- "Search for 'refund' in all documents"

### Test Google Sheets Server
Ask Claude:
- "List all unanswered questions from the Google Sheet"
- "Get question Q001"
- "Post an answer for question Q001: The Professional plan costs $99/month"
- "Update the status of Q001 to 'answered'"

## Troubleshooting

### Server won't start
- Check you're in the virtual environment: `which python` should show `.venv/bin/python`
- Verify imports: `python -c "import mcp"`

### Claude can't see the servers
- Check Claude Desktop is fully restarted
- Verify paths in config are absolute, not relative
- Check server is actually running (no error messages)

### Google Sheets errors
- Verify Sheet ID is correct (just the ID, not full URL)
- Check service account has Editor access to the sheet
- Ensure credentials file path is correct

## Debug Mode

To see more detailed output from servers:
```bash
MCP_DEBUG=true python src/server.py
```

This will show all MCP protocol messages.