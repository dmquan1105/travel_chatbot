from langchain_community.tools.tavily_search.tool import TavilySearchResults
from dotenv import load_dotenv
from langchain.tools import tool
from typing import List, Dict
import json

load_dotenv(override=True)


@tool("web_search")
def web_search(query: str) -> List[Dict[str, str]]:
    """Searches for information from the web using Tavily.

    Args:
        query (str): The user's query.

    Returns:
        List[Dict[str, str]]: A list of search result dictionaries with title, url, and content.
    """
    search = TavilySearchResults()
    results = search.run(query)

    if not results:
        return []

    formatted_results = []
    for res in results[:3]:
        formatted_results.append(
            {
                "title": res.get("title", ""),
                "url": res.get("url", ""),
                "content": res.get("content", ""),
            }
        )

    return formatted_results


def main():
    print("\nKết quả JSON từ tool `web_search`:\n")
    result = web_search.invoke("Đền Trần Thái Bình")
    print(
        json.dumps(result, ensure_ascii=False, indent=2)
    )  # In đẹp JSON, hỗ trợ tiếng Việt


if __name__ == "__main__":
    main()
