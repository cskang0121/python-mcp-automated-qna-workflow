# Knowledge Base MCP Server

This MCP server provides access to local text documentation, enabling Claude to search and retrieve information from your business documents.

## Features

- **List Documents**: Browse available documentation files
- **Read Document**: Retrieve full content of specific documents
- **Search Content**: Search across all documents for specific information
- **Category Organization**: Documents organized by type (products, support, policies)

## Setup

### 1. Install Dependencies

```bash
cd knowledge_base_mcp
uv venv
uv pip install -e .
```

### 2. Add Your Documentation

Place your text documents in the `data/` directory:

```
knowledge_base_mcp/data/
├── products/
│   ├── product-overview.txt
│   ├── pricing.txt
│   └── features.txt
├── support/
│   ├── faq.txt
│   ├── troubleshooting.txt
│   └── getting-started.txt
└── policies/
    ├── refund-policy.txt
    ├── privacy-policy.txt
    └── terms-of-service.txt
```

### 3. Configuration

The server reads all `.txt` files from the `data/` directory and its subdirectories.

## Running the Server

```bash
python src/server.py
```

The server will start and be available for Claude Desktop to connect.

## Available Tools

### `list_documents`
Returns a list of all available documents organized by category.

**Example Response:**
```json
{
  "products": ["product-overview.txt", "pricing.txt"],
  "support": ["faq.txt", "troubleshooting.txt"],
  "policies": ["refund-policy.txt"]
}
```

### `read_document`
Reads the full content of a specific document.

**Parameters:**
- `path`: Document path relative to data directory (e.g., "products/pricing.txt")

### `search_documents`
Searches across all documents for specific keywords or phrases.

**Parameters:**
- `query`: Search term or phrase
- `max_results`: Maximum number of results to return (default: 10)

**Returns:** Matching excerpts with document references

## Document Format

Documents should be plain text files (.txt) with clear formatting:

```text
# Section Title

Content goes here...

## Subsection

More detailed information...
```

## Best Practices

1. **Clear Naming**: Use descriptive filenames (e.g., `refund-policy.txt` not `doc1.txt`)
2. **Consistent Structure**: Use consistent formatting across documents
3. **Regular Updates**: Keep documentation current
4. **Categorization**: Group related documents in subdirectories

## Testing

```bash
uv pip install -e ".[dev]"
pytest tests/
```

## Adding Sample Documentation

Quick start with sample docs:

```bash
# Product information
echo "Our product costs \$99/month with a 30-day free trial." > data/products/pricing.txt
echo "Q: How do I reset my password?\nA: Click 'Forgot Password' on the login page." > data/support/faq.txt
echo "We offer a 30-day money-back guarantee." > data/policies/refund-policy.txt
```