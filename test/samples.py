import os
import time

import numpy as np
import pyaudio
from openwakeword import Model
from whispercpp import api, Whisper

from config import PROJECT_ROOT, CONFIG, MODELS_PATH
import azure.cognitiveservices.speech as speechsdk


def azure_keyword_recognition():
    speech_key = CONFIG["key"]
    service_region = CONFIG["region"]

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = "zh-CN"
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"

    model = speechsdk.KeywordRecognitionModel(f"{MODELS_PATH}/hey_bot_pi.table")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        print('KW CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print('KW RECOGNIZED KEYWORD: {}'.format(evt))
            speech_recognizer.stop_keyword_recognition()
        elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print('KW RECOGNIZED: {}'.format(evt))
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print('KW NOMATCH: {}'.format(evt))

    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: print('KW SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('KW SESSION STOPPED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_keyword_recognition(model)
    print('Detecting keyword...')
    while not done:
        time.sleep(.5)

    speech_recognizer.recognized.disconnect_all()
    speech_recognizer.session_started.disconnect_all()
    speech_recognizer.session_stopped.disconnect_all()
    speech_recognizer.canceled.disconnect_all()


def run():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1280
    audio = pyaudio.PyAudio()

    owwModel = Model(inference_framework='tflite',
                     wakeword_models=[f"{os.path.dirname(__file__)}/../models/heyy_ro_bot_pai_40000.tflite"])

    n_models = len(owwModel.models.keys())
    #
    # Generate output string header
    print("\n\n")
    print("#" * 100)
    print("Listening for wakewords...")
    print("#" * 100)
    print("\n" * (n_models * 3))

    mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    while True:
        # Get audio
        audio = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)

        # Feed to openWakeWord model
        prediction = owwModel.predict(audio)
        for k, v in prediction.items():
            if v > 0.4:
                print(f"嘿 我听到了 当前置信度：{v}")


def whisper_run():
    params = (  # noqa # type: ignore
        api.Params.from_enum(api.SAMPLING_GREEDY)
        .with_language("zh")
        .with_print_progress(False)
        .with_print_realtime(False)
        .build()
    )
    print(params)
    # ctx = api.Context.from_file(f"{PROJECT_ROOT}/models/tiny.en.bin")
    w = Whisper.from_params(f"{PROJECT_ROOT}/models/whisper/ggml-base.bin", params)
    result = w.stream_transcribe()
    for r in result:
        print(r)


def pyaudio_play():
    import pyaudio
    import wave

    # WAV文件的路径
    filename = '/data/output.wav'

    # 定义块大小
    chunk = 1024

    # 打开WAV文件
    wf = wave.open(filename, 'rb')

    # 创建PyAudio对象
    p = pyaudio.PyAudio()
    print(wf.getnchannels(), wf.getsampwidth(), wf.getframerate())

    # 打开流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),  # 根据wav文件的宽度设置格式
                    channels=wf.getnchannels(),  # 设置通道数
                    rate=wf.getframerate(),  # 设置帧率
                    output=True)  # 设置为输出

    # 读取数据
    data = wf.readframes(chunk)

    # 播放
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    # 停止流
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()

    # 关闭WAV文件
    wf.close()
