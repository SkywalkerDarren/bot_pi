import unittest


class MyTestCase(unittest.TestCase):
    def test_azure(self):
        from speech_recognize_service.azure_speech_recognizer import AzureSpeechRecognizer
        text = AzureSpeechRecognizer().speech_to_text()
        print(text)

    def test_whisper(self):
        from speech_recognize_service.whisper_speech_recognizer import WhisperSpeechRecognizer
        WhisperSpeechRecognizer().speech_to_text()

    def test_openai(self):
        from speech_recognize_service.openai_speech_recognizer import OpenAISpeechRecognizer
        text = OpenAISpeechRecognizer().speech_to_text()
        print(text)


if __name__ == '__main__':
    unittest.main()
