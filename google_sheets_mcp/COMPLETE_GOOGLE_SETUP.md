# Complete Google Sheets Setup Guide - From Zero to Working

This guide assumes you're starting from scratch, including creating a Google account.

## Part 1: Google Account Setup

### Step 1: Create a Google Account (Skip if you have one)

1. Open your browser and go to: https://accounts.google.com/signup
2. Fill in the form:
   - First name and Last name
   - Choose a username (this becomes your email: username@gmail.com)
   - Create a strong password
3. Click "Next"
4. Add your phone number (optional but recommended)
5. Add recovery email (optional)
6. Enter your birthday and gender
7. Click "Next"
8. Review and accept Google's Terms of Service
9. Your Google account is ready!

### Step 2: Sign in to Google

1. Go to https://google.com
2. Click "Sign in" in the top right corner
3. Enter your email and password
4. You should see your profile icon in the top right

## Part 2: Google Cloud Console Setup

### Step 3: Access Google Cloud Console

1. Go to: https://console.cloud.google.com
2. You'll see a welcome screen if it's your first time
3. You might need to:
   - Accept the Terms of Service
   - Click "Select a Country" and choose your country
   - Click "Agree and Continue"

### Step 4: Create Your First Project

1. At the top of the page, you'll see "Select a project" dropdown
2. Click on it → Click "NEW PROJECT"
3. Fill in:
   - **Project name**: `MCP-Learning` (or any name you like)
   - **Location**: Leave as "No organization" (unless you have one)
4. Click "CREATE"
5. Wait about 30 seconds for the project to be created
6. You'll get a notification when it's ready

### Step 5: Make Sure You're in the Right Project

1. Click the dropdown at the top that shows project name
2. Make sure "MCP-Learning" (or your project name) is selected
3. If not, select it from the list

## Part 3: Enable Google Sheets API

### Step 6: Navigate to API Library

1. Click the hamburger menu (☰) in the top left
2. Hover over "APIs & Services"
3. Click "Library"

### Step 7: Find and Enable Google Sheets API

1. In the search box, type: `Google Sheets`
2. Click on "Google Sheets API" from the results
3. You'll see a page describing the API
4. Click the blue "ENABLE" button
5. Wait for it to enable (about 10-30 seconds)
6. You'll be redirected to the API dashboard

## Part 4: Create Service Account (Robot User)

### Step 8: Go to Credentials

1. In the left sidebar, click "Credentials"
2. You'll see a page about credentials

### Step 9: Create Service Account

1. Click "+ CREATE CREDENTIALS" button at the top
2. Select "Service account" from the dropdown
3. Fill in Step 1 of 3:
   - **Service account name**: `mcp-sheets-robot`
   - **Service account ID**: (this auto-fills)
   - **Description**: `Robot account for MCP to access Google Sheets`
4. Click "CREATE AND CONTINUE"

### Step 10: Skip Optional Permissions (Step 2 of 3)

