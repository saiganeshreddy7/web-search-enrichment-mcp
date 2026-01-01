from fastmcp import FastMCP
from typing import Any, Dict, Annotated
import asyncio

from fastmcp_docs import FastMCPDocs

from search_enrich_workflow import search_scrap_enrich
from tools.weather.weather_service import get_weather_by_location
from tools.summarizer.summarizer import summarize_content

mcp = FastMCP("My MCP Server")

@mcp.tool(tags=["search"])
async def get_websearch(
    input: Annotated[Dict[str, Any], "Input dict with 'query' key"]
) -> Dict[str, Any]:
    """
    Perform web search and enrichment for given query.
    input: { "query": str }
    """
    print("[DEBUG] get_websearch called with input:", input)
    query = input["query"]
    result = await search_scrap_enrich(query)
    return {"result": result}

@mcp.tool(tags=["weather"])
async def get_weather(
    input: Annotated[Dict[str, Any], "Input dict with 'location' key"]
) -> Dict[str, Any]:
    """
    Get current weather for a location.
    input: { "location": str }
    """
    print("[DEBUG] get_weather called with input:", input)
    location = input["location"]
    result = get_weather_by_location(location)
    # Ensure result is JSON serializable
    try:
        import json
        json.dumps(result)
        return result
    except Exception:
        # Fallback: convert to string if not serializable
        return {"result": str(result)}

@mcp.tool(tags=["summarize"])
async def get_summarized_content(
    input: Annotated[Dict[str, Any], "Input dict with 'data' key"]
) -> Dict[str, Any]:
    """
    Summarize given content.
    input: { "data": str }
    """
    data = input["data"]
    result = await summarize_content(data)
    return result

@mcp.tool(tags=["health"])
async def ping(input: Dict[str, Any] = None) -> Dict[str, Any]:
    """Health check endpoint"""
    print("[DEBUG] ping called with input:", input)
    return {"result": "pong"}

docs = FastMCPDocs(
    mcp=mcp,
    title="🛠️ My MCP Server - Search, Weather, Summarizer",
    version="1.0.0",
    description="Web search, weather lookup, and content summarization tools"
)

if __name__ == "__main__":
    # Setup docs BEFORE running
    asyncio.run(docs.setup())
    # mcp.run(transport="streamable-http", port=8001)
    # ✅ CHANGE THIS LINE IN YOUR SERVER
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)

