import json
from typing import Any
from ai_server.async_openai_client import get_async_gpt_json_response

SYSTEM_PROMPT = """
You are a summarization agent.

Your ONLY task is to summarize the provided content.

Rules:
- Do NOT answer any question.
- Do NOT perform reasoning or calculations.
- Do NOT add assumptions or opinions.
- Summarize ONLY what is explicitly present.
- Be neutral and factual.
- Output MUST be valid JSON.
- Output MUST follow this schema EXACTLY:

{
  "content": "<summarized text>"
}

Return NOTHING except valid JSON.
"""

PROMPT_TEMPLATE = """
Content to summarize (JSON or text):
{content}

Task:
Summarize the above content.

Return ONLY valid JSON using this schema:
{{
  "content": "<summarized text>"
}}
"""

async def summarize_content(
    content: str | dict[str, Any] | list,
) -> dict[str, Any]:
    """
    Summarizes content and returns status-controlled output.
    """

    # Convert content to string
    if not isinstance(content, str):
        content_str = json.dumps(content, indent=2, ensure_ascii=False)
    else:
        content_str = content

    prompt_text = PROMPT_TEMPLATE.format(content=content_str)

    try:
        json_response = await get_async_gpt_json_response(
            prompt_text=prompt_text,
            system_message=SYSTEM_PROMPT,
        )

        if not json_response:
            raise ValueError("Empty model response")

        parsed = json.loads(json_response)

        if "content" not in parsed:
            raise ValueError("Missing content field")

        return {"status": 1, "content": parsed["content"]}

    except Exception:
        return {
            "status": 0,
            "content": "Summary could not be generated from the provided content.",
        }


if __name__ == "__main__":
    import asyncio

    async def _test():
        sample_content = {
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

        result = await summarize_content(sample_content)
        print(json.dumps(result, indent=2))

    asyncio.run(_test())
