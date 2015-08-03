from collections import deque


class Fitness:

    def __init__(self):
        pass

    def get_measure(self):
        pass

    def update(self, value):
        pass


class StandardFitness(Fitness):

    def __init__(self):
        self.success = 0
        self.all = 0

    def get_measure(self):
        if self.all == 0:
            return 0
        else:
            return float(self.success) / self.all

    def update(self, value):
        self.all += 1
        self.success += value


class CurrentFitness(Fitness):

    def __init__(self, scope=50):
        self.scope = scope
        self.memories = deque([])

    def get_measure(self):
        if len(self.memories) < 1:
            return 0
        else:
            return float(sum(self.memories)) / len(self.memories)

    def update(self, value):
        while len(self.memories) >= self.scope:
            self.memories.pop()
        self.memories.append(value)
