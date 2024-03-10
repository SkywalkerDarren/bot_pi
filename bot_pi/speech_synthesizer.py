from audio_manager import AudioManager
import azure.cognitiveservices.speech as speechsdk

from config import CONFIG


class PushAudioOutputStreamSampleCallback(speechsdk.audio.PushAudioOutputStreamCallback):

    def __init__(self, am: AudioManager) -> None:
        super().__init__()

        self._stream = am.get_spk_stream(
            rate=CONFIG["sample_rate"],
            channels=CONFIG["channels"],
            width=CONFIG["width"]
        )
        self._stream.open()

    def write(self, audio_buffer: memoryview) -> int:
        print("{} bytes received.".format(audio_buffer.nbytes))
        self._stream.write(bytes(audio_buffer))
        return audio_buffer.nbytes

    def close(self) -> None:
        self._stream.close()
        print("Push audio output stream closed.")


class SpeechSynthesizer:
    def __init__(self):
        self._am = AudioManager()
        speech_key = CONFIG["key"]
        service_region = CONFIG["region"]

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_recognition_language = "zh-CN"
        speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
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
