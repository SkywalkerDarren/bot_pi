class VoiceAssistantController:
    def __init__(self):
        self._can_continue_chat = False

    def reset_continue_chat(self):
        self._can_continue_chat = False

    def can_continue_chat(self) -> bool:
        return self._can_continue_chat

    def need_continue_chat(self):
        self._can_continue_chat = True
