import os
import threading
import unittest
import wave
from concurrent.futures import ThreadPoolExecutor

from audio_service.audio_manager import AudioManager
from audio_service.vad import VAD


class MyTestCase(unittest.TestCase):
    def test_mic(self):
        am = AudioManager()
        mic = am.get_mic_stream()
        vad = VAD()
        v = vad.get_vad()

        with mic as recorder:
            print('recording')
            have_data = True
            while have_data:
                wav = recorder.read()
                have_data = len(wav) > 0
                audio_float32 = vad.int2float(wav)
                result = v(audio_float32)
                if result and 'end' in result:
                    print('voiced')
                    break
        print('recording done')

    def test_multi_use_microphone(self):
        am = AudioManager()

        def record():
            mic = am.get_mic_stream()
            vad = VAD()
            v = vad.get_vad()
            with mic as recorder:
                print('recording', threading.current_thread().name)
                have_data = True
                while have_data:
                    wav = recorder.read()
                    have_data = len(wav) > 0
                    audio_float32 = vad.int2float(wav)
                    result = v(audio_float32)
                    if result and 'end' in result:
                        print('voiced', threading.current_thread().name)
                        break
            print('recording done', threading.current_thread().name)

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(record)
            executor.submit(record)

    def test_spk(self):
        p = os.path.dirname(__file__)
        with wave.open(os.path.join(p, "StarWars3.wav")) as wav:
            wav: wave.Wave_read
            am = AudioManager()
            spk = am.get_spk_stream(
                rate=wav.getframerate(),
                channels=wav.getnchannels(),
                width=wav.getsampwidth()
            )
            with spk as speaker:
                print('speaking')
                speaker.write(wav.readframes(wav.getnframes()))
            print('speaking done')


if __name__ == '__main__':
    unittest.main()
