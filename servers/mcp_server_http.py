from fastmcp import FastMCP
from typing import Any, Dict

from search_enrich_workflow import search_scrap_enrich
from tools.weather.weather_service import get_weather_by_location
from tools.summarizer.summarizer import summarize_content

mcp = FastMCP("My MCP Server")

@mcp.tool
async def get_websearch(input: Dict[str, Any]) -> Dict[str, Any]:
    """
    input: { "query": str }
    """
    print("[DEBUG] get_websearch called with input:", input)
    query = input["query"]
    result = await search_scrap_enrich(query)
    # print("[DEBUG] get_websearch result:", result)
    return {"result": result}

@mcp.tool
async def get_weather(input: Dict[str, Any]) -> Dict[str, Any]:
    """
    input: { "location": str }
    """
    print("[DEBUG] get_weather called with input:", input)
    location = input["location"]
    result = get_weather_by_location(location)
    # print("[DEBUG] get_weather result:", result)
    return result

@mcp.tool
async def get_summarized_content(input: Dict[str, Any]) -> Dict[str, Any]:
    """
    input: { "data": str }
    """
    # print("[DEBUG] get_summarized_content called with input:", input)
    data = input["data"]
    result = await summarize_content(data)
    # print("[DEBUG] get_summarized_content result:", result)
    return result

@mcp.tool
async def ping(input: Dict[str, Any] = None) -> Dict[str, Any]:
    print("[DEBUG] ping called with input:", input)
    return {"result": "pong"}

if __name__ == "__main__":
    mcp.run(transport="http", port=8001)