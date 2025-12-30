import asyncio
from fastmcp import Client
import json

client = Client("http://localhost:8001/mcp")


async def test_ping():
    async with client:
        result = await client.call_tool("ping", {})
        # Parse pong value from result
        pong_value = None
        if hasattr(result, "data"):
            pong_value = result.data
        elif (
            hasattr(result, "structured_content")
            and "result" in result.structured_content
        ):
            pong_value = result.structured_content["result"]
        if pong_value == "pong":
            print("pong pong pong")
        else:
            print("Ping result:", result)


async def websearch(query: str):
    async with client:
        result = await client.call_tool("get_websearch", {"query": query})
        return result


async def weather(location: str):
    async with client:
        result = await client.call_tool(
            name="get_weather", arguments={"location": location}
        )
        return result


async def summarize(data: list[dict[str, any]]):
    async with client:
        result = await client.call_tool(
            name="get_summarized_content", arguments={"data": data}
        )
        return result


if __name__ == "__main__":
    print("""select which tool to run 
        0:test_ping 
        1:websearch 
        2:weather 
        3:summarize""")

    input_value = input()
    if input_value == "0":
        asyncio.run(test_ping())

    elif input_value == "1":
        query = "What's the weather like in New York?"
        result = asyncio.run(websearch(query))
        # Extract the exact same JSON data structure
        final_data = []
        for content in result.content:
            if hasattr(content, "text"):
                final_data.append(json.loads(content.text))
        print(json.dumps(final_data, indent=2))

    elif input_value == "2":
        location = "New York"
        result = asyncio.run(weather(location))
        # Extract the exact same JSON data structure
        final_data = []
        for content in result.content:
            if hasattr(content, "text"):
                final_data.append(json.loads(content.text))
        print(json.dumps(final_data, indent=2))
    elif input_value == "3":
        sample_data = [
            {
                "websearch": {
                    "headline": "Mumbai experiences warm temperatures",
                    "source": "example.com",
                },
                "weather": {
                    "location": "Mumbai",
                    "temperature": "24°C",
                    "condition": "Sunny",
                },
            }
        ]
        result = asyncio.run(summarize(sample_data))
        # Extract the exact same JSON data structure
        final_data = []
        for content in result.content:
            if hasattr(content, "text"):
                final_data.append(json.loads(content.text))
        print(json.dumps(final_data, indent=2))
