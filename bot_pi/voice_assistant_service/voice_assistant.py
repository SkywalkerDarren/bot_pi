import time

from chat_service.chat_manager import ChatManager
from chat_service.llm import get_llm
from keyword_recognize_service import get_keyword_recognizer
from keyword_recognize_service.keyword_recognizer import KeywordRecognizer
from speech_recognize_service import get_speech_recognizer
from speech_recognize_service.speech_recognizer import SpeechRecognizer
from speech_synthesize_service import get_speech_synthesizer
from speech_synthesize_service.speech_synthesizer import SpeechSynthesizer
from tools.run_code_tool import RunCodeTool
from tools.search_engine_tool import SearchEngineTool
from voice_assistant_service.voice_assistant_controller import VoiceAssistantController


class VoiceAssistant:
    def __init__(self):
        self.keyword_recognizer: KeywordRecognizer = get_keyword_recognizer("open_wakeup_word")
        self.speech_recognizer: SpeechRecognizer = get_speech_recognizer("azure")
        self.speech_synthesizer: SpeechSynthesizer = get_speech_synthesizer("azure")
        engine = get_llm("openai")
        engine.add_tool(RunCodeTool())
        engine.add_tool(SearchEngineTool())
        self.voice_assistant_controller = VoiceAssistantController()
        self.chat_manager = ChatManager(engine)

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
                print(e)
                return 1
