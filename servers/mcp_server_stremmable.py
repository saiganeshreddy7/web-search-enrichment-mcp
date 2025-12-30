from fastmcp import FastMCP
from fastmcp_docs import FastMCPDocs
from typing import Any, Annotated
import asyncio
from search_enrich_workflow import search_scrap_enrich

mcp = FastMCP("My MCP Server")

@mcp.tool(tags=["search"])
async def enrich_query(
    query: Annotated[str, "Search query to enrich with data"]
) -> Any:
    """Enrich a query with search and scraped data"""
    result = await search_scrap_enrich(query)
    return result

@mcp.tool(tags=["health"])
async def ping() -> str:
    """Health check endpoint"""
    return "pong"

# Setup Swagger-style UI (3 lines!)
docs = FastMCPDocs(
    mcp=mcp,
    title="🛠️ My MCP Server Tools",
    version="1.0.0",
    description="Search enrichment and health check tools"
)

if __name__ == "__main__":
    asyncio.run(docs.setup())
    mcp.run(transport="streamable-http", port=8001)  # Changed here!

