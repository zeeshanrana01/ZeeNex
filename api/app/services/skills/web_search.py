from app.services.skills import skill
import urllib.parse
import httpx

@skill(
    name="web_search",
    description="Search the web for current information on a topic",
    parameters={
        "query": {
            "type": "string",
            "description": "The search query"
        }
    }
)
def web_search(query: str) -> str:
    # We'll use a simple DuckDuckGo HTML scrape as a zero-config search implementation
    # This avoids the need for API keys while providing real results

    encoded_query = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

    try:
        with httpx.Client(headers={"User-Agent": "Mozilla/5.0"}, timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()

            # Basic parsing of DDG HTML results
            # We look for the 'result__a' class which contains the main links/titles
            import re
            results = re.findall(r'<a class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>', response.text)

            if not results:
                return f"No search results found for '{query}'."

            formatted_results = []
            for link, title in results[:5]:
                formatted_results.append(f"- {title}: {link}")

            return "Search results for '" + query + "':\n" + "\n".join(formatted_results)

    except Exception as e:
        return f"Web search failed for '{query}': {str(e)}"
