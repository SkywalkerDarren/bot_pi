from search_service.duckduckgo_search import DuckDuckGoSearchClient
from search_service.google_search import GoogleSearchClient


class SearchService:

    def __init__(self):
        self.clients = [
            GoogleSearchClient(),
            DuckDuckGoSearchClient(),
        ]

    def search(self, query: str) -> str:
        for client in self.clients:
            try:
                result = client.search(query)
                if result:
                    return result
            except Exception as e:
                print(f"Error: {e}")
        else:
            return "No result found"
