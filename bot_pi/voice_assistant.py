import time

from chat_manager import ChatManager
from keyword_recognizer import OpenWakeupWordRecognizer
from speech_recognizer import SpeechRecognizer
from speech_synthesizer import SpeechSynthesizer


class VoiceAssistant:
    def __init__(self):
        self.keyword_recognizer = OpenWakeupWordRecognizer()
        self.speech_recognizer = SpeechRecognizer()
        self.speech_synthesizer = SpeechSynthesizer()
        self.chat_manager = ChatManager()

    def work(self):
        self.keyword_recognizer.recognize()

        t1 = time.time()
        speech_list = self.speech_recognizer.speech_to_text()
        t2 = time.time()
        print(f"stt耗时：{t2-t1}s")

        if not speech_list:
            user_speech = '没有听到，请再说一遍'
        else:
            user_speech = ''.join(speech_list)

        t3 = time.time()
        content = self.chat_manager.chat(user_speech)
        t4 = time.time()
        print(f"chat耗时：{t4-t3}s")

        t5 = time.time()
        self.speech_synthesizer.text_to_speech(content)
        t6 = time.time()
        print(f"tts耗时：{t6-t5}s")

    def run(self) -> int:
        while True:
            try:
                self.work()
            except Exception as e:
                print(e)
                return 1