1. You'll see "Grant this service account access to project"
2. Just click "CONTINUE" (we don't need special permissions)

### Step 11: Skip User Access (Step 3 of 3)

1. You'll see "Grant users access to this service account"
2. Just click "DONE"

### Step 12: Create the Key File

1. You should now see your service account in the list
2. Click on the email that looks like: `mcp-sheets-robot@mcp-learning-xxxxx.iam.gserviceaccount.com`
3. Click on "KEYS" tab at the top
4. Click "ADD KEY" → "Create new key"
5. Choose "JSON" (should be selected by default)
6. Click "CREATE"
7. **IMPORTANT**: A file will download to your computer!
   - It will be named something like: `mcp-learning-xxxxx-xxxxxxxxxxxx.json`
   - This is your secret key file - keep it safe!

### Step 13: Move and Rename the Key File

1. Find the downloaded file (usually in Downloads folder)
2. Move it to: `/Users/kangchinshen/Desktop/python-model-context-protocol/google_sheets_mcp/`
3. Rename it to: `google-credentials.json`

On Mac, you can do this in Terminal:
```bash
# Replace the xxxxx with your actual filename
mv ~/Downloads/mcp-learning-*.json ~/Desktop/python-model-context-protocol/google_sheets_mcp/google-credentials.json
```

## Part 5: Create Test Google Sheet

### Step 14: Create a New Spreadsheet

1. Go to: https://sheets.google.com
2. Click the big "+" button to create a new blank spreadsheet
3. Name it by clicking "Untitled spreadsheet" at the top
4. Type: `MCP Test Q&A`

### Step 15: Set Up the Columns

Click on each cell and type exactly:
- **A1**: `Question ID`
- **B1**: `Question Text`
- **C1**: `Status`
- **D1**: `Answer`
- **E1**: `Timestamp`
- **F1**: `Answered By`

### Step 16: Add Sample Questions

Starting from row 2, add this sample data:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Q001 | How much does the Professional plan cost? | unanswered | | | |
| Q002 | Can I cancel my subscription anytime? | unanswered | | | |
| Q003 | What payment methods do you accept? | unanswered | | | |
| Q004 | Is there a student discount? | unanswered | | | |
| Q005 | How do I reset my password? | unanswered | | | |

### Step 17: Get the Sheet ID

1. Look at your browser's address bar
2. The URL looks like: `https://docs.google.com/spreadsheets/d/XXXXXXXXXX/edit#gid=0`
3. Copy the part where XXXXXXXXXX is (between `/d/` and `/edit`)
4. This is your Sheet ID - save it in .env as GOOGLE_SHEETS_ID

Example:
- URL: `https://docs.google.com/spreadsheets/d/1a2B3c4D5e6F7g8H9i0J/edit#gid=0`
- Sheet ID: `1a2B3c4D5e6F7g8H9i0J`

### Step 18: Find Your Service Account Email

1. Open the `google-credentials.json` file you saved earlier
2. Look for a line that says `"client_email":`
3. Copy the email address (looks like: `mcp-sheets-robot@mcp-learning-xxxxx.iam.gserviceaccount.com`)

You can use this command:
```bash
grep client_email ~/Desktop/python-model-context-protocol/google_sheets_mcp/google-credentials.json
```

### Step 19: Share the Sheet with Your Robot

1. Go back to your Google Sheet
2. Click the green "Share" button in the top right
3. In the "Add people and groups" box, paste the service account email
4. Make sure it says "Editor" in the dropdown (not "Viewer")
5. **IMPORTANT**: Uncheck "Notify people" (robots don't read email!)
6. Click "Share"

## Part 6: Configure the MCP Server

### Step 20: Create the Environment File

1. Navigate to the google_sheets_mcp folder:
```bash
cd ~/Desktop/python-model-context-protocol/google_sheets_mcp
```

2. Create the .env file:
```bash
cat > .env << EOF
GOOGLE_SHEETS_ID=YOUR_SHEET_ID_HERE
GOOGLE_CREDENTIALS_PATH=./google-credentials.json
SHEET_NAME=Sheet1
EOF
```

3. Edit the .env file and replace YOUR_SHEET_ID_HERE with your actual Sheet ID from Step 17

### Step 21: Test the Connection

1. Make sure you're in the virtual environment:
```bash
cd ~/Desktop/python-model-context-protocol
source .venv/bin/activate
```

2. Test the connection:
```bash
cd google_sheets_mcp
python3 << 'EOF'
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

print(f"Sheet ID: {SHEETS_ID}")
print(f"Credentials Path: {CREDENTIALS_PATH}")

try:
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=credentials)
    
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEETS_ID, 
        range="A1:F1"
    ).execute()
    
    headers = result.get('values', [[]])[0]
    print("✅ SUCCESS! Connected to Google Sheets!")
    print(f"Headers: {headers}")
    
    # Try to read questions
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEETS_ID,
        range="A2:C6"
    ).execute()
    
    questions = result.get('values', [])
    print(f"\nFound {len(questions)} questions:")
    for q in questions:
        print(f"  - {q[0]}: {q[1]} [{q[2]}]")
    
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

### Expected Output

If everything is set up correctly, you should see:
```
Sheet ID: 1a2B3c4D5e6F7g8H9i0J
Credentials Path: ./google-credentials.json
✅ SUCCESS! Connected to Google Sheets!
Headers: ['Question ID', 'Question Text', 'Status', 'Answer', 'Timestamp', 'Answered By']

Found 5 questions:
  - Q001: How much does the Professional plan cost? [unanswered]
  - Q002: Can I cancel my subscription anytime? [unanswered]
  - Q003: What payment methods do you accept? [unanswered]
  - Q004: Is there a student discount? [unanswered]
  - Q005: How do I reset my password? [unanswered]
```

## Troubleshooting

### "File not found" Error
- Make sure google-credentials.json is in the google_sheets_mcp folder
- Check the filename is exactly `google-credentials.json`

### "Permission denied" Error
- Make sure you shared the sheet with the service account email
- Check that you gave "Editor" permission, not "Viewer"

### "Invalid credentials" Error
- You might have the wrong credentials file
- Try downloading a new key from Google Cloud Console

### Can't find Sheet ID
- The Sheet ID is in the URL between `/d/` and `/edit`
- It's a long string of letters and numbers
- Don't include the `/d/` or `/edit` parts

## Security Reminder

⚠️ **IMPORTANT SECURITY NOTES:**
1. NEVER share your `google-credentials.json` file with anyone
2. NEVER commit it to Git (it's already in .gitignore)
3. This file gives full access to your Google Sheets
4. If you think it's been compromised, delete the key in Google Cloud Console and create a new one

## Next Steps

Now that Google Sheets is connected, you can:
1. Run the MCP server: `python src/server.py`
2. Configure Claude Desktop to use the server
3. Start asking Claude to read and update your Google Sheet!

Congratulations! You've successfully set up Google Sheets authentication for your MCP server! 🎉