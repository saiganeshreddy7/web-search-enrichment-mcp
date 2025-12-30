import asyncio
from fastmcp import Client
import json

client = Client("http://localhost:8001/mcp")

async def call_websearch(query):
    async with client:
        return await client.call_tool("get_websearch", {"input": {"query": query}})

async def call_weather(location):
    async with client:
        return await client.call_tool("get_weather", {"input": {"location": location}})

async def sequential_run():
    print("Sequential run:")
    result1 = await call_websearch("top sightseeing spots in Tokyo")
    print("**"*40)
    print("Websearch result:")
    print(json.dumps(result1.result if hasattr(result1, 'result') else str(result1), indent=2, ensure_ascii=False))
    print("**"*40)
    result2 = await call_weather("Tokyo")
    print("Weather result:")
    print(json.dumps(result2.result if hasattr(result2, 'result') else str(result2), indent=2, ensure_ascii=False))
    print("**"*40)

async def parallel_run():
    print("Parallel run:")
    tasks = [
        call_websearch("top sightseeing spots in Tokyo"),
        call_weather("Tokyo")
    ]
    results = await asyncio.gather(*tasks)
    print("**"*40)
    print("Websearch result:")
    print(json.dumps(results[0].result if hasattr(results[0], 'result') else str(results[0]), indent=2, ensure_ascii=False))
    print("**"*40)
    print("Weather result:")
    print(json.dumps(results[1].result if hasattr(results[1], 'result') else str(results[1]), indent=2, ensure_ascii=False))
    print("**"*40)

if __name__ == "__main__":
    print("Select run mode:\n1: Sequential\n2: Parallel")
    mode = input().strip()
    if mode == "1":
        asyncio.run(sequential_run())
    elif mode == "2":
        asyncio.run(parallel_run())
    else:
        print("Invalid selection.")
