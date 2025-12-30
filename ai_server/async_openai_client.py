"""
Async OpenAI Module - A robust async wrapper for OpenAI API calls
Provides reliable chat completion and JSON response functionality with retry logic.
"""

import os
import re
import asyncio
import json
import logging
from typing import Optional, List
from dataclasses import dataclass
from dotenv import load_dotenv

try:
    from openai import AsyncOpenAI
    from openai.types.chat import ChatCompletionMessageParam
    from openai import (
        OpenAIError,
        APIError,
        APITimeoutError,
        RateLimitError,
        APIConnectionError,
        AuthenticationError,
        PermissionDeniedError,
        BadRequestError,
    )
except ImportError:
    raise ImportError("OpenAI library not found. Install with: pip install openai")


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class OpenAIConfig:
    """Configuration class for OpenAI client settings."""

    api_key: Optional[str] = None
    model_name: str = "gpt-4o"
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 60.0
    temperature: float = 0.0
    max_tokens: Optional[int] = None

    def __post_init__(self):
        """Initialize API key from environment if not provided."""
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY must be set in environment variables or passed directly"
            )


class AsyncOpenAIClient:
    """
    Robust async OpenAI client with error handling and retry logic.

    Features:
    - Exponential backoff retry logic
    - Comprehensive error handling
    - Support for both text and JSON responses
    - Configurable timeouts and retry policies
    - Proper logging and debugging
    """

    def __init__(self, config: Optional[OpenAIConfig] = None):
        """
        Initialize the async OpenAI client.

        Args:
            config: OpenAI configuration object. If None, uses default config.
        """
        self.config = config or OpenAIConfig()

        # Initialize the async OpenAI client
        self.client = AsyncOpenAI(
            api_key=self.config.api_key,
            timeout=self.config.timeout,
            max_retries=0,  # We handle retries ourselves for better control
        )

        logger.info(
            f"Initialized AsyncOpenAI client with model: {self.config.model_name}"
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def close(self):
        """Close the client connection."""
        if hasattr(self.client, "close"):
            await self.client.close()

    def _is_retryable_error(self, error: Exception) -> bool:
        """
        Determine if an error is retryable.

        Args:
            error: Exception to check

        Returns:
            bool: True if error should be retried
        """
        retryable_errors = (
            APITimeoutError,
            RateLimitError,
            APIConnectionError,
            APIError,
        )

        # Don't retry authentication or bad request errors
        non_retryable_errors = (
            AuthenticationError,
            PermissionDeniedError,
            BadRequestError,
        )

        if isinstance(error, non_retryable_errors):
            return False

        if isinstance(error, retryable_errors):
            return True

        # For generic OpenAI errors, check if it's a 5xx server error
        if isinstance(error, OpenAIError):
            if hasattr(error, "response") and error.response:
                status_code = error.response.status_code
                return 500 <= status_code < 600

        # Retry on network-related errors
        if isinstance(error, (ConnectionError, TimeoutError, asyncio.TimeoutError)):
            return True

        return False

    async def _make_request_with_retry(
        self, messages: List[ChatCompletionMessageParam], **kwargs
    ) -> str:
        """
        Make a request with retry logic and exponential backoff.

        Args:
            messages: Chat completion messages
            **kwargs: Additional arguments for the API call

        Returns:
            str: Response content

        Raises:
            OpenAIError: If all retries are exhausted
        """
        last_error = None

        for attempt in range(self.config.max_retries + 1):
            try:
                # Calculate delay with exponential backoff and jitter
                if attempt > 0:
                    delay = self.config.retry_delay * (2 ** (attempt - 1))
                    # Add jitter to prevent thundering herd
                    jitter = delay * 0.1 * (0.5 - asyncio.get_event_loop().time() % 1)
                    total_delay = delay + jitter

                    logger.info(
                        f"Retrying request (attempt {attempt + 1}/{self.config.max_retries + 1}) after {total_delay:.2f}s"
                    )
                    await asyncio.sleep(total_delay)

                # Make the API call
                response = await self.client.chat.completions.create(
                    model=self.config.model_name,
                    messages=messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                    **kwargs,
                )

                # Successful response
                content = response.choices[0].message.content
                if not content:
                    raise ValueError("Empty response received from OpenAI API")

                return content.strip()

            except Exception as e:
                last_error = e
                logger.warning(
                    f"API request failed (attempt {attempt + 1}): {type(e).__name__}: {e}"
                )

                # Check if we should retry
                if not self._is_retryable_error(e):
                    logger.error(
                        f"Non-retryable error encountered: {type(e).__name__}: {e}"
                    )
                    raise

                # If this was the last attempt, raise the error
                if attempt == self.config.max_retries:
                    logger.error(
                        f"All retry attempts exhausted. Last error: {type(e).__name__}: {e}"
                    )
                    raise

        # This should never be reached, but just in case
        raise last_error or OpenAIError("Request failed after all retries")

    async def get_completion(
        self,
        prompt: str,
        system_message: str = "You are a helpful assistant.",
        **kwargs,
    ) -> Optional[str]:
        """
        Get a text completion from OpenAI.

        Args:
            prompt: User prompt
            system_message: System message for the assistant
            **kwargs: Additional arguments for the API call

        Returns:
            Optional[str]: Response content or None if failed
        """
        try:
            messages: List[ChatCompletionMessageParam] = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ]

            response = await self._make_request_with_retry(messages, **kwargs)
            logger.info("Successfully received completion response")
            return response

        except Exception as e:
            logger.error(f"Failed to get completion: {type(e).__name__}: {e}")
            return None

    async def get_json_completion(
        self,
        prompt: str,
        system_message: str = "You are a helpful assistant. Respond with valid JSON.",
        validate_json: bool = True,
        **kwargs,
    ) -> Optional[str]:
        """
        Get a JSON-formatted completion from OpenAI.

        Args:
            prompt: User prompt
            system_message: System message for the assistant
            validate_json: Whether to validate the JSON response
            **kwargs: Additional arguments for the API call

        Returns:
            Optional[str]: JSON response content or None if failed
        """
        try:
            # Enhance system message for JSON responses
            if "json" not in system_message.lower():
                system_message += (
                    " You must respond with valid JSON only. No markdown formatting."
                )

            # Enhance prompt for JSON responses
            enhanced_prompt = (
                f"{prompt} "
                f"Respond with a properly formatted JSON object only. "
                f"Do not include any text before or after the JSON. "
                f"Do not use markdown code blocks."
            )

            messages: List[ChatCompletionMessageParam] = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": enhanced_prompt},
            ]

            response = await self._make_request_with_retry(messages, **kwargs)

            # Clean markdown formatting if accidentally included
            cleaned_response = re.sub(r"^```(?:json)?\s*", "", response)
            cleaned_response = re.sub(r"\s*```$", "", cleaned_response)
            cleaned_response = cleaned_response.strip()

            # Validate JSON if requested
            if validate_json:
                try:
                    json.loads(cleaned_response)
                    logger.info("Successfully received and validated JSON response")
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                    return None

            return cleaned_response

        except Exception as e:
            logger.error(f"Failed to get JSON completion: {type(e).__name__}: {e}")
            return None

    async def get_multiple_completions(
        self,
        prompts: List[str],
        system_message: str = "You are a helpful assistant.",
        max_concurrent: int = 5,
        **kwargs,
    ) -> List[Optional[str]]:
        """
        Get multiple completions concurrently with rate limiting.

        Args:
            prompts: List of user prompts
            system_message: System message for the assistant
            max_concurrent: Maximum concurrent requests
            **kwargs: Additional arguments for the API calls

        Returns:
            List[Optional[str]]: List of response contents
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def get_single_completion(prompt: str) -> Optional[str]:
            async with semaphore:
                return await self.get_completion(prompt, system_message, **kwargs)

        logger.info(
            f"Processing {len(prompts)} prompts with max {max_concurrent} concurrent requests"
        )

        tasks = [get_single_completion(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to None
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Task failed with exception: {result}")
                processed_results.append(None)
            else:
                processed_results.append(result)

        return processed_results


# Convenience functions for backward compatibility and ease of use
async def get_async_gpt_response(
    prompt_text: str,
    system_message: str = "You are a helpful assistant.",
    config: Optional[OpenAIConfig] = None,
) -> Optional[str]:
    """
    Convenience function for getting a single completion.

    Args:
        prompt_text: User prompt
        system_message: System message
        config: OpenAI configuration

    Returns:
        Optional[str]: Response content or None if failed
    """
    async with AsyncOpenAIClient(config) as client:
        return await client.get_completion(prompt_text, system_message)


async def get_async_gpt_json_response(
    prompt_text: str,
    system_message: str = "You are a helpful assistant. Respond with valid JSON.",
    config: Optional[OpenAIConfig] = None,
) -> Optional[str]:
    """
    Convenience function for getting a JSON completion.

    Args:
        prompt_text: User prompt
        system_message: System message
        config: OpenAI configuration

    Returns:
        Optional[str]: JSON response content or None if failed
    """
    async with AsyncOpenAIClient(config) as client:
        return await client.get_json_completion(prompt_text, system_message)


# Example usage and testing
async def main():
    """Example usage of the async OpenAI client."""
    try:
        # Initialize config
        config = OpenAIConfig(
            model_name="gpt-4o", max_retries=3, timeout=60.0, temperature=0.1
        )

        # Test basic completion
        print("Testing basic completion...")
        response = await get_async_gpt_response(
            "Explain async programming in Python in 2 sentences.", config=config
        )
        print(f"Response: {response}")

        print("\n" + "=" * 50 + "\n")

        # Test JSON completion
        print("Testing JSON completion...")
        json_response = await get_async_gpt_json_response(
            "List the top 3 programming languages with their key features.",
            "You are a programming expert. Respond with valid JSON that includes the name of each language and at least 2 key features.",
            config=config,
        )
        print(f"JSON Response: {json_response}")

        print("\n" + "=" * 50 + "\n")

        # Test client with context manager
        print("Testing client with context manager...")
        async with AsyncOpenAIClient(config) as client:
            prompts = [
                "What is machine learning?",
                "What is deep learning?",
                "What is neural networks?",
            ]

            results = await client.get_multiple_completions(prompts, max_concurrent=2)
            for i, result in enumerate(results):
                print(f"Response {i + 1}: {result[:100] if result else 'Failed'}...")

    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    asyncio.run(main())
