from fastmcp import FastMCP
from typing import Any
from search_enrich_workflow import search_scrap_enrich

mcp = FastMCP("My MCP Server")

@mcp.tool
async def enrich_query(query: str) -> Any:
    result = await search_scrap_enrich(query)
    return result

@mcp.tool
async def ping() -> str:
    return "pong"

if __name__ == "__main__":
    mcp.run(transport="http", port=8001)