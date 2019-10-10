from itertools import chain
import numpy as np

class AdaptiveNetworkClassifier(object):
    """
    Class representing adaptive network of RBF (radial base function) units
    used as a classifier in Steels and Belpaeme (2005) work. Each sample
    stored in SampleStorage corresponds to a single RBF unit. Classifier
    response to a new sample is the weighted sum of RBF units activations.

    :param SampleStorage sample_storage: storage of samples associated with \
            specific classes (with weights)
    """

    def __init__(self, sample_storage):
        self.sample_storage = sample_storage

    def fit(self, X, y):
        pass

    def predict(self, X):
        categories = self.sample_storage.get_categories()
        proba = self.predict_proba(X)
        cls_indices = proba.argmax(axis=1)
        return np.array([categories[idx] for idx in cls_indices])

    def predict_proba(self, X):
        categories = self.sample_storage.get_categories()
        samples, labels, weights = self.sample_storage.export()
        activations = self.sample_storage.sample_activation(samples, X)*weights
        activations = np.atleast_2d(activations)
        res = np.hstack([activations[:, labels == cat].sum(axis=1)
                         for cat in categories])
        return np.atleast_2d(res)
