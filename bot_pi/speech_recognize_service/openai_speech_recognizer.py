import openai

from config import CONFIG
from speech_recognize_service.speech_recognizer import SpeechRecognizer


class OpenAISpeechRecognizer(SpeechRecognizer):

    def __init__(self):
        self.openai_api_key = CONFIG.openai.key
        self.open_ai = openai.OpenAI(api_key=self.openai_api_key)

    def speech_to_text(self):
        transcription = self.open_ai.audio.transcriptions.create(
            model="whisper-1",
            response_format='text',
            language='zh'
        )
        return transcription.text
