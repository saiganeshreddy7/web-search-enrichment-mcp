import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(query: str):
    async with client:
        result = await client.call_tool("enrich_query", {"query": query})
        print(result)



query = """Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?"""
asyncio.run(call_tool(query))