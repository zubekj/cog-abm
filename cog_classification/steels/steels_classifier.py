import random

from sklearn.utils.validation import NotFittedError

from cog_classification.core.environment import Environment
from cog_classification.core.fitness import CurrentFitness
from cog_classification.core.network import Network
from cog_classification.core.simulation import Simulation
from cog_classification.core.condition import IterationCondition
from steels_classifier_results import SteelsClassifierResults
from cog_classification.steels.guessing_game import GuessingGame
from cog_classification.steels.steels_classification_agent import SteelsClassificationAgent
from cog_classification.tools.topology_generator import generate_topology
from cog_classification.core.behavior_switcher import BehaviorSwitcher


class SteelsClassifier:
    """
    Classifier founded on Steels and Belpaeme multi-agent network and interactions concept.

    :param classifiers: Classifiers that will be used with agents creation.
    :type classifiers: List of classifiers.
    """

    def __init__(self, classifiers=None, alpha=0.99, good_agent_measure=0.95):
        self.classifiers = classifiers
        self.alpha = alpha
        self.good_agent_measure = good_agent_measure
        self.simulation = None
        self.result = None
        self.condition = IterationCondition(1000)
        self.interactions = BehaviorSwitcher(GuessingGame(good_agent_measure=self.good_agent_measure))

    def fit(self, x, y):
        """
        Fit the steels classifier according to the given training data.

        :param list x: Samples.
        :param list y: Samples' classes.
        """

        environment = Environment(x, y)

        agents = {}

        if self.classifiers is None:
            for _ in range(15):
                agent = SteelsClassificationAgent(alpha=self.alpha)
                agents[agent.id] = agent
        else:
            for classifier in self.classifiers:
                agent = SteelsClassificationAgent(classifier=classifier, alpha=self.alpha)
                agents[agent.id] = agent

        for agent in agents.values():
            agent.set_fitness("DG", CurrentFitness())
            agent.set_fitness("GG", CurrentFitness())

        network = Network(agents, {1: generate_topology("clique", agents_names=agents.keys())})

        self.simulation = Simulation(network, self.interactions, BehaviorSwitcher(environment),
                                     SteelsClassifierResults(), self.condition)

        self.result = self.simulation.run()

    def predict(self, samples):
        """
        :param list samples: The samples which classes are predicted.

        :raise: **NotFittedError** - if no data have been fitted yet.

        :return: The predicted classes of sample.
        :rtype: list
        """
        if self.result is not None:
            return self.result.predict(samples)
        else:
            raise NotFittedError


class SteelsClassifierExtended(SteelsClassifier):
    """
    Classifier founded on Steels and Belpaeme multi-agent network and interactions concept.

    This classifier extends standard classifier on data access options.

    :param classifiers: Classifiers that will be used with agents creation.
    :type classifiers: List of classifiers.
    """

    @staticmethod
    def accuracy(classifier, x, y):
        predicted_y = classifier.predict(x)
        return float(len([i for i in range(len(y)) if y[i] == predicted_y[i]])) / len(y)

    def get_results(self, samples, classes):

        def categories_count(agent):
            categories = []

            for sample in samples:
                category = agent.classify(sample)
                if category is not None:
                    if all([category != c for c in categories]):
                        categories.append(category)

            return len(categories), [agent.get_category_size(category) for category in categories]

        data = zip(samples, classes)
        random.shuffle(data)
        samples, classes = zip(*data)
        samples = list(samples)
        classes = list(classes)

        border = len(samples) * 2 / 3

        self.fit(samples[:border], classes[:border])

        categories = [categories_count(agent) for agent in self.result.results['agents']]

        categories_min = 1000
        categories_max = -1
        categories_sum = 0

        avg_agent_sum = 0
        avg_total_sum = 0
        samples_max = 0

        for category_number, list_of_stimuli in categories:
            if category_number > categories_max:
                categories_max = category_number
            if category_number < categories_min:
                categories_min = category_number
            categories_sum += category_number

            if category_number > 0:
                avg_agent_sum += float(sum(list_of_stimuli)) / category_number
                avg_total_sum += sum(list_of_stimuli)
                samples_max = max(samples_max, max(list_of_stimuli))

        category_avenge = float(categories_sum) / len(categories)

        agent_avenge_sample_number = avg_agent_sum / len(categories)
        if categories_sum > 0:
            avenge_sample_number = float(avg_total_sum) / categories_sum
        else:
            avenge_sample_number = 0

        return {"category_minimum": categories_min,
                "category_maximum": categories_max,
                "category_avenge": category_avenge,
                "agent_avenge_sample": agent_avenge_sample_number,
                "avenge_sample_number": avenge_sample_number,
                "max_samples": samples_max,
                "accuracy": self.accuracy(self, samples[border:], classes[border:])}
