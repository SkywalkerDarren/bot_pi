import io
import wave

import numpy as np
from whispercpp import api, Whisper

from audio_service.audio_manager import AudioManager
from audio_service.vad import VAD
from config import PROJECT_ROOT
from speech_recognize_service.speech_recognizer import SpeechRecognizer


class WhisperSpeechRecognizer(SpeechRecognizer):

    def __init__(self):
        self.am = AudioManager()
        self.vad = VAD().get_vad()
        self.i2f = VAD.int2float
        params = (  # noqa # type: ignore
            api.Params.from_enum(api.SAMPLING_GREEDY)
            .with_language("zh")
            .with_print_progress(False)
            .with_print_realtime(False)
            .build()
        )
        print(params)
        # ctx = api.Context.from_file(f"{PROJECT_ROOT}/models/tiny.en.bin")
        self.w = Whisper.from_params(f"{PROJECT_ROOT}/models/whisper/ggml-tiny.bin", params)

    def speech_to_text(self):
        mic = self.am.get_mic_stream()
        mem_file = io.BytesIO()
        print('recording started')

        with mic as recorder:
            with wave.open(mem_file, 'wb') as f:
                f.setnchannels(recorder.channels)
                f.setsampwidth(recorder.width)
                f.setframerate(recorder.rate)

                while True:
                    wav_int16 = recorder.read()
                    f.writeframes(wav_int16)
                    wav_float32 = self.i2f(wav_int16)
                    result = self.vad(wav_float32)
                    if result and 'end' in result:
                        break

        print('recording done')
        mem_file.seek(0)  # 重置内存文件的指针到开始位置

        with wave.open(mem_file, 'rb') as wav:
            wav: wave.Wave_read
            data_np = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)
            wav_float32 = self.i2f(data_np)
            t = self.w.transcribe(wav_float32)
            print(t)
        return t
