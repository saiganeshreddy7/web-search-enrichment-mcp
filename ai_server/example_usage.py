"""
Example usage of the Async OpenAI Client
Demonstrates various ways to use the robust async OpenAI wrapper.
"""

import asyncio
import json

# Import our custom modules
from async_openai_client import (
    AsyncOpenAIClient,
    OpenAIConfig,
    get_async_gpt_response,
    get_async_gpt_json_response,
)
from settings import settings


async def example_1_simple_usage():
    """Example 1: Simple usage with convenience functions."""
    print("=" * 60)
    print("EXAMPLE 1: Simple Usage with Convenience Functions")
    print("=" * 60)

    # Using convenience function with default settings
    response = await get_async_gpt_response(
        prompt_text="Explain what async programming is in Python in 2 sentences.",
        system_message="You are a helpful Python programming assistant.",
    )

    print(f"Response: {response}")
    print()


async def example_2_json_response():
    """Example 2: Getting structured JSON responses."""
    print("=" * 60)
    print("EXAMPLE 2: Structured JSON Responses")
    print("=" * 60)

    # Get JSON response about programming languages
    json_response = await get_async_gpt_json_response(
        prompt_text="List the top 3 programming languages for web development with their main use cases.",
        system_message="You are a programming expert. Return a JSON array with objects containing 'language', 'primary_use', and 'popularity_rank' fields.",
    )

    if json_response:
        try:
            # Parse and pretty print the JSON
            data = json.loads(json_response)
            print("Parsed JSON Response:")
            print(json.dumps(data, indent=2))
        except json.JSONDecodeError:
            print(f"Raw JSON Response: {json_response}")
    else:
        print("Failed to get JSON response")
    print()


async def example_3_custom_config():
    """Example 3: Using custom configuration."""
    print("=" * 60)
    print("EXAMPLE 3: Custom Configuration")
    print("=" * 60)

    # Create custom configuration
    config = OpenAIConfig(
        api_key=settings.OPENAI_API_KEY,
        model_name="gpt-4o-mini",  # Using different model
        max_retries=2,
        timeout=30.0,
        temperature=0.7,  # More creative responses
        max_tokens=150,
    )

    # Use with convenience function
    response = await get_async_gpt_response(
        prompt_text="Write a creative short story about a robot learning to paint.",
        system_message="You are a creative writing assistant.",
        config=config,
    )

    print(f"Creative Response: {response}")
    print()


async def example_4_client_context_manager():
    """Example 4: Using the client as a context manager."""
    print("=" * 60)
    print("EXAMPLE 4: Client Context Manager Usage")
    print("=" * 60)

    # Create config from settings
    config = OpenAIConfig(**settings.openai_config_dict)

    async with AsyncOpenAIClient(config) as client:
        # Single completion
        response1 = await client.get_completion(
            prompt="What is machine learning?",
            system_message="You are a technical educator. Explain concepts clearly and concisely.",
        )
        print(f"ML Explanation: {response1}")

        # JSON completion
        json_response = await client.get_json_completion(
            prompt="Create a simple task list for learning Python",
            system_message="Respond with JSON containing an array of tasks with 'task', 'difficulty', and 'estimated_hours' fields.",
        )

        if json_response:
            try:
                tasks = json.loads(json_response)
                print("\\nPython Learning Tasks:")
                print(json.dumps(tasks, indent=2))
            except json.JSONDecodeError:
                print(f"JSON Response: {json_response}")
    print()


async def example_5_multiple_concurrent_requests():
    """Example 5: Multiple concurrent requests."""
    print("=" * 60)
    print("EXAMPLE 5: Multiple Concurrent Requests")
    print("=" * 60)

    config = OpenAIConfig(api_key=settings.OPENAI_API_KEY, max_retries=2, timeout=45.0)

    async with AsyncOpenAIClient(config) as client:
        prompts = [
            "Explain what is REST API in one sentence.",
            "Explain what is GraphQL in one sentence.",
            "Explain what is WebSocket in one sentence.",
            "Explain what is gRPC in one sentence.",
            "Explain what is OAuth in one sentence.",
        ]

        print("Making 5 concurrent requests...")
        results = await client.get_multiple_completions(
            prompts=prompts,
            system_message="You are a technical expert. Provide clear, concise explanations.",
            max_concurrent=3,  # Limit to 3 concurrent requests
        )

        for i, result in enumerate(results):
            if result:
                print(f"{i + 1}. {result}")
            else:
                print(f"{i + 1}. Failed to get response")
    print()


async def example_6_error_handling():
    """Example 6: Error handling demonstration."""
    print("=" * 60)
    print("EXAMPLE 6: Error Handling Demo")
    print("=" * 60)

    # Create config with very short timeout to trigger timeout error
    config = OpenAIConfig(
        api_key=settings.OPENAI_API_KEY,
        timeout=1.0,  # Very short timeout
        max_retries=1,
    )

    async with AsyncOpenAIClient(config) as client:
        response = await client.get_completion(
            prompt="Write a detailed essay about the history of artificial intelligence, covering major milestones, key researchers, and technological breakthroughs from the 1950s to present day. Include specific examples and explain the impact of each development.",
            system_message="You are a technology historian.",
        )

        if response:
            print(f"Unexpected success: {response[:100]}...")
        else:
            print(
                "Expected failure due to short timeout - this demonstrates error handling"
            )
    print()


async def example_7_settings_integration():
    """Example 7: Integration with existing settings module."""
    print("=" * 60)
    print("EXAMPLE 7: Settings Integration")
    print("=" * 60)

    # Show current settings
    print("Current OpenAI Settings:")
    print(f"  API Key: {'Set' if settings.OPENAI_API_KEY else 'Not Set'}")
    print(f"  Model: {settings.OPENAI_MODEL}")
    print(f"  Temperature: {settings.OPENAI_TEMPERATURE}")
    print(f"  Timeout: {settings.OPENAI_TIMEOUT}")
    print(f"  Max Retries: {settings.OPENAI_MAX_RETRIES}")

    # Use settings directly
    config = OpenAIConfig(**settings.openai_config_dict)

    response = await get_async_gpt_response(
        prompt_text="Summarize the benefits of using environment variables for configuration.",
        config=config,
    )

    print(f"\\nResponse using settings: {response}")
    print()


async def main():
    """Run all examples."""
    print("ASYNC OPENAI CLIENT - COMPREHENSIVE EXAMPLES")
    print("=" * 80)

    try:
        await example_1_simple_usage()
        await example_2_json_response()
        await example_3_custom_config()
        await example_4_client_context_manager()
        await example_5_multiple_concurrent_requests()
        await example_6_error_handling()
        await example_7_settings_integration()

        print("=" * 80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 80)

    except Exception as e:
        print(f"Error in examples: {type(e).__name__}: {e}")


if __name__ == "__main__":
    # Make sure you have OPENAI_API_KEY in your .env file or environment
    asyncio.run(main())
