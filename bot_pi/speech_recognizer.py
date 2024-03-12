import azure.cognitiveservices.speech as speechsdk

from config import CONFIG


class SpeechRecognizer:

    def __init__(self):
        speech_key = CONFIG.azure_speech.key
        service_region = CONFIG.azure_speech.region
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_recognition_language = CONFIG.azure_speech.recognition_language
        self._speech_config = speech_config

    def speech_to_text(self):
        speech_list = []

        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print('SPEECH RECOGNIZED: {}'.format(evt))
                speech_list.append(evt.result.text)
            elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                print('SPEECH NOMATCH: {}'.format(evt))

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self._speech_config)
        speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs,
                                                  "5000")
        speech_recognizer.properties.set_property(
            speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs,
            "5000")
        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.recognize_once()
        speech_recognizer.recognized.disconnect_all()
        del speech_recognizer
        return speech_list
