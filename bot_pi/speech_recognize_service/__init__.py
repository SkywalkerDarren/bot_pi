from typing import Literal


def get_speech_recognizer(name: Literal["azure", "whisper", "openai"]):
    if name == "azure":
        from speech_recognize_service.azure_speech_recognizer import AzureSpeechRecognizer
        return AzureSpeechRecognizer()
    elif name == "whisper":
        from speech_recognize_service.whisper_speech_recognizer import WhisperSpeechRecognizer
        return WhisperSpeechRecognizer()
    elif name == "openai":
        from speech_recognize_service.openai_speech_recognizer import OpenAISpeechRecognizer
        return OpenAISpeechRecognizer()
    else:
        raise ValueError(f"Speech recognizer {name} not found")
