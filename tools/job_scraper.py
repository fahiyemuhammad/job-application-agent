import requests
from bs4 import BeautifulSoup
import re


def _clean_text(text: str) -> str:
    """Remove excessive whitespace and blank lines."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def scrape_job_posting(url: str, max_chars: int = 8000) -> dict:
    """
    Scrapes job posting or company website content from a URL.
    Extracts all meaningful text — not just <p> tags.
    Falls back gracefully on errors.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "meta", "noscript"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title else "Unknown Title"

        job_containers = soup.find_all(
            attrs={
                "class": re.compile(
                    r"job|description|posting|career|position|vacancy|role|listing",
                    re.I,
                )
            }
        )

        if job_containers:
            raw = " ".join(c.get_text(separator="\n") for c in job_containers)
        else:
            tags = soup.find_all(["p", "li", "h1", "h2", "h3", "h4", "span", "div"])
            raw = "\n".join(t.get_text(separator=" ") for t in tags)

        description = _clean_text(raw)[:max_chars]

        if len(description) < 100:
            description = _clean_text(soup.get_text(separator="\n"))[:max_chars]

        return {
            "job_title": title,
            "job_description": description,
        }

    except Exception as e:
        return {
            "job_title": "",
            "job_description": "",
            "error": str(e),
        }