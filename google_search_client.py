import aiohttp
# import asyncio
import json
from typing import Any
from config import settings

SERPER_API_KEY = settings.SERPER_API_KEY


async def serper_search(
    q: str,
    num: int = 3,
    page: int = 1,
    # gl: str | None = None,
    # location: str | None = None,
    # hl: str | None = None,
    # tbs: str | None = None,
    # autocorrect: bool | None = None,
    # batch: list | None = None,
) -> Any:
    """
    Perform a search using Serper API (async).
    Parameters:
      q (str): Query string (mandatory)
      gl (str): Country code (e.g., 'us')
      location (str): Location
      hl (str): Language code (e.g., 'en')
      tbs (str): Date range
      autocorrect (bool): Autocorrect
      num (int): Number of results (default: 3)
      page (int): Page number (default: 1)
      batch (list): Mini-batch of queries (up to 100)
    """
    url = "https://google.serper.dev/search"
    payload_dict = {
        "q": q,
        "num": num,
        "page": page,
        # "gl": gl,
        # "location": location,
        # "hl": hl,
        # "tbs": tbs,
        # "autocorrect": autocorrect,
        # "batch": batch,
    }

    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=url, headers=headers, data=json.dumps(obj=payload_dict)
        ) as response:
            result = await response.json()
            return result.get("organic", [])


# # Example usage:
# if __name__ == "__main__":

#     async def main() -> None:
#         result = await serper_search(
#             q="Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?"
#         )
#         print(json.dumps(result, indent=2))

#     asyncio.run(main())