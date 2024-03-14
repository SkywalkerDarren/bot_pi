from voice_assistant_service.voice_assistant import VoiceAssistant


def run():
    voice_assistant = VoiceAssistant()
    status = voice_assistant.run()
    if status != 0:
        print("Voice assistant stopped with error.")


if __name__ == "__main__":
    run()
