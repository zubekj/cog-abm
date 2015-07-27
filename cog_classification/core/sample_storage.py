from itertools import izip

import numpy as np


class SampleStorage:
    """
    Sample storage provides a way to represent samples known by agent and gives you a easy way to export this samples
    to format designed for machine learning algorithms.

    Every sample is associated with true class of sample, environment of origin,
    class of sample storage (one sample can be associated with more than one class),
    weight of association to this class, which can affect removing of sample if weight is lower than fixed
    forgetting threshold.

    Each sample is represented as index in environment of origin at which is stored. It is result of concern about
    performance and memory usage.

    Each sample of the same class from sample storage has the same true class. Every try to add sample with different
    true class will result in creating new class add adding this sample to it.

    Weights can be increased and decreased but it will not remove samples from class directly. Even if weight of
    sample will drop to 0 (minimum weight), sample will be still part of class. To remove sample with weights lower
    than forgetting threshold methods remove weak samples and remove weak samples from class should be used.

    Sample storage is implementation of the class described in Konrad Kurdej's master's thesis:
    "Modelowanie procesow poznawczych: konsensusowa metoda klasyfikacji z komunikacja miedzy agentami".
    """

    def __init__(self, alpha=0.99, beta=1, sigma=1, new_weight=1, max_weight=1,
                 forgetting_threshold=0.05, distance=None):
        """
        Parameters explanation:
        alpha - how fast samples are forgotten. Values from 0 (total sclerosis) to 1 (perfect memory).
        beta - how much weights of samples will be increased. Values from 0 (no strengthening) to infinity.
        sigma - affects how factor of similarity affects strengthening of weights.
                Value form 0 (similarity doesn't affects strengthening)
                      to infinity (the less similar samples the weaker strengthen).
        max_weight - the maximum weight of sample. Value from 0 to infinity.
        new_weight - the weight of new sample added to sample storage if no other value were given.
                     Value from 0 to max weight.
        forgetting_threshold - the samples with lower weight value than forgetting threshold value are removed.
                               Value from 0 to max weight.
        distance - default function which can compute distance between two samples.
        """

        self.class_name = 0

        self.alpha = alpha
        assert alpha >= 0
        assert alpha <= 1

        self.beta = beta
        assert beta >= 0

        self.sigma = sigma
        assert sigma >= 0

        self.max_weight = max_weight
        assert max_weight >= 0

        self.new_weight = new_weight
        assert new_weight >= 0
        assert new_weight <= max_weight

        self.forgetting_threshold = forgetting_threshold
        assert new_weight >= 0
        assert new_weight <= max_weight

        # Distance is used only in increase weights.
        self.distance = distance or self.standard_distance

        self.classes = {}
        self.true_classes = {}

    def add_sample(self, sample, environment, target_class=None, sample_weight=None):
        """
        Adds the sample to given target class or created new class if no target class is given.
        Sample is represented by index in environment from which it orginate.
        Sample has sample weight if given or default new weight of sample storage.
        Sample weight should be larger than or equal 0.

        If sample would be add to class, which true class is different, then for sample there is generated new class.
        If sample would be add to class, that already contains this sample, then method do nothing.

        Sample can be added to multiple classes.
        """

        if sample_weight is None:
            sample_weight = self.new_weight
        else:
            assert sample_weight >= 0
            assert sample_weight <= self.max_weight

        true_class = environment.get_true_class(sample)

        if target_class in self.classes:
            if true_class == self.true_classes[target_class]:
                # No difference between true classes of sample and target_class.
                if not self.sample_in_class(sample, environment, target_class):
                    # Adding new sample to class
                    self.set_weight(environment, target_class, sample_weight, sample=sample)
            else:
                # There is difference in true classes of sample and given target class.
                # So we are adding sample to empty class (it forces creation of new class for sample).
                self.add_sample(sample, environment, sample_weight=sample_weight)
        else:
            # No target class in sample storage.
            # So we create new class for sample (and new name if target_class is None).
            target_class = self.create_new_class(target_class, environment, true_class)
            self.set_weight(environment, target_class, sample_weight, sample=sample)

    def create_new_class(self, target_class, environment, true_class):
        """
        Creation of new sample storage class.

        If target class is given then we assert that this class is not in classes.
        This method add this new created class to sample storage classes.

        Create new class returns correct name of created class.
        """

        if target_class is None:
            # We create new name for target class.

            # First we finds the name that wasn't used.
            name_in_classes = True
            name = None

            while name_in_classes:
                name_in_classes = False
                name = "Class number: " + str(self.class_name)
                for class_name in self.classes:
                    if class_name == name:
                        name_in_classes = True
                        break
                self.class_name += 1

            target_class = name
            # After while loop we didn't increase self.class_name because after finding unique name
            # we increased this value on the end of while loop.

        self.classes[target_class] = {}
        self.classes[target_class][environment] = ([], [])
        self.true_classes[target_class] = true_class

        return target_class

    def decrease_weights_in_class(self, target_class):
        """
        Decrease weights of every sample in target class according to alpha value.

        The weights will never drop below 0.

        This method didn't remove any sample.
        """

        the_class = self.classes[target_class]

        for environment in the_class:
            _, weights = the_class[environment]
            for i in range(len(weights)):
                weights[i] *= self.alpha

    def decrease_weights(self):
        """
        Decrease weights of every sample according to alpha value.

        The weights will never drop below 0.

        This method didn't remove any sample.
        """
        for target_class in self.get_classes():
            self.decrease_weights_in_class(target_class)

    def empty(self):
        """
        Tests if sample storage is empty.
        In sample storage there isn't class without samples.
        """
        return len(self.classes) == 0

    def export(self):
        """
        Returns list of list of all attributes of every sample
        and second list of class in which sample is in sample storage.
        """
        data = []
        decisions = []

        for target_class in self.get_classes():
            the_class = self.classes[target_class]

            true_samples = []
            for environment in the_class:
                indexes, _ = the_class[environment]
                for index in indexes:
                    true_samples.append(environment.get_sample(index))

            for single_data in true_samples:
                data.append(single_data)
            decisions += [target_class] * len(true_samples)

        return np.array(data), np.array(decisions)

    def increase_weights_in_class(self, sample, environment, target_class):
        """
        Increase the weights of samples in target class
        according to their distance to sample modified by sigma and beta.

        Weights will never rise above max weight.
        """

        the_class = self.classes[target_class]
        sample = environment.get_sample(sample)
        for environment_local in the_class:
            indexes, weights = the_class[environment_local]
            for i in range(len(indexes)):
                class_sample = environment_local.get_sample(indexes[i])
                weight_change = self.beta * 0.1 ** (self.sigma * self.distance(class_sample, sample))
                new_weight = min(weights[i] + weight_change, self.max_weight)
                # We don't change value directly because it will be easier to change only set weight if some
                # changes will be necessary.
                self.set_weight(environment, target_class, new_weight, index=i)

    def remove_class(self, target_class):
        """ Removes class and all its samples from sample storage. """
        try:
            self.classes.pop(target_class)
        except KeyError:
            for c in self.classes:
                if target_class == c:
                    target_class = c
                    break

            self.classes.pop(target_class)

    def remove_sample_from_class(self, environment, target_class, sample=None, index=None):
        """
        Removes sample or item from index from target class.

        One of the sample or index should be specified.

        If it was last sample then removes target class, too.
        """

        the_class = self.classes[target_class]

        indexes, weights = the_class[environment]

        if index is None:
            # We must find index of sample:
            for i in range(len(indexes)):
                if indexes[i] == sample:
                    index = i
                    break

        indexes.pop(index)
        weights.pop(index)

        if self.get_class_samples_size(target_class) == 0:
            self.remove_class(target_class)

    def remove_weak_samples(self):
        """
        Removes samples, which weight is lower than forgetting threshold, in each class.
        """
        for target_class in self.get_classes():
            self.remove_weak_samples_from_class(target_class)

    def remove_weak_samples_from_class(self, target_class):
        """
        Removes all samples which weight is lower than forgetting threshold.

        If all samples are removed from class, the class is removed too.
        """

        the_class = self.classes[target_class]
        for environment in the_class:

            to_remove = []
            indexes, weights = the_class[environment]
            for i, (index, weight) in enumerate(izip(indexes, weights)):
                if weight < self.forgetting_threshold:
                    to_remove.append(i)

            to_remove = sorted(to_remove, reverse=True)
            for i in to_remove:
                # Remove sample from class ensures removing classes without samples.
                self.remove_sample_from_class(environment, target_class, index=i)

    def sample_in_class(self, sample, environment, target_class):
        """ Checking if given sample is in target class. """
        if environment not in self.classes[target_class]:
            return False
        else:
            indexes, _ = self.classes[target_class][environment]
            return sample in indexes

    @staticmethod
    def standard_distance(sample1, sample2):
        """ Calculates standard distance between two samples of numerical values. """

        distance = 0
        for v1, v2 in izip(sample1, sample2):
            distance += abs(v1 - v2)

        return distance

    def get_class_samples(self, target_class):
        """ Returns list of tuple (sample, environment, weight) for target class. """
        samples = []
        
        the_class = self.classes[target_class]
        for environment in the_class:
            indexes, weights = the_class[environment]
            for index, weight in izip(indexes, weights):
                samples.append((index, environment, weight))

        return samples

    def get_class_samples_size(self, target_class):
        """ Returns number of samples in given target class. """
        size = 0

        the_class = self.classes[target_class]
        for environment in the_class:
            indexes, _ = the_class[environment]
            size += len(indexes)

        return size

    def get_classes(self):
        """ Returns labels of all classes of sample storage. """
        return self.classes.keys()

    def get_classes_size(self):
        """ Returns number of all classes of sample storage. """
        return len(self.classes)

    def get_true_class(self, target_class):
        """ Returns true class of given target class. """
        return self.true_classes[target_class]

    def set_distance(self, distance):
        """ Sets function to compute distance between two samples. """
        self.distance = distance

    def set_weight(self, environment, target_class, new_weight, sample=None, index=None):
        """
        Sets weight of given sample or item from index in given target class to new weight.
        One of the sample or index should be specified.
        """
        assert new_weight >= 0
        assert new_weight <= self.max_weight

        the_class = self.classes[target_class]
        if environment not in the_class:
                the_class[environment] = ([], [])

        indexes, weights = the_class[environment]

        if index is not None:
            # We know which weight change.
            weights[index] = new_weight
        else:
            # We must find index of sample.
            found = False
            for i, (index, weight) in enumerate(izip(indexes, weights)):
                if index == sample:
                    weights[i] = new_weight
                    found = True
                    break

            if not found:
                indexes.append(sample)
                weights.append(new_weight)
