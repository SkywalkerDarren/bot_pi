import unittest
from typing import Optional

from pydantic import BaseModel

from chat_service.llm.claude_engine import ClaudeEngine
from chat_service.llm.openai_engine import OpenAIEngine
from tools import BaseTool
from tools.search_engine_tool import SearchEngineTool


class TestTool(BaseTool):
    class TestParams(BaseModel):
        """
        一个参数，可以是任意字符串
        """
        param: str

    def __init__(self):
        super().__init__("test_tool", "测试工具，用来测试能否正常工作", self.TestParams)

    def run(self, validated_params: Optional[BaseModel]) -> str:
        param = validated_params.param
        return f"测试工具正常工作，参数是：{param}"


class FakeSearchEngineTool(SearchEngineTool):
    def run(self, validated_params):
        return "网络异常，搜索失败"


class MyTestCase(unittest.TestCase):
    def test_claude_tool(self):
        engine = ClaudeEngine()
        engine.add_tool(TestTool())
        engine.add_tool(FakeSearchEngineTool())
        text = engine.chat("查下树莓派的文档的地址")
        print(text)
        text = engine.chat("测试工具")
        print(text)

    def test_claude_text(self):
        engine = ClaudeEngine()
        text = engine.chat("介绍你自己")
        print(text)

    def test_openai_tool(self):
        engine = OpenAIEngine()
        engine.add_tool(TestTool())
        engine.add_tool(FakeSearchEngineTool())
        text = engine.chat("查下树莓派的文档的地址")
        print(text)
        text = engine.chat("测试工具")
        print(text)

    def test_bootstrapping(self):
        # engine = ClaudeEngine()
        engine = OpenAIEngine()
        engine.add_tool(TestTool())
        text = engine.chat("测试，连续使用3次测试工具，每次只能调用1个工具")
        print(text)

    def test_openai_text(self):
        engine = OpenAIEngine()
        text = engine.chat("介绍你自己")
        print(text)


if __name__ == '__main__':
    unittest.main()
