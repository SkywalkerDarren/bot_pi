from chat_service.llm.llm_engine import LLMEngine
from tools.clean_history_tool import CleanHistoryTool


class ChatManager:
    def __init__(self, engine: LLMEngine):
        engine.add_tool(CleanHistoryTool(self.clean_history))
        self.ai = engine
        self.history = []

    def clean_history(self):
        self.history = []

    def chat(self, message):
        content, history = self.ai.chat(message, self.history)
        self.history = history
        return content

    def check_is_end(self, user: str, assistant: str):
        msg = (
            f"以下是对话的最后部分，根据对话，判断这通聊天是否结束，如果需要继续聊天就使用‘继续聊天工具’开启继续聊天，否则返回DONE：\n"
            f"user: {user}\nassistant: {assistant}")
        print(msg)

        self.ai.chat(msg, [])
