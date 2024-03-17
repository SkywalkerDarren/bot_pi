import unittest

from chat_service.llm.openai_engine import OpenAIEngine
from tools.run_code_tool import _run_code
from tools.voice_assistant_tool import ContinueChatTool
from voice_assistant_service.voice_assistant_controller import VoiceAssistantController


class MyTestCase(unittest.TestCase):
    def test_run_code(self):
        _run_code('print("hello world")')

    def test_chat_continue(self):
        msg = """以下是对话的最后部分，根据对话，判断这通聊天是否结束，如果聊天需要继续就使用工具开启继续聊天，否则返回DONE：
user: 随便问我一个问题。
assistant: 你今天晚餐吃的是什么呢？"""

        controller = VoiceAssistantController()

        tool = ContinueChatTool(controller)
        engine = OpenAIEngine()
        engine.add_tool(tool)
        text = engine.chat(msg, [])
        print(text)


if __name__ == '__main__':
    unittest.main()
