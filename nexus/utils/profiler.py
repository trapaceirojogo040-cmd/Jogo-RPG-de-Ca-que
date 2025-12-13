class Profiler:
    def __init__(self):
        self.samples = []

    def record(self, dt):
        self.samples.append(dt)

    def average(self):
        return sum(self.samples)/len(self.samples) if self.samples else 0
