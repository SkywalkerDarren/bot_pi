import os
import time
import traceback
import wave

from audio_service.audio_manager import AudioManager
from chat_service.chat_manager import ChatManager
from config import ASSETS_PATH
from keyword_recognize_service.keyword_recognizer import KeywordRecognizer
from speech_recognize_service.speech_recognizer import SpeechRecognizer
from speech_synthesize_service.speech_synthesizer import SpeechSynthesizer
from voice_assistant_service.voice_assistant_controller import VoiceAssistantController


class VoiceAssistant:
    def __init__(
            self,
            keyword_recognizer: KeywordRecognizer,
            speech_recognizer: SpeechRecognizer,
            speech_synthesizer: SpeechSynthesizer,
            voice_assistant_controller: VoiceAssistantController,
            chat_manager: ChatManager
    ):
        self.keyword_recognizer = keyword_recognizer
        self.speech_recognizer = speech_recognizer
        self.speech_synthesizer = speech_synthesizer
        self.voice_assistant_controller = voice_assistant_controller
        self.chat_manager = chat_manager
        self._am = AudioManager()

    def play_notify_sound(self):
        with wave.open(os.path.join(ASSETS_PATH, "notify.wav")) as wav:
            spk = self._am.get_spk_stream(
                rate=wav.getframerate(),
                channels=wav.getnchannels(),
                width=wav.getsampwidth()
            )
            with spk as speaker:
                print('speaking')
                speaker.write(wav.readframes(wav.getnframes()))
            print('speaking done')

    def work(self):
        if not self.voice_assistant_controller.can_continue_chat():
            self.keyword_recognizer.recognize()
        else:
            self.voice_assistant_controller.reset_continue_chat()

        self.play_notify_sound()

        try:
            t1 = time.time()
            speech = self.speech_recognizer.speech_to_text()
            t2 = time.time()
            print(f"stt耗时：{t2 - t1}s")
        except Exception as e:
            traceback.print_exc()
            print(e)
            return

        if not speech:
            return

        try:
            t3 = time.time()
            content = self.chat_manager.chat(speech)
            self.chat_manager.check_is_end(speech, content)
            t4 = time.time()
            print(f"chat耗时：{t4 - t3}s")
        except Exception as e:
            traceback.print_exc()
            print(e)
            content = "对话出错了"

        try:
            t5 = time.time()
            self.speech_synthesizer.text_to_speech(content)
            t6 = time.time()
            print(f"tts耗时：{t6 - t5}s")
        except Exception as e:
            traceback.print_exc()
            print(e)

    def run(self) -> int:
        self.play_notify_sound()
        while True:
            try:
                self.work()
            except Exception as e:
                traceback.print_exc()
                print(e)
                return 1
