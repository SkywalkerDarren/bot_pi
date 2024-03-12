import os

from openwakeword import Model

from audio_manager import AudioManager
from config import MODELS_PATH, CONFIG


class KeywordRecognizer:

    def recognize(self):
        ...


class OpenWakeupWordRecognizer(KeywordRecognizer):
    def __init__(self):
        print('Initializing OpenWakeupWordRecognizer...')
        print(CONFIG.open_wakeup_word.model_type)
        self.oww_model = Model(
            inference_framework=CONFIG.open_wakeup_word.model_type,
            wakeword_models=[os.path.join(MODELS_PATH, CONFIG.open_wakeup_word.model_name)]
        )
        self.am = AudioManager()
        self.threshold = CONFIG.open_wakeup_word.sensitivity

    def recognize(self):
        print('Listening for keyword...')
        with self.am.get_mic_stream() as mic_stream:
            detected = False
            while not detected:
                # Get audio
                audio = mic_stream.read()

                # Feed to openWakeWord model
                prediction = self.oww_model.predict(audio)

                for k, v in prediction.items():
                    if v > self.threshold:
                        print(f"嘿 我听到了 当前置信度：{v}")
                        detected = True
        self.oww_model.reset()
        print('Keyword detected, please speak')
