# Async OpenAI Client Module

A robust, production-ready async wrapper for the OpenAI API with comprehensive error handling, retry logic, and modern Python patterns.

## Features

✅ **Robust Error Handling** - Comprehensive exception handling with smart retry logic  
✅ **Exponential Backoff** - Intelligent retry delays with jitter to prevent API flooding  
✅ **JSON Response Support** - Built-in JSON validation and cleaning  
✅ **Concurrent Requests** - Rate-limited concurrent processing with semaphores  
✅ **Context Manager Support** - Proper resource management  
✅ **Configuration Management** - Flexible configuration with environment variable support  
✅ **Production Ready** - Logging, timeouts, and best practices built-in  
✅ **Type Hints** - Full typing support for better IDE experience  
✅ **Backward Compatible** - Drop-in replacement for your existing Azure OpenAI code  

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install openai python-dotenv httpx
```

## Quick Start

### 1. Set up your environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_OPENAI_API_KEY_here
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.0
OPENAI_TIMEOUT=60.0
OPENAI_MAX_RETRIES=3
```

### 2. Basic Usage

```python
import asyncio
from async_openai_client import get_async_gpt_response, get_async_gpt_json_response

async def main():
    # Simple text completion
    response = await get_async_gpt_response(
        prompt_text="Explain async programming in Python",
        system_message="You are a helpful programming assistant."
    )
    print(response)
    
    # JSON completion
    json_response = await get_async_gpt_json_response(
        prompt_text="List top 3 Python libraries for web scraping",
        system_message="Return JSON with library name and description."
    )
    print(json_response)

asyncio.run(main())
```

### 3. Advanced Usage with Client

```python
import asyncio
from async_openai_client import AsyncOpenAIClient, OpenAIConfig

async def main():
    # Custom configuration
    config = OpenAIConfig(
        model_name="gpt-4o",
        max_retries=5,
        timeout=120.0,
        temperature=0.7
    )
    
    # Use as context manager
    async with AsyncOpenAIClient(config) as client:
        # Single completion
        response = await client.get_completion(
            prompt="Write a haiku about programming",
            system_message="You are a creative poet."
        )
        print(response)
        
        # Multiple concurrent completions
        prompts = [
            "Explain REST APIs",
            "Explain GraphQL", 
            "Explain WebSockets"
        ]
        
        results = await client.get_multiple_completions(
            prompts=prompts,
            max_concurrent=3
        )
        
        for i, result in enumerate(results):
            print(f"Response {i+1}: {result}")

asyncio.run(main())
```

## Configuration Options

### OpenAIConfig Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | `None` | OpenAI API key (auto-loads from env) |
| `model_name` | `str` | `"gpt-4o"` | OpenAI model to use |
| `max_retries` | `int` | `3` | Maximum retry attempts |
| `retry_delay` | `float` | `1.0` | Base delay between retries (seconds) |
| `timeout` | `float` | `60.0` | Request timeout (seconds) |
| `temperature` | `float` | `0.0` | Response creativity (0.0-2.0) |
| `max_tokens` | `int` | `None` | Maximum response tokens |

### Environment Variables

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.0
OPENAI_MAX_TOKENS=1000
OPENAI_TIMEOUT=60.0
OPENAI_MAX_RETRIES=3
OPENAI_RETRY_DELAY=1.0
OPENAI_MAX_CONCURRENT=5
OPENAI_LOG_LEVEL=INFO
```

## Error Handling

The module intelligently handles various error types:

### Retryable Errors
- **API Timeout Errors** - Network/server timeouts
- **Rate Limit Errors** - API rate limiting (429)
- **API Connection Errors** - Network connectivity issues
- **Server Errors** - 5xx HTTP status codes

### Non-Retryable Errors
- **Authentication Errors** - Invalid API key
- **Permission Denied** - Insufficient permissions
- **Bad Request Errors** - Invalid request format

### Retry Logic
- **Exponential Backoff** - Delays increase exponentially (1s, 2s, 4s, 8s...)
- **Jitter** - Random delay variation to prevent thundering herd
- **Smart Error Detection** - Only retries appropriate error types

## Integration with Existing Settings

The module works with your existing settings pattern:

```python
# settings.py (your existing file)
from settings import settings

