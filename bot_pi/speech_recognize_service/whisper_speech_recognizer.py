from whispercpp import api, Whisper

from config import PROJECT_ROOT
from speech_recognize_service.speech_recognizer import SpeechRecognizer


class WhisperSpeechRecognizer(SpeechRecognizer):

    def __init__(self):
        params = (  # noqa # type: ignore
            api.Params.from_enum(api.SAMPLING_BEAM_SEARCH)
            .with_language("zh")
            .with_print_progress(False)
            .with_print_realtime(False)
            .build()
        )
        print(params)
        self.w = Whisper.from_params(f"{PROJECT_ROOT}/models/whisper/ggml-base.bin", params)

    def speech_to_text(self):
        result = self.w.stream_transcribe()
        for r in result:
            print(r)
