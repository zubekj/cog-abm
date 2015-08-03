from cog_classification.steels_classifier.steels_classifier import SteelsClassifier

from sklearn import datasets


class TestSteelsClassifier:

    def __init__(self):
        self.classifier = None

    def setup(self):
        self.classifier = SteelsClassifier()

    def test_classifier_1(self):
        """ Simple test using irises. """
        iris = datasets.load_iris()
        self.classifier.fit(iris.data, iris.target)

        success = 0
        for i, sample in iris.data:
            success += self.classifier.predict(sample) == iris.target[i]

        print(float(success)/len(iris.data))