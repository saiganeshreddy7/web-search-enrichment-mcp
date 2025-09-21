from typing import Any
from mcp.server.fastmcp import FastMCP
from search_enrich_workflow import search_scrap_enrich

mcp = FastMCP("enrich_query")


@mcp.tool()
async def enrich_query(query: str) -> Any:
    result = await search_scrap_enrich(query)
    return result


if __name__ == "__main__":
    mcp.run(transport="stdio")