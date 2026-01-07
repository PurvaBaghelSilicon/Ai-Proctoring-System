import sounddevice as sd
import numpy as np

class AudioDetector:
    def __init__(self, threshold=0.05):
        self.threshold = threshold
        self.rms = 0

    def callback(self, indata, frames, time, status):
        self.rms = np.sqrt(np.mean(indata**2))

    def start(self):
        self.stream = sd.InputStream(callback=self.callback)
        self.stream.start()

    def is_spike(self):
        return self.rms > self.threshold

    def stop(self):
        self.stream.stop()
