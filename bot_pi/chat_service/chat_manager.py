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
        return self.ai.chat(message)
