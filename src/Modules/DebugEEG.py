import numpy as np

class EEG:
    def __init__(self, shapes=[['axisname', 0]], timeaxis='timeaxisname', timerange=[0.0, 1.0]):
        self.axis_name = [ax[0] for ax in dim]
        self.dim = [ax[1] for ax in dim]

        self.eeg = np.zeros(dim)

        for ax in dim:
            if ax[0] == timeaxis:
                self.time = np.linspace(timerange[0], timerange[1], ax[1])
                break

        self.adds = []


    def AddSin(self, parameter = [[1.0, 1.0]], axis=None):
        if axis is None:
            for prm in parameter:
                amp, freq = prm
                self.eeg += amp * np.sin(2 * np.pi * freq * self.time)
                self.adds.append(prm)
        else:
            for prm in parameter:
                amp, freq = prm
                self.eeg += amp * np.sin(2 * np.pi * freq * self.time)
                self.adds.append(prm)

        return self.eeg

    def AddRand(self, amp=1.0):
        self.eeg += amp * np.random.randn(self.trialnum, self.chnum, self.samplenum)
        self.adds.append([amp, 'randn'])

        return self.eeg

    def Output(self):
        return self.eeg
