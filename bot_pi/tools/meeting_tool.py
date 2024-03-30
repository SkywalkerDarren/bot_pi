from typing import Optional

from anthropic import BaseModel

from audio_service.audio_manager import AudioManager
from chat_service.base_tool import BaseTool


class MeetingTranscribe:
    in_use = False

    def __init__(self):
        self._am = AudioManager()
        from speech_recognize_service.azure_speech_recognizer import AzureSpeechRecognizer
        self._transcriber = AzureSpeechRecognizer()
        self._real_time_content = []
        self._transcriber.set_text_yield(lambda text: self._real_time_content.append(text))

    @property
    def content(self) -> str:
        return '\n'.join(self._real_time_content)

    def start_transcribe(self):
        self._transcriber.start_transcribe()
        self.in_use = True

    def stop_transcribe(self):
        self._transcriber.stop_transcribe()
        self.in_use = False


_transcriber: Optional[MeetingTranscribe] = None


class StartMeetingTool(BaseTool):
    def __init__(self):
        global _transcriber
        if _transcriber is None:
            _transcriber = MeetingTranscribe()
        super().__init__("start_meeting_transcription", "开启实时会议转写功能")

    def run(self, validated_params: Optional[BaseModel]) -> str:
        global _transcriber
        if _transcriber is not None:
            _transcriber.start_transcribe()
            return "实时会议转写功能已开启"
        else:
            return "实时会议转写功能开启失败"


class StopMeetingTool(BaseTool):
    def __init__(self):
        global _transcriber
        if _transcriber is None:
            _transcriber = MeetingTranscribe()
        super().__init__("stop_meeting_transcription", "关闭实时会议转写功能")

    def run(self, validated_params: Optional[BaseModel]) -> str:
        global _transcriber
        if _transcriber is not None and _transcriber.in_use:
            _transcriber.stop_transcribe()
            return "实时会议转写功能已关闭"
        else:
            return "实时会议转写功能关闭失败"


class GetMeetingContent(BaseTool):

    def __init__(self):
        global _transcriber
        if _transcriber is None:
            _transcriber = MeetingTranscribe()
        super().__init__("get_meeting_content", "获取实时会议转写内容")

    def run(self, validated_params: Optional[BaseModel]) -> str:
        global _transcriber
        if _transcriber is not None:
            return _transcriber.content
        else:
            return "获取实时会议转写内容失败"
