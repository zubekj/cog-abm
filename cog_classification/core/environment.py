import random
import numpy as np


class Environment:
    """
    Stores samples and their classes.
    """

    def __init__(self, samples, classes):
        """
        Parameters explanation:
        samples - list of samples
        classes - list of samples' classes
        """
        self.samples = samples
        self.classes = classes

    def get_random_sample(self):
        """
        Returns random sample.
        """
        return random.choice(self.samples)

    def get_random_sample_index(self):
        """
        Returns index of random sample.
        """
        return random.randrange(len(self.samples))

    def get_sample(self, index):
        """
        Returns sample with specified index.
        """
        return np.array(self.samples[index])

    def get_samples(self, indexes):
        """
        Returns list of samples with given indexes.
        """
        return np.array([self.samples[index] for index in indexes])

    def get_true_class(self, index):
        """
        Returns class of sample with given index.
        """
        return np.array(self.classes[index])
