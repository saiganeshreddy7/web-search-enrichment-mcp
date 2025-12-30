import asyncio
from fastmcp import Client

async def test_ping():
    async with Client("http://localhost:8001/mcp") as client: 
        result = await client.call_tool("ping", {})
        print("Ping result:", result.content if hasattr(result, 'content') else result)

async def call_tool(query: str):
    async with Client("http://localhost:8001/mcp") as client:
        result = await client.call_tool("enrich_query", {"query": query})
        print(result.content if hasattr(result, 'content') else result)

if __name__ == "__main__":
    asyncio.run(test_ping())
