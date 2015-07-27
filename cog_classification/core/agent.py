""" Module implementing agent in the system. """

from multiprocessing import Lock

from sklearn import svm
from sklearn.utils.validation import NotFittedError

from sample_storage import SampleStorage


class Agent(object):
    """
    Class representing agent in the system.
    """

    # AID is set that it will match networks nodes.
    AID = 0
    AID_lock = Lock()

    def __init__(self, aid=None, classifier=None, sample_storage=None):
        self.id = aid or Agent.get_next_id()
        self.classifier = classifier or svm.SVC()
        self.sample_storage = sample_storage or SampleStorage()

        self.fitness = {}

    @classmethod
    def get_next_id(cls):
        cls.AID_lock.acquire()
        aid = cls.AID
        cls.AID += 1
        cls.AID_lock.release()
        return aid

    def add_topic_to_class(self, category, topic, environment):
        self.sample_storage.add_sample(topic, environment, category)

    def add_topic_to_new_class(self, topic, environment):
        self.sample_storage.add_sample(topic, environment)

    def classify(self, sample):
        if self.sample_storage.get_classes_size() == 1:
            return self.sample_storage.get_classes()
        else:
            try:
                return self.classifier.predict([sample])
            except NotFittedError:
                return None

    def forget(self):
        self.sample_storage.decrease_weights()

    def good_category_for_topic(self, category, topic, environment):
        self.sample_storage.increase_weights_in_class(topic, environment, category)

    def learn(self):
        data, decisions = self.sample_storage.export()
        if len(decisions) > 0 and self.sample_storage.get_classes_size() > 1:
            self.classifier.fit(data, decisions)

    def update_fitness(self, name, information):
        self.fitness[name].update(information)

    def get_id(self):
        return self.id

    def get_fitness_measure(self, name):
        return self.fitness[name].get_measure()

    def set_fitness(self, name, fitness_measure):
        self.fitness[name] = fitness_measure
