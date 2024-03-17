import io
import wave

import openai

from audio_service.audio_manager import AudioManager
from audio_service.vad import VAD
from config import CONFIG
from speech_recognize_service.speech_recognizer import SpeechRecognizer


class OpenAISpeechRecognizer(SpeechRecognizer):

    def __init__(self):
        self.openai_api_key = CONFIG.openai.key
        self.open_ai = openai.OpenAI(api_key=self.openai_api_key)
        self.am = AudioManager()
        self.vad = VAD().get_vad()
        self.i2f = VAD.int2float

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

        # 使用内存中的数据而不是从磁盘文件读取
        transcription = self.open_ai.audio.transcriptions.create(
            file=("temp.wav", mem_file),
            model="whisper-1",
            response_format='text',
            language='zh'
        )
        return transcription
