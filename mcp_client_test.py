import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main(query: str) -> list[dict]:
    server_params = StdioServerParameters(command="python", args=["mcp_server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Call the tool
            result = await session.call_tool("enrich_query", {"query": query})

            # Extract the exact same JSON data structure
            final_data = []
            for content in result.content:
                if hasattr(content, "text"):
                    # Parse back to original format
                    final_data.append(json.loads(content.text))

            # This returns the EXACT same format as sent
            return final_data


if __name__ == "__main__":
    query = """Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?"""
    # Get the exact same data structure back
    returned_data = asyncio.run(main(query))
    # Print it nicely
    print("RETURNED DATA (same format as sent):")
    print(json.dumps(returned_data, indent=2))