from bs4 import BeautifulSoup


def parse_html(html: str) -> str | None:
    """
    Extract only clean text from HTML.
    - Removes scripts, styles, and tags
    - Collapses multiple whitespaces
    - Returns None if parsing fails or no text
    """
    try:
        soup = BeautifulSoup(markup=html, features="html.parser")

        # Remove script and style elements
        for script_or_style in soup(name=["script", "style"]):
            script_or_style.decompose()

        # Get visible text
        text = soup.get_text(separator=" ", strip=True)

        # Collapse multiple whitespaces into single space
        clean_text = " ".join(text.split())

        return clean_text if clean_text else None

    except Exception:
        return None


def parse_all(html_list: list[str | None]) -> list[str | None]:
    """
    Parse a list of HTML content to clean text.
    Maintains order. If HTML is None, parsed data is None.
    """
    return [parse_html(html) if html else None for html in html_list]