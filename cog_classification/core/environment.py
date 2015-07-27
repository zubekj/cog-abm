import random
import numpy as np


class Environment:

    def __init__(self, data, decisions):
        self.data = data
        self.decisions = decisions

        random.seed()

    def get_random_sample(self):


    def get_sample(self, index):
        return np.array(self.data[index])

    def get_samples(self, indexes):
        return np.array([self.data[index] for index in indexes])

    def get_true_class(self, index):
        return np.array(self.decisions[index])
