""" Module implementing steels agent used in simulation. """

from cog_classification.steels_universal.steels_agent import SteelsAgent

class SteelsSimulationAgent(SteelsAgent):

    def __init__(self, aid=None, lexicon=None, adaptive_network=None):
        SteelsAgent.__init__(self, aid, lexicon)
        self.adaptive_network = adaptive_network

    def add_sample(self, sample_index, environment, category=None):
        pass

    def choose_the_best_sample_for_category(self, category, samples):
        pass

    def classify(self, sample):
        pass

    def forget(self):
        pass

    def strengthen_memory_sample_category(self, category, sample_index, environment):
        pass
