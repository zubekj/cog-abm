from nose.tools import assert_equals
import random

from cog_classification.core.agent import Agent

from test_sample_storage import DummyEnvironment

import numpy as np


class TestAgent:

    def __init__(self):
        self.agent = None
        self.environment = None
        pass

    def add_topic_to_class(self, category, topic, environment=None):
        environment = environment or self.environment
        self.agent.add_topic_to_class(category, topic, environment)

    def setup(self):
        self.agent = Agent()
        # sample_storage=SampleStorage()
        self.environment = DummyEnvironment()

    def test_add_topic_to_class(self):
        self.add_topic_to_class(1, 1)

    def test_set_fitness(self):
        self.agent.set_fitness("DF", DummyFitness())
        assert_equals(self.agent.get_fitness_measure("DF"), 0)

    def test_learning_cycle(self):
        self.add_topic_to_class(1, 1)
        self.add_topic_to_class(2, 2)
        self.agent.learn()
        assert_equals(self.agent.classify(np.array([1])), [1])
        assert_equals(self.agent.classify(np.array([2])), [2])

    def test_single_classification_game_iterations(self):
        random.seed()
        self.agent.set_fitness("DF", DummyFitness())
        for _ in range(100):
            self.agent.learn()
            x = random.choice(range(10))
            c = self.agent.classify(np.array([x]))
            if [x % 10] == c:
                self.agent.good_category_for_topic(c[0], x, self.environment)
                value = 1
            else:
                if self.agent.get_fitness_measure("DF") > 0.95:
                    self.agent.good_category_for_topic(c[0], x, self.environment)
                    value = 0
                else:
                    self.agent.add_topic_to_new_class(x, self.environment)
                    value = 0

            self.agent.update_fitness("DF", value)
            self.agent.forget()


class DummyFitness:

    def __init__(self):
        self.success = 0
        self.all = 0

    def get_measure(self):
        if self.all == 0:
            return 0
        else:
            return self.success / self.all

    def update(self, value):
        self.all += 1
        self.success += value
