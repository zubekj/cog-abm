""" Module implementing agent in the system. """

from multiprocessing import Lock

from sklearn import svm

from sample_storage import SampleStorage


class Agent(object):
    """
    Class representing agent in the system.
    """

    # AID is set that it will match networks nodes.
    AID = 0
    AID_lock = Lock()

    def __init__(self, aid=None, classifier=svm.SVC(gamma=0.001, C=100), sample_storage=SampleStorage()):
        self.id = aid or Agent.get_next_id()
        self.classifier = classifier
        self.sample_storage = sample_storage

    @classmethod
    def get_next_id(cls):
        cls.AID_lock.acquire()
        aid = cls.AID
        cls.AID += 1
        cls.AID_lock.release()
        return aid

    def classify(self, sample):
        return self.classifier.predict(sample)

    def good_category_for_topic(self, category, topic, distance):
        self.sample_storage.increase_weights_in_class(topic, category, distance)

    def get_id(self):
        return self.id