# Use with your settings
from async_openai_client import OpenAIConfig

config = OpenAIConfig(**settings.openai_config_dict)
```

## Migration from Azure OpenAI

Easy migration from your existing Azure OpenAI code:

### Before (Azure OpenAI)
```python
async def get_async_gpt4o_response(prompt_text: str, system_message: str = "You are a helpful assistant.") -> str | None:
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt_text}
    ]
    
    response = await azure_client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content
```

### After (OpenAI)
```python
# Direct replacement
from async_openai_client import get_async_gpt_response as get_async_gpt4o_response

# Or with custom config
async def get_async_gpt4o_response(prompt_text: str, system_message: str = "You are a helpful assistant.") -> str | None:
    return await get_async_gpt_response(prompt_text, system_message)
```

## API Reference

### AsyncOpenAIClient

#### Methods

- **`get_completion(prompt, system_message, **kwargs)`** - Get text completion
- **`get_json_completion(prompt, system_message, validate_json=True, **kwargs)`** - Get JSON completion  
- **`get_multiple_completions(prompts, system_message, max_concurrent=5, **kwargs)`** - Concurrent completions

#### Context Manager
```python
async with AsyncOpenAIClient(config) as client:
    # Client automatically closed when exiting context
    response = await client.get_completion("Hello")
```

### Convenience Functions

- **`get_async_gpt_response(prompt_text, system_message, config)`** - Simple completion
- **`get_async_gpt_json_response(prompt_text, system_message, config)`** - JSON completion

## Best Practices

### 1. Use Context Managers
```python
async with AsyncOpenAIClient(config) as client:
    # Ensures proper cleanup
    response = await client.get_completion("prompt")
```

### 2. Configure Appropriate Timeouts
```python
# For simple queries
config = OpenAIConfig(timeout=30.0)

# For complex tasks
config = OpenAIConfig(timeout=120.0)
```

### 3. Handle Rate Limits
```python
# Limit concurrent requests
results = await client.get_multiple_completions(
    prompts=many_prompts,
    max_concurrent=3  # Adjust based on your rate limits
)
```

### 4. Use Structured Outputs
```python
# For structured data, always use JSON completion
json_response = await client.get_json_completion(
    prompt="Generate user data",
    system_message="Return JSON with name, email, age fields"
)
```

## Logging

The module provides comprehensive logging:

```python
import logging

# Set log level
logging.getLogger('async_openai_client').setLevel(logging.DEBUG)

# Logs include:
# - Request attempts and retries
# - Error details and types
# - Response validation
# - Performance metrics
```

## Testing

Run the example file to test your setup:

```bash
python example_usage.py
```

This will run comprehensive tests of all functionality.

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'openai'**
   ```bash
   pip install openai>=1.30.0
   ```

2. **ValueError: OPENAI_API_KEY must be set**
   - Add your API key to `.env` file
   - Or set environment variable: `export OPENAI_API_KEY=your_key`

3. **Timeout Errors**
   - Increase timeout: `OpenAIConfig(timeout=120.0)`
   - Check network connectivity
   - Verify API key permissions

4. **Rate Limit Errors**
   - Reduce concurrent requests: `max_concurrent=2`
   - Increase retry delay: `OpenAIConfig(retry_delay=2.0)`
   - Check your OpenAI usage limits

## Contributing

1. Fork the repository
2. Make your changes
3. Add tests for new functionality
4. Ensure all examples run successfully
5. Submit a pull request

## License

This module is provided as-is for educational and development purposes. Please ensure you comply with OpenAI's usage policies and terms of service.

---

**Built with ❤️ for robust, production-ready OpenAI integration**