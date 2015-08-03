""" Module implementing steels agent used in classification task. """

from sklearn import svm
from sklearn.utils.validation import NotFittedError

from cog_classification.steels_universal.steels_agent import SteelsAgent
from cog_classification.data_storage.sample_storage import SampleStorage

from itertools import izip


class SteelsClassificationAgent(SteelsAgent):

    def __init__(self, aid=None, lexicon=None, classifier=None, sample_storage=None):
        SteelsAgent.__init__(self, aid, lexicon)
        self.classifier = classifier or svm.SVC()
        self.sample_storage = sample_storage or SampleStorage()

    def add_sample(self, sample_index, environment, category=None):
        """
        Adds sample_index form environment to storage.
        """
        self.sample_storage.add_sample(sample_index, environment, category)

    def choose_the_best_sample_for_category(self, category, samples):

        the_best_sample = None
        the_best_probability = -float('inf')

        # We are looking for a sample that probability of belonging to guesses category is the highest.
        for sample in samples:
            probability = self.get_probability(sample, category)
            if the_best_probability < probability:
                the_best_probability = property
                the_best_sample = sample

        return the_best_sample

    def classify(self, sample):
        """
        Classify given specific sample.

        If agent known only one class, it return the class.
        If agent hasn't taught any classification yet, it  return None.
        """
        if self.sample_storage.get_categories_size() == 1:
            return self.sample_storage.get_categories()[0]
        else:
            try:
                # Classifier predicts categories for array of samples and returns array of predicted categories.
                return self.classifier.predict([sample])[0]
            except NotFittedError:
                return None

    def forget(self):
        """
        Weakens agent's memory of all known samples and removes categories that become scarcely known.
        """
        self.sample_storage.decrease_weights()
        removed_categories = self.sample_storage.remove_weak_samples()

        for category in removed_categories:
            self.lexicon.remove_category(category)

    def strengthen_memory_sample_category(self, category, sample_index, environment):
        """
        Strengthen memory of sample storage samples in category that are similar to sample form environment.
        """
        self.sample_storage.increase_weights_in_category(sample_index, environment, category)

    def learn(self):
        """
        Teaches classifier using samples and class from sample storage.
        """
        data, decisions = self.sample_storage.export()
        if len(decisions) > 0 and self.sample_storage.get_categories_size() > 1:
            self.classifier.fit(data, decisions)

    def get_category_class(self, category):
        """"
        Returns class of given category.
        """
        return self.sample_storage.get_class(category)

    def get_probability(self, sample, sample_category):
        probabilities = self.classifier.class_probabilities([sample])

        for category, probability in izip(self.classifier.classes, probabilities):
            if sample_category == category:
                return probability

        return 0
