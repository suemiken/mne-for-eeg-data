import numpy as np
from scipy import signal
class butter:
    def __init__(self, lowcut, highcut, fs, order=5, filter_type='bandpass'):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        self.b, self.a = signal.butter(order, [low, high], btype=filter_type)

    def fit(self, data, axis=-1):
        return signal.lfilter(self.b, self.a, data, axis=axis)
        
class butter2:
    def __init__(self, lowcut, highcut, fs, order=5, filter_type='bandpass'):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        self.sos = signal.butter(order, [low, high], btype=filter_type, output='sos')

    def fit(self, data, axis=-1):
        return signal.sosfiltfilt(self.sos, data, axis=axis)
