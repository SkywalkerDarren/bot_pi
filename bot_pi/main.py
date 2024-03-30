from chat_service.chat_manager import ChatManager
from chat_service.llm import get_llm
from keyword_recognize_service import get_keyword_recognizer
from speech_recognize_service import get_speech_recognizer
from speech_synthesize_service import get_speech_synthesizer
from tools.meeting_tool import StartMeetingTool, StopMeetingTool, GetMeetingContent
from tools.run_code_tool import RunCodeTool
from tools.search_engine_tool import SearchEngineTool
from tools.voice_assistant_tool import ContinueChatTool
from voice_assistant_service.voice_assistant import VoiceAssistant
from voice_assistant_service.voice_assistant_controller import VoiceAssistantController


def run():
    keyword_recognizer = get_keyword_recognizer("open_wakeup_word")
    speech_recognizer = get_speech_recognizer("azure")
    speech_synthesizer = get_speech_synthesizer("azure")
    voice_assistant_controller = VoiceAssistantController()
    engine = get_llm("openai")
    engine.add_tool(RunCodeTool())
    engine.add_tool(SearchEngineTool())
    engine.add_tool(ContinueChatTool(voice_assistant_controller))
    engine.add_tool(StartMeetingTool())
    engine.add_tool(StopMeetingTool())
    engine.add_tool(GetMeetingContent())
    chat_manager = ChatManager(engine)
    voice_assistant = VoiceAssistant(
        keyword_recognizer,
        speech_recognizer,
        speech_synthesizer,
        voice_assistant_controller,
        chat_manager
    )
    status = voice_assistant.run()
    if status != 0:
        print("Voice assistant stopped with error.")


if __name__ == "__main__":
    run()
