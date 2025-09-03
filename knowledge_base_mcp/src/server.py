#!/usr/bin/env python3
"""
Simple Knowledge Base MCP Server
Serves text documents from the data/ directory
"""

import os
import asyncio
from pathlib import Path
from typing import Any
import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# Initialize server
server = Server("knowledge-base")
DATA_DIR = Path(__file__).parent.parent / "data"

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="list_documents",
            description="List all available documents organized by category",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="read_document",
            description="Read the full content of a specific document",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Document path relative to data directory (e.g., 'products/pricing.txt')",
                    }
                },
                "required": ["path"],
            },
        ),
        types.Tool(
            name="search_documents",
            description="Search across all documents for keywords",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term or phrase",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10,
                    }
                },
                "required": ["query"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls"""
    
    if name == "list_documents":
        documents = {}
        for category_dir in DATA_DIR.iterdir():
            if category_dir.is_dir():
                docs = [f.name for f in category_dir.glob("*.txt")]
                if docs:
                    documents[category_dir.name] = docs
        
        return [types.TextContent(
            type="text",
            text=f"Available documents:\n{documents}"
        )]
    
    elif name == "read_document":
        if not arguments or "path" not in arguments:
            return [types.TextContent(
                type="text",
                text="Error: 'path' parameter is required"
            )]
        
        file_path = DATA_DIR / arguments["path"]
        if not file_path.exists():
            return [types.TextContent(
                type="text",
                text=f"Error: Document '{arguments['path']}' not found"
            )]
        
        try:
            content = file_path.read_text()
            return [types.TextContent(
                type="text",
                text=content
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error reading document: {str(e)}"
            )]
    
    elif name == "search_documents":
        if not arguments or "query" not in arguments:
            return [types.TextContent(
                type="text",
                text="Error: 'query' parameter is required"
            )]
        
        query = arguments["query"].lower()
        max_results = arguments.get("max_results", 10)
        results = []
        
        for txt_file in DATA_DIR.rglob("*.txt"):
            try:
                content = txt_file.read_text()
                if query in content.lower():
                    # Find the line containing the query
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if query in line.lower():
                            context = lines[max(0, i-1):min(len(lines), i+2)]
                            results.append({
                                "file": str(txt_file.relative_to(DATA_DIR)),
                                "excerpt": '\n'.join(context)
                            })
                            if len(results) >= max_results:
                                break
                    if len(results) >= max_results:
                        break
            except Exception:
                continue
        
        if not results:
            return [types.TextContent(
                type="text",
                text=f"No results found for '{arguments['query']}'"
            )]
        
        result_text = f"Found {len(results)} results for '{arguments['query']}':\n\n"
        for r in results:
            result_text += f"📄 {r['file']}:\n{r['excerpt']}\n\n"
        
        return [types.TextContent(
            type="text",
            text=result_text
        )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Run the server"""
    # Print startup message
    print("Knowledge Base MCP Server starting...", flush=True)
    print(f"Document directory: {DATA_DIR}", flush=True)
    
    # Count available documents
    doc_count = sum(1 for _ in DATA_DIR.rglob("*.txt"))
    print(f"Documents loaded: {doc_count}", flush=True)
    print("Server running successfully. Waiting for MCP connections...\n", flush=True)
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="knowledge-base",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())