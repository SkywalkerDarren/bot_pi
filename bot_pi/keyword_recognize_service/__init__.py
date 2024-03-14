from typing import Literal


def get_keyword_recognizer(name: Literal["open_wakeup_word"]):
    if name == "open_wakeup_word":
        from keyword_recognize_service.open_wakeup_word_recognizer import OpenWakeupWordRecognizer
        return OpenWakeupWordRecognizer()
    else:
        raise ValueError(f"Unknown keyword recognizer: {name}")
