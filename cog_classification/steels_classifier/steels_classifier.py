from sklearn.utils.validation import NotFittedError

from cog_classification.core.environment import Environment
from cog_classification.core.fitness import CurrentFitness
from cog_classification.core.network import Network
from cog_classification.core.simulation import Simulation
from cog_classification.core.condition import IterationCondition
from steels_classifier_results import SteelsClassifierResults
from cog_classification.steels_universal.guessing_game import GuessingGame
from cog_classification.steels_universal.steels_agent import SteelsAgent
from cog_classification.tools.topology_generator import generate_topology
from cog_classification.data_storage.changing_class import ChangingClass


class SteelsClassifier:
    """
    Classifier founded on Steels and Belpaeme multi-agent network and interactions concept.
    """

    def __init__(self, classifiers=None):
        """
        Args:
            classifiers (list): list of classifiers that will be used with agents creation.
        """
        self.classifiers = classifiers
        self.simulation = None
        self.result = None
        self.condition = IterationCondition(1000)
        self.interactions = ChangingClass({'i': GuessingGame()}, {1: 'i'})

    def fit(self, x, y):
        """
            Fit the steels classifier according to the given training data.

            Args:
                x (list): list of samples.
                y (list): list of samples' classes.
        """

        environment = Environment(x, y)

        agents = {}

        if self.classifiers is None:
            for _ in range(10):
                agent = SteelsAgent()

                agents[agent.get_id()] = agent
        else:
            for classifier in self.classifiers:
                agent = SteelsAgent(classifier=classifier)
                agents[agent.get_id()] = agent

        for agent in agents.values():
            agent.set_fitness("DG", CurrentFitness())
            agent.set_fitness("GG", CurrentFitness())

        network = Network(agents, {'a': generate_topology("clique", agents_names=agents.keys())}, {1: 'a'})

        self.simulation = Simulation(network, self.interactions, ChangingClass({'e': environment}, {1: 'e'}),
                                     SteelsClassifierResults(), self.condition)

        self.result = self.simulation.run()

    def predict(self, sample):
        if self.result is not None:
            return self.result.predict(sample)
        else:
            raise NotFittedError
