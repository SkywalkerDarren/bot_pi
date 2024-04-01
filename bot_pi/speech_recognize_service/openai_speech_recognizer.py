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
        self.vad = VAD()

    def speech_to_text(self):
        mic = self.am.get_mic_stream()
        mem_file = io.BytesIO()
        print('recording started')

        with mic as recorder:
            with wave.open(mem_file, 'wb') as f:
                f.setnchannels(recorder.channels)
                f.setsampwidth(recorder.width)
                f.setframerate(recorder.rate)

                last_state_activity = False  # 上一次的状态，默认为静音
                self.vad.reset_states()

                while True:
                    wav = recorder.read()
                    f.writeframes(wav)
                    chunk = recorder.chunk
                    self.vad(wav, chunk)
                    is_activity = self.vad.is_activity()
                    if is_activity:
                        print('activity')
                        last_state_activity = True  # 如果检测到活动，更新状态为活动
                    else:
                        print('silence')
                        if last_state_activity:  # 如果上一次是活动而这一次是静音，表示发生了状态变化
                            print('Ending recording due to transition from activity to silence.')
                            break  # 结束录制
                        last_state_activity = False  # 更新状态为静音

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
