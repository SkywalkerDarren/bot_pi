import os

import openwakeword.utils
import psutil
from openwakeword import Model

from audio_service.audio_manager import AudioManager
from config import CONFIG, MODELS_PATH
from keyword_recognize_service.keyword_recognizer import KeywordRecognizer


class OpenWakeupWordRecognizer(KeywordRecognizer):
    def __init__(self):
        print('Initializing OpenWakeupWordRecognizer...')
        print(CONFIG.open_wakeup_word.model_type)
        openwakeword.utils.download_models(target_directory=MODELS_PATH)
        self.oww_model = Model(
            inference_framework=CONFIG.open_wakeup_word.model_type,
            wakeword_models=[os.path.join(MODELS_PATH, CONFIG.open_wakeup_word.model_name)],
            melspec_model_path=os.path.join(MODELS_PATH, f"melspectrogram.{CONFIG.open_wakeup_word.model_type}"),
            embedding_model_path=os.path.join(MODELS_PATH, f"embedding_model.{CONFIG.open_wakeup_word.model_type}")
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
