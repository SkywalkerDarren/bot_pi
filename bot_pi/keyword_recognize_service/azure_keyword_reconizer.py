import time

import azure.cognitiveservices.speech as speechsdk

from config import CONFIG, MODELS_PATH
from keyword_recognize_service.keyword_recognizer import KeywordRecognizer


class AzureKeywordRecognizer(KeywordRecognizer):

    def __init__(self):
        speech_key = CONFIG.azure_speech.key
        service_region = CONFIG.azure_speech.region

        self.speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        self.speech_config.speech_recognition_language = CONFIG.azure_speech.recognition_language
        self.speech_config.speech_synthesis_voice_name = CONFIG.azure_speech.voice_name

        self.model = speechsdk.KeywordRecognitionModel(f"{MODELS_PATH}/hey_bot_pi.table")

    def recognize(self):

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)

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

        speech_recognizer.start_keyword_recognition(self.model)
        print('Detecting keyword...')
        while not done:
            time.sleep(.5)

        speech_recognizer.recognized.disconnect_all()
        speech_recognizer.session_started.disconnect_all()
        speech_recognizer.session_stopped.disconnect_all()
        speech_recognizer.canceled.disconnect_all()
        del speech_recognizer
