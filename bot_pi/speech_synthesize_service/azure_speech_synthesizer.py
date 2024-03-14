import azure.cognitiveservices.speech as speechsdk

from audio_manager import AudioManager
from config import CONFIG
from speech_synthesize_service.speech_synthesizer import SpeechSynthesizer


class PushAudioOutputStreamSampleCallback(speechsdk.audio.PushAudioOutputStreamCallback):

    def __init__(self, am: AudioManager) -> None:
        super().__init__()

        self._stream = am.get_spk_stream(
            rate=16000,
            channels=1,
            width=2
        )
        self._stream.open()

    def write(self, audio_buffer: memoryview) -> int:
        print("{} bytes received.".format(audio_buffer.nbytes))
        self._stream.write(bytes(audio_buffer))
        return audio_buffer.nbytes

    def close(self) -> None:
        self._stream.close()
        print("Push audio output stream closed.")


class AzureSpeechSynthesizer(SpeechSynthesizer):
    def __init__(self):
        self._am = AudioManager()
        speech_key = CONFIG.azure_speech.key
        service_region = CONFIG.azure_speech.region

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name = CONFIG.azure_speech.voice_name
        self._speech_config = speech_config

    def text_to_speech(self, contents):
        output_config = speechsdk.audio.AudioOutputConfig(
            stream=speechsdk.audio.PushAudioOutputStream(
                PushAudioOutputStreamSampleCallback(self._am)
            )
        )
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self._speech_config,
            audio_config=output_config
        )
        speech_synthesis_result = speech_synthesizer.speak_text_async(contents).get()
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(contents))

        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
        del speech_synthesizer
