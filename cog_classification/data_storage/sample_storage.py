from itertools import izip

import numpy as np


class SampleStorage:
    """
    Sample storage provides a way to represent samples known by agent and gives you a easy way to export this samples
    to format designed for machine learning algorithms.

    Every sample is associated with class of sample, environment of origin,
    category of sample storage (one sample can be associated with more than one category),
    weight of association to this category, which can affect removing of sample if weight is lower than fixed
    forgetting threshold.

    Each sample is represented as sample index in environment of origin at which is stored.
    It is result of concern about performance and memory usage.

    Each sample of the same category in sample storage has the same class. Every try to add sample with different
    class will result in creating new category and adding this sample to it.

    Weights can be increased and decreased but it will not remove samples from category directly. Even if weight of
    sample will drop to 0 (minimum weight), sample will be still part of category. To remove sample with weights lower
    than forgetting threshold methods remove weak samples and remove weak samples from category should be used.

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

        self.category_name = 0

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
        self.distance = distance

        self.categories = {}
        self.classes = {}

    def add_sample(self, sample_index, environment, category=None, sample_weight=None):
        """
        Adds the sample to given category or created new category if no category is given.
        Sample is represented by sample index in environment from which it originate.
        Sample has sample weight if given or default new weight of sample storage.
        Sample weight should be larger than or equal 0.

        If sample would be add to category, which class is different, then for sample there is generated new category.
        If sample would be add to category, that already contains this sample, then method do nothing.

        Sample can be added to multiple categories.
        """

        if sample_weight is None:
            sample_weight = self.new_weight
        else:
            assert sample_weight >= 0
            assert sample_weight <= self.max_weight

        sample_class = environment.get_class(sample_index)

        if category in self.categories:
            if sample_class == self.classes[category]:
                # No difference between class of sample and class of category.
                if not self.sample_in_category(sample_index, environment, category):
                    # Adding new sample to category
                    self.set_weight(environment, category, sample_weight, sample_index=sample_index)
            else:
                # There is difference in class of sample and class of category.
                # So we are adding sample to empty category (it forces creation of new category for sample).
                self.add_sample(sample_index, environment, sample_weight=sample_weight)
        else:
            # No such category in sample storage.
            # So we create new category for sample (and new name if category is None).
            category = self.create_new_category(environment, sample_class, category)
            self.set_weight(environment, category, sample_weight, sample_index=sample_index)

    def create_new_category(self, environment, sample_class, category=None):
        """
        Creation of new sample storage category.

        If category is given then we assert that this category is not in categories.
        This method add this new created category to sample storage categories.

        Create new category returns correct name of created category.
        """

        if category is None:
            # We create new name for category.

            # First we finds the name that wasn't used.
            name_in_categories = True
            name = None

            while name_in_categories:
                name_in_categories = False
                name = "Category number: " + str(self.category_name)
                for category_name in self.categories:
                    if category_name == name:
                        name_in_categories = True
                        break
                self.category_name += 1

            category = name
            # After while loop we didn't increase self.category_name because after finding unique name
            # we increased this value on the end of while loop.

        self.categories[category] = {}
        self.categories[category][environment] = ([], [])
        self.classes[category] = sample_class

        return category

    def decrease_weights(self):
        """
        Decrease weights of every sample according to alpha value.

        The weights will never drop below 0.

        This method didn't remove any sample.
        """
        for category in self.get_categories():
            self.decrease_weights_in_category(category)

    def decrease_weights_in_category(self, category):
        """
        Decrease weights of every sample in category according to alpha value.

        The weights will never drop below 0.

        This method didn't remove any sample.
        """

        the_category = self.categories[category]

        for environment in the_category:
            _, weights = the_category[environment]
            for i in range(len(weights)):
                weights[i] *= self.alpha

    def empty(self):
        """
        Tests if sample storage is empty.
        In sample storage there isn't category without samples.
        """
        return len(self.categories) == 0

    def export(self):
        """
        Returns numpy array of list of all attributes of every sample
        and second numpy array of categories in which samples are stored in sample storage.
        """
        samples = []
        samples_classes = []

        for category in self.get_categories():
            the_category = self.categories[category]

            single_category_samples = []
            for environment in the_category:
                sample_indexes, _ = the_category[environment]
                for index in sample_indexes:
                    single_category_samples.append(environment.get_sample(index))

            for sample in single_category_samples:
                samples.append(sample)
            samples_classes += [category] * len(single_category_samples)

        return np.array(samples), np.array(samples_classes)

    def increase_weights_in_category(self, sample_index, environment, category):
        """
        Increase the weights of samples in category according to their distance to sample modified by sigma and beta.

        Weights will never rise above max weight.
        """

        the_category = self.categories[category]
        sample = environment.get_sample(sample_index)

        for environment_local in the_category:

            sample_indexes, weights = the_category[environment_local]

            for i in range(len(sample_indexes)):

                category_sample = environment_local.get_sample(sample_indexes[i])

                if self.distance is None:
                    distance = environment.distance(category_sample, sample)
                else:
                    distance = self.distance(category_sample, sample)

                weight_change = self.beta * 0.1 ** (self.sigma * distance)
                new_weight = min(weights[i] + weight_change, self.max_weight)

                # We don't change value directly because it will be easier to change only set weight if some
                # changes will be necessary.
                self.set_weight(environment, category, new_weight, index=i)

    def remove_category(self, category):
        """ Removes category and all its samples from sample storage. """
        try:
            self.categories.pop(category)
            self.classes.pop(category)
        except KeyError:
            for c in self.categories:
                if category == c:
                    category = c
                    break

            self.categories.pop(category)
            self.classes.pop(category)

    def remove_sample_from_category(self, environment, category, sample_index=None, index=None):
        """
        Removes sample or item from index from category.

        Sample index - index of sample in environment.
        Index - index of sample index in category environment.

        One of the sample or index should be specified.

        If it was last sample then removes category and returns it's name, otherwise returns None.
        """

        the_category = self.categories[category]

        sample_indexes, weights = the_category[environment]

        if index is None:
            # We must find index of sample:
            for i in range(len(sample_indexes)):
                if sample_indexes[i] == sample_index:
                    index = i
                    break

        sample_indexes.pop(index)
        weights.pop(index)

        if self.get_category_samples_size(category) == 0:
            self.remove_category(category)
            return category

    def remove_weak_samples(self):
        """
        Removes samples, which weight is lower than forgetting threshold, in each category.

        Return list of all removed categories.
        """
        removed_categories = [self.remove_weak_samples_from_category(category) for category in self.get_categories()]
        return [category for category in removed_categories if category is not None]

    def remove_weak_samples_from_category(self, category):
        """
        Removes all samples which weight is lower than forgetting threshold.

        If all samples are removed from category, the category is removed too.
        """

        the_category = self.categories[category]
        for environment in the_category:

            to_remove = []
            sample_indexes, weights = the_category[environment]
            for i, (_, weight) in enumerate(izip(sample_indexes, weights)):
                if weight < self.forgetting_threshold:
                    to_remove.append(i)

            to_remove = sorted(to_remove, reverse=True)
            for i in to_remove:
                # Remove sample from category ensures removing categories without samples.
                self.remove_sample_from_category(environment, category, index=i)

    def sample_in_category(self, sample_index, environment, category):
        """ Checking if given sample index is in category. """
        if environment not in self.categories[category]:
            return False
        else:
            sample_indexes, _ = self.categories[category][environment]
            return sample_index in sample_indexes

    def get_category_samples(self, category):
        """ Returns list of tuple (sample_index, environment, weight) for category. """
        samples = []
        
        the_category = self.categories[category]
        for environment in the_category:
            sample_indexes, weights = the_category[environment]
            for sample_index, weight in izip(sample_indexes, weights):
                samples.append((sample_index, environment, weight))

        return samples

    def get_category_samples_size(self, category):
        """ Returns number of samples in given category. """
        size = 0

        the_category = self.categories[category]
        for environment in the_category:
            sample_indexes, _ = the_category[environment]
            size += len(sample_indexes)

        return size

    def get_categories(self):
        """ Returns labels of all categories of sample storage. """
        return self.categories.keys()

    def get_categories_size(self):
        """ Returns number of all categories of sample storage. """
        return len(self.categories)

    def get_class(self, category):
        """ Returns class of given category. """
        return self.classes[category]

    def set_distance(self, distance):
        """ Sets function to compute distance between two samples. """
        self.distance = distance

    def set_weight(self, environment, category, new_weight, sample_index=None, index=None):
        """
        Sets weight of given sample or item from index in given category to new weight.
        One of the sample or index should be specified.
        """
        assert new_weight >= 0
        assert new_weight <= self.max_weight

        the_category = self.categories[category]
        if environment not in the_category:
                the_category[environment] = ([], [])

        sample_indexes, weights = the_category[environment]

        if index is not None:
            # We know which weight change.
            weights[index] = new_weight
        else:
            # We must find index of sample_index.
            found = False
            for i, (index, weight) in enumerate(izip(sample_indexes, weights)):
                if index == sample_index:
                    weights[i] = new_weight
                    found = True
                    break

            if not found:
                sample_indexes.append(sample_index)
                weights.append(new_weight)
