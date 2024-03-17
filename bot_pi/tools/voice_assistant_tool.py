from chat_service.base_tool import BaseTool
from voice_assistant_service.voice_assistant import VoiceAssistantController


class ContinueChatTool(BaseTool):
    def __init__(self, voice_assistant_controller: VoiceAssistantController):
        self.voice_assistant_controller = voice_assistant_controller
        super().__init__("continue_chat", "保持会话，继续聊天，向用户询问以获取更多信息")

    def run(self, validated_params):
        self.voice_assistant_controller.need_continue_chat()
        return "已开启继续聊天模式"
