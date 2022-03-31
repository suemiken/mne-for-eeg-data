import time

class StopWatch:
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0

    def Start(self):
        self.start_time = time.clock()

    def Stop(self):
        self.stop_time = time.clock()

    def Get(self):
        return self.stop_time - self.start_time

    def Reset(self):
        self.start_time = 0
        self.stop_time = 0
