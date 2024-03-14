from chat_service.ai_tools import BaseTool


class CleanHistoryTool(BaseTool):
    def __init__(self, history_cleaner):
        self.history_cleaner = history_cleaner
        super().__init__("clean_history", "清除聊天历史记录")

    def run(self, validated_params):
        self.history_cleaner()
        return "历史记录已清空"
