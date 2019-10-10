import numpy as np
import random


class Environment(object):
    """
    Stores samples and their classes.

    :param list samples: list of samples. Not empty.
    :param list classes: list of samples' classes. Not empty.
    :param distance: distance function between two samples.
    :type distance: function(sample, sample)

    Samples and classes should have the same length.
    """

    def __init__(self, samples, classes, distance=None):
        assert samples is not None and classes is not None
        assert not samples == [] and not classes == []
        assert len(samples) == len(classes)

        self.samples = samples
        self.classes = classes

        if distance is None:
            distance = self.standard_distance

        self.distance = distance

    @staticmethod
    def standard_distance(sample1, sample2):
        """
        Calculates standard distance between two samples of numerical values.
        Defaults to Euclidean distance.

        :param iterable sample1: first sample.
        :param iterable sample2: second sample.

        :return: the calculated distance.
        :rtype: float
        """

        distance = 0
        for v1, v2 in zip(sample1, sample2):
            distance += (v1 - v2)**2

        return distance**0.5

    def get_all(self):
        """
        :returns: * list of all samples *(list)*
            * list of all classes *(list)*
        """
        return self.samples, self.classes

    def get_class(self, index):
        """
        Returns class of sample with given index.

        :param long index: the index of the sample whose class is needed.

        :return: class of sample with given index.
        :rtype: numpy array
        """
        return np.array(self.classes[index])

    def get_random_sample(self):
        """
        Return a random sample from all samples.

        :returns: * index of drawn sample *(long)*
            * drawn sample *(list)*
            * class of drawn sample
        """
        index = random.randrange(len(self.samples))
        sample = self.get_sample(index)
        sample_class = self.get_class(index)
        return index, sample, sample_class

    def get_random_context_samples(self, num_samples, topic_index):
        """
        Returns a number of random samples which are different than topic.
        In the default implementation samples have to belong to different
        classes.

        :param int topic_index: index of the topic sample present in the \
                environment

        :return: list of samples which are different than topic
        """
        samples = []
        sample_indices = set()
        topic_class = self.get_class(topic_index)
        while True:
            index, sample, cls = self.get_random_sample()
            if not cls == topic_class and index not in sample_indices:
                samples.append(sample)
                sample_indices.add(index)
                if len(samples) == num_samples:
                    return samples

    def get_sample(self, index):
        """
        Returns sample with specified index.

        :param long index: specified index.

        :return: sample associated with given index.
        :rtype: numpy array
        """
        return np.array(self.samples[index])

    def get_samples(self, indexes):
        """
        :param iterable indexes: specified indexes.

        :return: samples associated with given indexes.
        :rtype: numpy array
        """
        return np.array([self.samples[index] for index in indexes])


class NoClassEnvironment(Environment):
    """
    A variant of environment where all samples belong to a single class.
    Difference between topic and context in get_random_context_samples is checked
    based on sample distance threshold.

    :param list samples: list of samples. Not empty.
    :param float distance_threshold: threshold for checking sample similarity.
    :param distance: distance function between two samples.
    :type distance: function(sample, sample)
    """

    def __init__(self, samples, distance_threshold=0, distance=None):
        self.distance_threshold = distance_threshold
        classes = [0] * len(samples)
        super(NoClassEnvironment, self).__init__(samples, classes, distance)

    def get_random_context_samples(self, num_samples, topic_index):
        """
        Returns a number of random samples which are different than topic.
        The distance between samples has to be larger then distance_threshold.

        :param int topic_index: index of the topic sample present in the \
                environment

        :return: list of samples which are different than topic
        """
        samples = []
        sample_indices = set()
        topic = self.get_sample(topic_index)
        while True:
            index, sample, _ = self.get_random_sample()
            if self.distance(topic, sample) > self.distance_threshold \
                    and index not in sample_indices:
                samples.append(sample)
                sample_indices.add(index)
                if len(samples) == num_samples:
                    return samples
