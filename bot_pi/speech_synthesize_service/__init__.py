from typing import Literal


def get_speech_synthesizer(name: Literal["azure", "openai"]):
    if name == "azure":
        from speech_synthesize_service.azure_speech_synthesizer import AzureSpeechSynthesizer
        return AzureSpeechSynthesizer()
    elif name == "openai":
        from speech_synthesize_service.openai_speech_synthesizer import OpenAISpeechSynthesizer
        return OpenAISpeechSynthesizer()
    else:
        raise ValueError(f"Unknown speech recognizer: {name}")
