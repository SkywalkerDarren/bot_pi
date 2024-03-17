import openai

from audio_service.audio_manager import AudioManager
from config import CONFIG
from speech_synthesize_service.speech_synthesizer import SpeechSynthesizer


class OpenAISpeechSynthesizer(SpeechSynthesizer):
    def __init__(self):
        self.openai_api_key = CONFIG.openai.key
        self.tts_model = CONFIG.openai.tts_model
        self.voice = CONFIG.openai.voice
        self.open_ai = openai.OpenAI(api_key=self.openai_api_key)
        am = AudioManager()
        self._stream = am.get_spk_stream(
            rate=24000,
            channels=1,
            width=2
        )

    def text_to_speech(self, contents):
        response = self.open_ai.audio.speech.create(
            input=contents,
            model=self.tts_model,
            voice=self.voice,
            response_format="pcm",
        )

        with self._stream as stream:
            for chunk in response.iter_bytes():
                if chunk:
                    stream.write(chunk)
