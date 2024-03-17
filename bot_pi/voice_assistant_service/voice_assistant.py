import time
import traceback

from chat_service.chat_manager import ChatManager
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

    def work(self):
        if not self.voice_assistant_controller.can_continue_chat():
            self.keyword_recognizer.recognize()
        else:
            self.voice_assistant_controller.reset_continue_chat()

        t1 = time.time()
        speech = self.speech_recognizer.speech_to_text()
        t2 = time.time()
        print(f"stt耗时：{t2 - t1}s")

        if not speech:
            speech = '没有听到，请再说一遍'

        t3 = time.time()
        content = self.chat_manager.chat(speech)
        self.chat_manager.check_is_end(speech, content)
        t4 = time.time()
        print(f"chat耗时：{t4 - t3}s")

        t5 = time.time()
        self.speech_synthesizer.text_to_speech(content)
        t6 = time.time()
        print(f"tts耗时：{t6 - t5}s")

    def run(self) -> int:
        while True:
            try:
                self.work()
            except Exception as e:
                traceback.print_exc()
                print(e)
                return 1
