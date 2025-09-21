import asyncio
import aiohttp
import cloudscraper
from playwright.async_api import async_playwright


async def fetch_aiohttp(url: str, timeout: int = 10) -> str | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    return await response.text()
    except Exception:
        return None
    return None


def fetch_cloudscraper(url: str, timeout: int = 15) -> str | None:
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=timeout)
        if response.status_code == 200:
            return response.text
    except Exception:
        return None
    return None


async def fetch_playwright(url: str, timeout: int = 30) -> str | None:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=timeout * 1000)
            content = await page.content()
            await browser.close()
            return content
    except Exception:
        return None


async def fetch_with_fallback(url: str) -> str | None:
    # Tier 1: aiohttp
    html = await fetch_aiohttp(url)
    if html:
        return html

    # Tier 2: cloudscraper
    loop = asyncio.get_running_loop()
    html = await loop.run_in_executor(None, fetch_cloudscraper, url)
    if html:
        return html

    # Tier 3: Playwright
    html = await fetch_playwright(url)
    return html


async def fetch_all(urls: list[str], max_workers: int = 5) -> list[str | None]:
    sem = asyncio.Semaphore(max_workers)

    async def safe_fetch(url) -> str | None:
        async with sem:
            return await fetch_with_fallback(url)

    tasks = [safe_fetch(url) for url in urls]
    return await asyncio.gather(*tasks)