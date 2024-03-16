import unittest

from search_service.duckduckgo_search import DuckDuckGoSearchClient
from search_service.google_search import GoogleSearchClient


class MyTestCase(unittest.TestCase):
    def test_ddgs(self):
        data = DuckDuckGoSearchClient().search('test')
        print(data)
        self.assertIsNotNone(data)

    def test_google(self):
        data = GoogleSearchClient().search('test')
        print(data)
        self.assertIsNotNone(data)

    def test_search(self):
        from search_service.search_service import SearchService
        data = SearchService().search('test')
        print(data)
        self.assertIsNotNone(data)

if __name__ == '__main__':
    unittest.main()
