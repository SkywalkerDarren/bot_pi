import unittest


class MyTestCase(unittest.TestCase):
    def test_azure(self):
        from keyword_recognize_service.azure_keyword_reconizer import AzureKeywordRecognizer
        AzureKeywordRecognizer().recognize()

    def test_oww(self):
        # import openwakeword.utils
        # openwakeword.utils.download_models()

        from keyword_recognize_service.open_wakeup_word_recognizer import OpenWakeupWordRecognizer
        OpenWakeupWordRecognizer().recognize()


if __name__ == '__main__':
    unittest.main()
