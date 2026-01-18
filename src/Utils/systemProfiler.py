import time
from collections import deque

class SystemProfiler:
    def __init__(self, history=120):
        self.samples = {}  # system_name -> deque
        self.history = history

    def record(self, name, elapsed_ms):
        if name not in self.samples:
            self.samples[name] = deque(maxlen=self.history)
        self.samples[name].append(elapsed_ms)

    def stats(self):
        result = {}
        for name, values in self.samples.items():
            if not values:
                continue
            result[name] = {
                "avg": sum(values) / len(values),
                "max": max(values),
                "last": values[-1]
            }
        return result
