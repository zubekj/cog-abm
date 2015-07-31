from itertools import izip

import numpy as np
import random


class Environment:
    """
    Stores samples and their classes.
    """

    def __init__(self, samples, classes, distance=None):
        """
        Args:
            samples (list): list of samples.
            classes (list): list of samples' classes.
            distance (function): distance function between two samples.
        """
        self.samples = samples
        self.classes = classes

        if distance is None:
            distance = self.standard_distance

        self.distance = distance

    @staticmethod
    def standard_distance(sample1, sample2):
        """ Calculates standard distance between two samples of numerical values. """

        distance = 0
        for v1, v2 in izip(sample1, sample2):
            distance += abs(v1 - v2)

        return distance

    def get_all(self):
        """
        Returns:
            ((list, list)) list of samples and list of classes.
        """
        return self.samples, self.classes

    def get_all_classes(self):
        return self.classes

    def get_all_samples(self):
        return self.samples

    def get_random_sample(self):
        return random.choice(self.samples)

    def get_random_sample_index(self):
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

    def get_class(self, index):
        """
        Returns class of sample with given index.
        """
        return np.array(self.classes[index])

    def set_distance(self, distance):
        """"
        Change environment distance function.
        """
        self.distance = distance
