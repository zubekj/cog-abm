from sklearn.utils.validation import NotFittedError

from cog_classification.core.environment import Environment
from cog_classification.core.fitness import CurrentFitness
from cog_classification.core.network import Network
from cog_classification.core.simulation import Simulation
from cog_classification.core.condition import IterationCondition
from steels_classifier_results import SteelsClassifierResults
from cog_classification.steels_universal.guessing_game import GuessingGame
from steels_classification_agent import SteelsClassificationAgent
from cog_classification.tools.topology_generator import generate_topology
from cog_classification.core.behavior_switcher import BehaviorSwitcher


class SteelsClassifier:
    """
    Classifier founded on Steels and Belpaeme multi-agent network and interactions concept.

    :param classifiers: Classifiers that will be used with agents creation.
    :type classifiers: List of classifiers.
    """

    def __init__(self, classifiers=None):
        self.classifiers = classifiers
        self.simulation = None
        self.result = None
        self.condition = IterationCondition(1000)
        self.interactions = BehaviorSwitcher(GuessingGame())

    def fit(self, x, y):
        """
        Fit the steels classifier according to the given training data.

        :param list x: Samples.
        :param list y: Samples' classes.
        """

        environment = Environment(x, y)

        agents = {}

        if self.classifiers is None:
            for _ in range(10):
                agent = SteelsClassificationAgent()
                agents[agent.id] = agent
        else:
            for classifier in self.classifiers:
                agent = SteelsClassificationAgent(classifier=classifier)
                agents[agent.id] = agent

        for agent in agents.values():
            agent.set_fitness("DG", CurrentFitness())
            agent.set_fitness("GG", CurrentFitness())

        network = Network(agents, {1: generate_topology("clique", agents_names=agents.keys())})

        self.simulation = Simulation(network, self.interactions, BehaviorSwitcher(environment),
                                     SteelsClassifierResults(), self.condition)

        self.result = self.simulation.run()

    def predict(self, sample):
        """
        :param sample: The sample which class is predicted.

        :raise: **NotFittedError** - if no data have been fitted yet.

        :return: The predicted class of sample.
        :rtype: hashable
        """
        if self.result is not None:
            return self.result.predict(sample)
        else:
            raise NotFittedError
