# tools.py
from agents import function_tool
import requests
from bs4 import BeautifulSoup


@function_tool
def search_web(query: str) -> str:
    """Search DuckDuckGo and return top snippets."""
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for a in soup.select('.result__snippet'):
        text = a.get_text(strip=True)
        if text:
            results.append(text)
        if len(results) >= 5:
            break

    return "\n".join(results)

@function_tool
def extract_factual_claims(text: str) -> list[str]:
    # For demo purposes, use a mock implementation
    return [line for line in text.split('.') if line.strip() and "the" in line]

@function_tool
def fact_check_claim(claim: str) -> str:
    return f"The claim '{claim}' appears valid based on available information."

@function_tool
def append_fact_check_summary(original: str, fact_checks: list[str]) -> str:
    summary = "\n\n---\nFACT CHECK SUMMARY:\n" + "\n".join(fact_checks)
    return original + summary
