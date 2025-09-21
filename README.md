### 🚀 file structure & naming

```bash
.
├── config.py
├── google_search_client.py
├── html_text_parser.py
├── search_enrich_workflow.py
├── web_content_fetcher.py
│
├── servers/
│   ├── mcp_server_stdio.py   # MCP server using STDIO transport
│   ├── mcp_server_http.py    # MCP server using HTTP transport (FastMCP)
│
├── clients/
│   ├── client_stdio_test.py  # Test client for STDIO server
│   ├── client_http_test.py   # Test client for HTTP server
│
├── requirements.txt
├── .env
├── README.md
```

---

````markdown
# Web Search Enrichment MCP

A **Model Context Protocol (MCP) server** that provides web search enrichment 
by combining Google search results with web scraping and content parsing.

---

## File Structure

### Core Components
- **`search_enrich_workflow.py`** – Core workflow: search → scrape → parse → enrich
- **`google_search_client.py`** – Google search API client (Serper API)
- **`web_content_fetcher.py`** – Multi-tier fetcher (aiohttp → cloudscraper → Playwright)
- **`html_text_parser.py`** – Clean text extraction with BeautifulSoup4
- **`config.py`** – Env/config management

### MCP Servers
- **`servers/mcp_server_stdio.py`** – Runs the MCP server with **STDIO transport**  
- **`servers/mcp_server_http.py`** – Runs the MCP server with **HTTP transport** (via FastMCP)

### Clients
- **`clients/client_stdio_test.py`** – Test client for STDIO server  
- **`clients/client_http_test.py`** – Client for HTTP server (can be used from another repo)

---

## Workflow

1. **Search** → query Google via Serper API  
2. **Fetch** → retrieve HTML content with resilient fallbacks  
3. **Parse** → clean text extraction  
4. **Enrich** → combine search + scraped context  

---

## Usage

### Run with STDIO
```bash
python servers/mcp_server_stdio.py
````

Test with:

```bash
python clients/client_stdio_test.py
```

---

### Run with HTTP (FastMCP)

```bash
python servers/mcp_server_http.py
```

Call the tool:

```bash
python clients/client_http_test.py
```

---

## Features

* **Multi-tier fetching**: aiohttp → cloudscraper → Playwright
* **Async**: concurrent search & scraping
* **Clean text**: strips scripts, styles, boilerplate
* **Error resilience**: gracefully handles failures

```

---

This way:  
- `mcp_server_stdio.py` is **local-friendly** (plugin-style).  
- `mcp_server_http.py` is **remote-friendly** (service-style).  
- Clients are clearly named and sit in `clients/`.  

