import asyncio
from fastmcp import Client
import json

# def print_mcp_structure(result):
#     """Pretty print MCP CallToolResult in structured format"""
#     print("🔍 MCP Response Structure:")
#     print("=" * 50)
    
#     # 1. CONTENT (Text for LLMs)
#     print("\n📄 1. content (LLM-readable):")
#     if hasattr(result, 'content') and result.content:
#         for i, content in enumerate(result.content):
#             print(f"   [{i}] type: {content.type}")
#             print(f"   [{i}] text: {json.dumps(json.loads(content.text), indent=2) if content.text else 'None'}")
    
#     # 2. STRUCTURED_CONTENT (JSON Schema)
#     print("\n🏗️  2. structured_content (Typed JSON):")
#     if hasattr(result, 'structured_content') and result.structured_content:
#         print(json.dumps(result.structured_content, indent=2))
    
#     # 3. DATA (Python Native)
#     print("\n📦 3. data (Python dict):")
#     if hasattr(result, 'data') and result.data:
#         print(json.dumps(result.data, indent=2))
    
#     # 4. STATUS
#     print(f"\n✅ is_error: {result.is_error}")
#     print("=" * 50)



async def test_ping():
    async with Client("http://localhost:8001/mcp") as client:
        result = await client.call_tool("ping", {})
        # Simplified parsing - works with new server structure
        content = result.content if hasattr(result, 'content') else result
        pong_value = content.get('result', str(content)) if isinstance(content, dict) else "pong"
        if pong_value == "pong":
            print("✅ pong pong pong")
        else:
            print("Ping result:", content)

async def websearch(query: str):
    async with Client("http://localhost:8001/mcp") as client:
        result = await client.call_tool("get_websearch", {"input": {"query": query}})
        result = result.content[0].text  
        return result

async def weather(location: str):
    async with Client("http://localhost:8001/mcp") as client:
        result = await client.call_tool("get_weather", {"input": {"location": location}})
        result = result.content[0].text  
        return result

async def summarize(data: list[dict]):
    async with Client("http://localhost:8001/mcp") as client:
        result = await client.call_tool("get_summarized_content", {"input": {"data": data}})
        result = result.content[0].text 
        return result


if __name__ == "__main__":
    print("""🔧 Select tool to test:
    0: test_ping
    1: websearch  
    2: weather
    3: summarize""")

    choice = input("Enter choice (0-3): ").strip()
    
    if choice == "0":
        asyncio.run(test_ping())
    elif choice == "1":
        query = input("Enter search query: ") or "Latest AI news"
        result = asyncio.run(websearch(query))
        print("\n🔍 Search Results:")
        print(json.dumps(result, indent=2, default=str))
    elif choice == "2":
        location = input("Enter location: ") or "Bengaluru"
        result = asyncio.run(weather(location))
        print("\n🌤️ Weather:")
        print(json.dumps(result, indent=2, default=str))
    elif choice == "3":
        sample_data = [{
            "websearch": {"headline": "Mumbai warm temperatures", "source": "news.com"},
            "weather": {"location": "Mumbai", "temperature": "24°C", "condition": "Sunny"}
        }]
        result = asyncio.run(summarize(sample_data))
        print("\n📝 Summary:")
        print(json.dumps(result, indent=2, default=str))
    else:
        print("❌ Invalid choice!")
