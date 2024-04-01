# This file contains the implementation of a class for voice activity detection (VAD),
# based on the pre-trained model from Silero (https://github.com/snakers4/silero-vad).

import os
from collections import deque

import numpy as np
# Imports
import onnxruntime as ort

from config import MODELS_PATH


class VAD:
    """
    A model class for a voice activity detection (VAD) based on Silero's model:

    https://github.com/snakers4/silero-vad
    """

    def __init__(self,
                 model_path: str = os.path.join(MODELS_PATH, "silero_vad.onnx"),
                 n_threads: int = 1
                 ):
        """Initialize the VAD model object.

            Args:
                model_path (str): The path to the Silero VAD ONNX model.
                n_threads (int): The number of threads to use for the VAD model.
        """

        # Initialize the ONNX model
        sessionOptions = ort.SessionOptions()
        sessionOptions.inter_op_num_threads = n_threads
        sessionOptions.intra_op_num_threads = n_threads
        self.model = ort.InferenceSession(model_path, sess_options=sessionOptions,
                                          providers=["CPUExecutionProvider"])

        # Create buffer
        self.prediction_buffer: deque = deque(maxlen=125)  # buffer lenght of 10 seconds

        # Set model parameters
        self.sample_rate = np.array(16000).astype(np.int64)

        # Reset model to start
        self.reset_states()

    def reset_states(self, batch_size=1):
        self._h = np.zeros((2, batch_size, 64)).astype('float32')
        self._c = np.zeros((2, batch_size, 64)).astype('float32')
        self._last_sr = 0
        self._last_batch_size = 0
        self.prediction_buffer.clear()

    def predict(self, x, frame_size=480):
        """
        Get the VAD predictions for the input audio frame.

        Args:
            x (np.ndarray): The input audio, must be 16 khz and 16-bit PCM format.
                            If longer than the input frame, will be split into
                            chunks of length `frame_size` and the predictions for
                            each chunk returned. Must be a length that is integer
                            multiples of the `frame_size` argument.
            frame_size (int): The frame size in samples. The reccomended
                              default is 480 samples (30 ms @ 16khz),
                              but smaller and larger values
                              can be used (though performance may decrease).

        Returns
            float: The average predicted score for the audio frame
        """
        chunks = [(x[i:i + frame_size] / 32767).astype(np.float32)
                  for i in range(0, x.shape[0], frame_size)]

        frame_predictions = []
        for chunk in chunks:
            ort_inputs = {'input': chunk[None,],
                          'h': self._h, 'c': self._c, 'sr': self.sample_rate}
            ort_outs = self.model.run(None, ort_inputs)
            out, self._h, self._c = ort_outs
            frame_predictions.append(out[0][0])

        return np.mean(frame_predictions)

    def is_activity(self):
        vad_frames = list(self.prediction_buffer)[-5:]
        max_score = np.max(vad_frames) if len(vad_frames) > 0 else 0
        return max_score > 0.5

    def __call__(self, x, frame_size=160 * 4):
        self.prediction_buffer.append(self.predict(x, frame_size))
