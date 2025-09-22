import asyncio
from fastmcp import Client

client = Client("http://localhost:8001/mcp")

async def call_tool(query: str):
    async with client:
        result = await client.call_tool("enrich_query", {"query": query})
        print(result)

async def test_ping():
    async with client:
        result = await client.call_tool("ping", {})
        # Parse pong value from result
        pong_value = None
        if hasattr(result, "data"):
            pong_value = result.data
        elif hasattr(result, "structured_content") and "result" in result.structured_content:
            pong_value = result.structured_content["result"]
        if pong_value == "pong":
            print("pong pong pong")
        else:
            print("Ping result:", result)



query = """Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?"""
asyncio.run(test_ping())
# asyncio.run(call_tool(query))