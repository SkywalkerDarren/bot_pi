from chat_manager import ChatManager
from keyword_recognizer import OpenWakeupWordRecognizer
from speech_recognizer import SpeechRecognizer
from speech_synthesizer import SpeechSynthesizer


def voice_assistant():
    kr = OpenWakeupWordRecognizer()
    sr = SpeechRecognizer()
    ss = SpeechSynthesizer()
    cm = ChatManager()
    while True:
        try:
            kr.recognize()

            speech_list = sr.speech_to_text()

            if not speech_list:
                print('没有听到，请再说一遍')
                continue

            user_speech = ''.join(speech_list)

            content = cm.chat(user_speech)

            print(f"ai: {content}")

            ss.text_to_speech(content)
        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    voice_assistant()
