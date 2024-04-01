import threading

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioConfig
from azure.cognitiveservices.speech.audio import AudioStreamFormat

from audio_service.audio_manager import AudioManager
from audio_service.vad import VAD
from config import CONFIG
from speech_recognize_service.speech_recognizer import SpeechRecognizer


class AzureSpeechRecognizer(SpeechRecognizer):

    def __init__(self):
        speech_key = CONFIG.azure_speech.key
        service_region = CONFIG.azure_speech.region
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_recognition_language = CONFIG.azure_speech.recognition_language
        self._speech_config = speech_config
        self._am = AudioManager()
        self._mic_stream = self._am.get_mic_stream()
        self._vad = VAD()
        self._text_yield = None
        self.speech_recognizer = None
        self.recognition_done = None
        self.push_stream_writer_thread = None
        self.push_flag = False

    def push_stream_writer(self, stream, manual_control):
        mic_stream = self._mic_stream

        with mic_stream as mic:
            self._vad.reset_states()
            while True:
                data = mic.read()
                frame = data.tobytes()
                # print('read {} bytes'.format(len(frame)))
                stream.write(frame)
                if not manual_control:
                    chunk = mic.chunk
                    self._vad(data, chunk)
                    is_activity = self._vad.is_activity()
                    if is_activity:
                        print('activity')
                        last_state_activity = True  # 如果检测到活动，更新状态为活动
                    else:
                        print('silence')
                        if last_state_activity:  # 如果上一次是活动而这一次是静音，表示发生了状态变化
                            print('Ending recording due to transition from activity to silence.')
                            break  # 结束录制
                        last_state_activity = False  # 更新状态为静音
                else:
                    if not self.push_flag:
                        break
        stream.close()

    def set_text_yield(self, text_yield):
        self._text_yield = text_yield

    def start_transcribe(self):
        self.recognition_done = threading.Event()
        self.push_flag = True
        audio_format = AudioStreamFormat(
            samples_per_second=self._mic_stream.rate,
            bits_per_sample=self._mic_stream.width * 8,
            channels=self._mic_stream.channels
        )
        stream = speechsdk.audio.PushAudioInputStream(audio_format)
        audio_config = AudioConfig(stream=stream)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self._speech_config,
            audio_config=audio_config,
            language='zh-CN'
        )

        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            print(f"RECOGNIZED: {evt}")
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print('SPEECH RECOGNIZED: {}'.format(evt))
                if self._text_yield:
                    self._text_yield(evt.result.text)
            elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                print('SPEECH NOMATCH: {}'.format(evt))

        def canceled_cb(evt: speechsdk.SpeechRecognitionCanceledEventArgs):
            print('CANCELED: {}'.format(evt.cancellation_details))

        def session_stopped_cb(evt):
            print('SESSION STOPPED: {}'.format(evt))
            self.recognition_done.set()

        # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.canceled.connect(canceled_cb)
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(session_stopped_cb)

        # Start push stream writer thread
        self.push_stream_writer_thread = threading.Thread(target=self.push_stream_writer, args=[stream, True])
        self.push_stream_writer_thread.start()

        self.speech_recognizer = speech_recognizer
        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

    def stop_transcribe(self):
        self.push_flag = False
        # Stop recognition and clean up
        self.speech_recognizer.stop_continuous_recognition()
        self.push_stream_writer_thread.join()

        del self.speech_recognizer

    def speech_to_text(self):
        print('AzureSpeechRecognizer.speech_to_text')
        speech_list = []
        recognition_done = threading.Event()

        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            print(f"RECOGNIZED: {evt}")
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print('SPEECH RECOGNIZED: {}'.format(evt))
                speech_list.append(evt.result.text)
                if self._text_yield:
                    self._text_yield(evt.result.text)
            elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                print('SPEECH NOMATCH: {}'.format(evt))

        def canceled_cb(evt: speechsdk.SpeechRecognitionCanceledEventArgs):
            print('CANCELED: {}'.format(evt.cancellation_details))

        def session_stopped_cb(evt):
            print('SESSION STOPPED: {}'.format(evt))
            recognition_done.set()

        audio_format = AudioStreamFormat(
            samples_per_second=self._mic_stream.rate,
            bits_per_sample=self._mic_stream.width * 8,
            channels=self._mic_stream.channels
        )
        stream = speechsdk.audio.PushAudioInputStream(audio_format)
        audio_config = AudioConfig(stream=stream)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self._speech_config,
            audio_config=audio_config,
            language='zh-CN'
        )
        # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.canceled.connect(canceled_cb)
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(session_stopped_cb)

        # Start push stream writer thread
        push_stream_writer_thread = threading.Thread(target=self.push_stream_writer, args=[stream, False])
        push_stream_writer_thread.start()

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        # Wait until all input processed
        recognition_done.wait()

        # Stop recognition and clean up
        speech_recognizer.stop_continuous_recognition()
        push_stream_writer_thread.join()

        del speech_recognizer
        return ''.join(speech_list)
