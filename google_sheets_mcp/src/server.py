#!/usr/bin/env python3
"""
Simple Google Sheets MCP Server
Handles Q&A operations on a Google Sheet
"""

import os
import asyncio
from typing import Any
import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize server
server = Server("google-sheets")

# Google Sheets setup
SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "./google-credentials.json")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")
RANGE_NAME = f"{SHEET_NAME}!A:F"

# Initialize Google Sheets client
service = None
if os.path.exists(CREDENTIALS_PATH):
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=credentials)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="list_questions",
            description="Get all unanswered questions from the sheet",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="get_question",
            description="Get a specific question by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "question_id": {
                        "type": "string",
                        "description": "The question ID (e.g., 'Q001')",
                    }
                },
                "required": ["question_id"],
            },
        ),
        types.Tool(
            name="post_answer",
            description="Post an answer for a specific question",
            inputSchema={
                "type": "object",
                "properties": {
                    "question_id": {
                        "type": "string",
                        "description": "The question ID",
                    },
                    "answer": {
                        "type": "string",
                        "description": "The answer text",
                    }
                },
                "required": ["question_id", "answer"],
            },
        ),
        types.Tool(
            name="update_status",
            description="Update the status of a question",
            inputSchema={
                "type": "object",
                "properties": {
                    "question_id": {
                        "type": "string",
                        "description": "The question ID",
                    },
                    "status": {
                        "type": "string",
                        "description": "New status (unanswered/answered/reviewed)",
                        "enum": ["unanswered", "answered", "reviewed"]
                    }
                },
                "required": ["question_id", "status"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool calls"""
    
    if not service:
        return [types.TextContent(
            type="text",
            text="Error: Google Sheets not configured. Check credentials and environment variables."
        )]
    
    if not SHEETS_ID:
        return [types.TextContent(
            type="text",
            text="Error: GOOGLE_SHEETS_ID not set in environment"
        )]
    
    sheet = service.spreadsheets()
    
    try:
        if name == "list_questions":
            result = sheet.values().get(spreadsheetId=SHEETS_ID, range=RANGE_NAME).execute()
            rows = result.get('values', [])
            
            if not rows:
                return [types.TextContent(type="text", text="No questions found in sheet")]
            
            # Filter for unanswered questions (Status column is C, index 2)
            unanswered = []
            for i, row in enumerate(rows[1:], start=2):  # Skip header
                if len(row) > 2 and row[2].lower() == 'unanswered':
                    unanswered.append({
                        'row': i,
                        'id': row[0] if len(row) > 0 else '',
                        'question': row[1] if len(row) > 1 else '',
                    })
            
            if not unanswered:
                return [types.TextContent(type="text", text="No unanswered questions")]
            
            text = f"Found {len(unanswered)} unanswered questions:\n"
            for q in unanswered:
                text += f"\n{q['id']}: {q['question']}"
            
            return [types.TextContent(type="text", text=text)]
        
        elif name == "get_question":
            if not arguments or "question_id" not in arguments:
                return [types.TextContent(type="text", text="Error: question_id required")]
            
            result = sheet.values().get(spreadsheetId=SHEETS_ID, range=RANGE_NAME).execute()
            rows = result.get('values', [])
            
            for i, row in enumerate(rows[1:], start=2):
                if len(row) > 0 and row[0] == arguments["question_id"]:
                    return [types.TextContent(
                        type="text",
                        text=f"Question {row[0]}:\n{row[1] if len(row) > 1 else ''}\nStatus: {row[2] if len(row) > 2 else 'unknown'}"
                    )]
            
            return [types.TextContent(type="text", text=f"Question {arguments['question_id']} not found")]
        
        elif name == "post_answer":
            if not arguments or "question_id" not in arguments or "answer" not in arguments:
                return [types.TextContent(type="text", text="Error: question_id and answer required")]
            
            # Find the row with this question ID
            result = sheet.values().get(spreadsheetId=SHEETS_ID, range=RANGE_NAME).execute()
            rows = result.get('values', [])
            
            for i, row in enumerate(rows[1:], start=2):
                if len(row) > 0 and row[0] == arguments["question_id"]:
                    # Update answer (column D) and status (column C)
                    from datetime import datetime
                    updates = [
                        ['answered', arguments["answer"], datetime.now().isoformat(), 'AI']
                    ]
                    
                    sheet.values().update(
                        spreadsheetId=SHEETS_ID,
                        range=f"{SHEET_NAME}!C{i}:F{i}",
                        valueInputOption="RAW",
                        body={"values": updates}
                    ).execute()
                    
                    return [types.TextContent(
                        type="text",
                        text=f"Answer posted for question {arguments['question_id']}"
                    )]
            
            return [types.TextContent(type="text", text=f"Question {arguments['question_id']} not found")]
        
        elif name == "update_status":
            if not arguments or "question_id" not in arguments or "status" not in arguments:
                return [types.TextContent(type="text", text="Error: question_id and status required")]
            
            result = sheet.values().get(spreadsheetId=SHEETS_ID, range=RANGE_NAME).execute()
            rows = result.get('values', [])
            
            for i, row in enumerate(rows[1:], start=2):
                if len(row) > 0 and row[0] == arguments["question_id"]:
                    sheet.values().update(
                        spreadsheetId=SHEETS_ID,
                        range=f"{SHEET_NAME}!C{i}",
                        valueInputOption="RAW",
                        body={"values": [[arguments["status"]]]}
                    ).execute()
                    
                    return [types.TextContent(
                        type="text",
                        text=f"Status updated to '{arguments['status']}' for question {arguments['question_id']}"
                    )]
            
            return [types.TextContent(type="text", text=f"Question {arguments['question_id']} not found")]
        
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    """Run the server"""
    # Print startup message
    print("Google Sheets MCP Server starting...", flush=True)
    
    # Check configuration
    if not SHEETS_ID:
        print("WARNING: GOOGLE_SHEETS_ID not set in environment", flush=True)
    else:
        print(f"Sheet ID: {SHEETS_ID[:10]}...{SHEETS_ID[-10:]}", flush=True)
    
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"ERROR: Credentials file not found at {CREDENTIALS_PATH}", flush=True)
        print("Please follow the setup instructions in COMPLETE_GOOGLE_SETUP.md", flush=True)
    elif service:
        print("Google credentials loaded successfully", flush=True)
        print("Server running successfully. Ready to process Q&A from Google Sheets.\n", flush=True)
    else:
        print("WARNING: Google service not initialized properly", flush=True)
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="google-sheets",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())