from pydantic import BaseModel

from chat_service.ai_tools import BaseTool
from search_service.search_service import SearchService


class SearchEngineTool(BaseTool):
    class SearchEngineParams(BaseModel):
        """
        搜索关键词
        """
        keyword: str

    def __init__(self, search_client: SearchService):
        self.search_client = search_client
        super().__init__("search_engine", "使用搜索引擎搜索关键词，搜索时建议使用中文", self.SearchEngineParams)

    def run(self, validated_params: SearchEngineParams):
        keyword = validated_params.keyword
        result = self.search_client.search(keyword)
        if not result:
            return "搜索失败"
        else:
            return result
