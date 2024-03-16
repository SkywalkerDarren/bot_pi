import unittest



class MyTestCase(unittest.TestCase):
    def test_azure(self):
        from speech_synthesize_service.azure_speech_synthesizer import AzureSpeechSynthesizer
        AzureSpeechSynthesizer().text_to_speech('国家发展改革委15日对外发布《促进国家级新区高质量建设行动计划》，推动国家级新区努力打造高质量发展引领区、改革开放新高地、城市建设新标杆。')

    def test_openai(self):
        from speech_synthesize_service.openai_speech_synthesizer import OpenAISpeechSynthesizer
        OpenAISpeechSynthesizer().text_to_speech('国家发展改革委15日对外发布《促进国家级新区高质量建设行动计划》，推动国家级新区努力打造高质量发展引领区、改革开放新高地、城市建设新标杆。')


if __name__ == '__main__':
    unittest.main()
