from pydantic import BaseModel

from search_service.search_service import SearchService
from chat_service.base_tool import BaseTool


class SearchEngineTool(BaseTool):
    class SearchEngineParams(BaseModel):
        """
        搜索关键词
        """
        keyword: str

    def __init__(self):
        self.search_client = SearchService()
        super().__init__("search_engine", "使用搜索引擎搜索关键词，搜索时建议使用中文", self.SearchEngineParams)

    def run(self, validated_params: SearchEngineParams):
        keyword = validated_params.keyword
        result = self.search_client.search(keyword)
        if not result:
            return "搜索失败"
        else:
            return result
