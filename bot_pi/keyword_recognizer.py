from openwakeword import Model

from audio_manager import AudioManager
from config import MODELS_PATH


class KeywordRecognizer:

    def recognize(self):
        ...


class OpenWakeupWordRecognizer(KeywordRecognizer):
    def __init__(self):
        self.oww_model = Model(
            inference_framework='tflite',
            wakeword_models=[f"{MODELS_PATH}/heyy_ro_bot_pai_40000.tflite"]
        )
        self.am = AudioManager()
        self.threshold = 0.5

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
