# Google Sheets MCP Server

This MCP server provides integration with Google Sheets, allowing Claude to read questions and write answers to a spreadsheet.

## Features

- **Read Questions**: Fetch unanswered questions from Google Sheets
- **Write Answers**: Post AI-generated answers back to the sheet
- **Update Status**: Mark questions as answered/reviewed
- **Batch Operations**: Process multiple Q&A items efficiently

## Setup

### 1. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sheets API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### 2. Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in service account details
4. Grant role: "Editor" or custom role with Sheets access
5. Create and download JSON key file
6. Save as `google-credentials.json` in this directory

### 3. Environment Setup

Create `.env` file:
```env
GOOGLE_SHEETS_ID=your-sheet-id-here
GOOGLE_CREDENTIALS_PATH=./google-credentials.json
```

### 4. Install Dependencies

```bash
cd google_sheets_mcp
uv venv
uv pip install -e .
```

## Google Sheet Structure

Your Google Sheet should have these columns:
- **A**: Question ID
- **B**: Question Text
- **C**: Status (unanswered/answered/reviewed)
- **D**: Answer
- **E**: Timestamp
- **F**: Answered By

## Running the Server

```bash
python src/server.py
```

The server will start on the default MCP port and be ready for Claude Desktop connection.

## Available Tools

### `list_questions`
Fetches all unanswered questions from the sheet.

### `get_question`
Retrieves a specific question by ID.

### `post_answer`
Writes an answer to the sheet for a specific question.

### `update_status`
Updates the status of a question (unanswered/answered/reviewed).

## Testing

```bash
uv pip install -e ".[dev]"
pytest tests/
```