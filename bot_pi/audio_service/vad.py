import numpy as np
import torch


class VAD:
    def __init__(self):
        self.model, utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            onnx=True
        )

        (
            self.get_speech_timestamps,
            self.save_audio,
            self.read_audio,
            self.VADIterator,
            self.collect_chunks
        ) = utils

        # Taken from utils_vad.py

        # Provided by Alexander Veysov

    @staticmethod
    def int2float(sound):
        abs_max = np.abs(sound).max()
        sound = sound.astype('float32')
        if abs_max > 0:
            sound *= 1 / 32768
        sound = sound.squeeze()  # depends on the use case
        return sound

    def get_vad(self):
        return self.VADIterator(
            self.model,
            threshold=0.5,
            sampling_rate=16000,
            min_silence_duration_ms=3000,
            speech_pad_ms=30
        )
