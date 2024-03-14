import json

from duckduckgo_search import DDGS

from search_service.search_client import SearchClient


class DuckDuckGoSearchClient(SearchClient):
    def search(self, query: str) -> str:
        result = DDGS(proxies=None).text(query, "zh-cn", max_results=10)
        return json.dumps(result, ensure_ascii=False)
