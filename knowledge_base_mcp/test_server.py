#!/usr/bin/env python3
"""
Simple test script for the Knowledge Base MCP server
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path

# Check if data directory exists and has files
DATA_DIR = Path(__file__).parent / "data"

print("🔍 Checking Knowledge Base MCP Server Setup...")
print(f"📁 Data directory: {DATA_DIR}")

if not DATA_DIR.exists():
    print("❌ Data directory doesn't exist!")
    sys.exit(1)

# List all text files
txt_files = list(DATA_DIR.rglob("*.txt"))
print(f"\n📄 Found {len(txt_files)} text files:")
for f in txt_files:
    print(f"  - {f.relative_to(DATA_DIR)}")

# Check if mcp is installed
try:
    import mcp
    print("\n✅ MCP SDK is installed")
except ImportError:
    print("\n❌ MCP SDK not installed. Run: uv pip install mcp")
    sys.exit(1)

# Try importing our server
try:
    from src import server
    print("✅ Server module imports successfully")
except ImportError as e:
    print(f"❌ Failed to import server: {e}")
    sys.exit(1)

print("\n✨ Knowledge Base server is ready to run!")
print("\nTo start the server, run:")
print("  python src/server.py")