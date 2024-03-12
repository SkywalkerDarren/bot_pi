import numpy as np
import pyaudio

from config import CONFIG


class MicStream:
    _stream = None

    def __init__(self, p: pyaudio.PyAudio, rate: int, chunk: int, width: int, channels: int):
        self._p = p
        self._rate = rate
        self._chunk = chunk
        self._width = width
        self._channels = channels

    @classmethod
    def in_use(cls):
        return cls._stream is not None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._stream is not None:
            self.close()

    def open(self):
        if self._stream is not None:
            raise ValueError("Stream is already open")
        self._stream = self._p.open(
            format=self._p.get_format_from_width(self._width),
            channels=self._channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
        )

    def read(self) -> np.ndarray:
        return np.frombuffer(self._stream.read(self._chunk), dtype=np.int16)

    def close(self) -> None:
        if self._stream is None:
            raise ValueError("Stream is not open")
        self._stream.stop_stream()
        self._stream.close()
        self._stream = None


class SpkStream:

    def __init__(self, p: pyaudio.PyAudio, rate: int, channels: int, width: int):
        self._p = p
        self._rate = rate
        self._channels = channels
        self._width = width
        self._stream = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._stream is not None:
            self.close()

    def open(self):
        if self._stream is not None:
            raise ValueError("Stream is already open")
        self._stream = self._p.open(
            format=self._p.get_format_from_width(self._width),
            channels=self._channels,
            rate=self._rate,
            output=True
        )

    def write(self, audio: bytes):
        self._stream.write(audio)

    def close(self) -> None:
        if self._stream is None:
            raise ValueError("Stream is not open")
        self._stream.stop_stream()
        self._stream.close()
        del self._stream
        self._stream = None


class AudioManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self._channels = CONFIG.recorder.channels
        self._rate = CONFIG.recorder.sample_rate
        self._chunk = CONFIG.recorder.chunk
        self._width = CONFIG.recorder.width
        self._p = pyaudio.PyAudio()
        self._format = self._p.get_format_from_width(self._width)

    def get_mic_stream(self):
        return MicStream(self._p, self._rate, self._chunk, self._width, self._channels)

    def get_spk_stream(self, rate, channels, width):
        return SpkStream(self._p, rate, channels, width)
