from chat_service.tools.ai_tools import BaseTool


class LLMEngine:

    def __init__(self):
        self.tools = []

    def system_prompt(self):
        pass

    def add_tool(self, tool: BaseTool):
        self.tools.append(tool)

    def chat(self, message):
        pass
