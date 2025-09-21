# Web Search Enrichment MCP

A Model Context Protocol (MCP) server that provides web search enrichment capabilities by combining Google search results with web scraping and content parsing.

## File Structure

### Core Files

- **`mcp_server.py`** - Main MCP server that exposes the enrichment functionality
- **`search_enrich_workflow.py`** - Core workflow orchestrator that combines search, scraping, and parsing
- **`google_search_client.py`** - Google search API client using Serper API
- **`web_content_fetcher.py`** - Multi-tier web content fetcher (aiohttp → cloudscraper → Playwright)
- **`html_text_parser.py`** - HTML parser that extracts clean text using BeautifulSoup4
- **`config.py`** - Configuration and environment variable management

### Testing & Utilities

- **`mcp_client_test.py`** - Test client for the MCP server
- **`requirements.txt`** - Python dependencies
- **`.env`** - Environment variables (API keys, etc.)

## Workflow

1. **Search**: Query Google using Serper API to get organic search results
2. **Fetch**: Download HTML content from search result URLs using multiple fallback strategies
3. **Parse**: Extract clean text from HTML using BeautifulSoup4
4. **Enrich**: Combine original search results with scraped content

## Features

- **Multi-tier fetching**: Falls back from aiohttp → cloudscraper → Playwright for maximum success rate
- **Async processing**: Concurrent fetching and processing for better performance
- **Clean text extraction**: Removes scripts, styles, and HTML tags
- **Error resilience**: Handles failures gracefully without breaking the workflow

## Usage

Run the MCP server:
```bash
python mcp_server.py
```

Test the functionality:
```bash
python mcp_client_test.py
```