# import asyncio
# import json
from google_search_client import serper_search
from web_content_fetcher import fetch_all
from html_text_parser import parse_all


async def search_scrap_enrich(query: str) -> list[dict]:
    organic_list = await serper_search(q=query)
    # Step 1: Extract URLs
    urls = [item.get("link") for item in organic_list if item.get("link")]

    if not urls:
        return organic_list

    # Step 2: Fetch HTMLs (maintains order)
    html_list: list[str | None] = await fetch_all(urls=urls)

    # Step 3: Parse HTMLs into clean text
    scraped_text_list: list[str | None] = parse_all(html_list=html_list)

    # Step 4: Attach scraped text back
    for item, scraped_text in zip(organic_list, scraped_text_list):
        item["scraped_data"] = scraped_text

    return organic_list


# # Example usage
# if __name__ == "__main__":
#     async def _test():
#         query = """Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?"""
#         results = await search_scrap_enrich(query)
#         print(json.dumps(results, indent=2))

#     asyncio.run(_test())