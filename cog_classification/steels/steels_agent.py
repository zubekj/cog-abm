from cog_classification.core.agent import Agent
from cog_classification.steels.lexicon import Lexicon


class SteelsAgent(Agent):
    """
    Class representing universal steels agent in the system.

    :param hashable aid: agent's id. Unique identifier of agent.
    :param lexicon lexicon: agent's storage of associations between categories and words.

    Steels agent can associate words with categories but cannot remember samples from environment.
    """

    def __init__(self, aid=None, lexicon=None):
        Agent.__init__(self, aid)
        self.lexicon = lexicon or Lexicon()

    def add_word_to_category(self, word, category):
        return self.lexicon.add_word_to_category(word, category)

    def decrease_weight_word_category(self, word, category):
        self.lexicon.decrease_weight(word, category)

    def find_category_for_word(self, word):
        return self.lexicon.find_category_for_word(word)

    def increase_weight_word_category(self, word, category):
        self.lexicon.increase_weight(word, category)

    def decrease_weights_for_other_categories(self, word, category):
        self.lexicon.decrease_weights_for_other_categories(word, category)

    def decrease_weights_for_other_words(self, word, category):
        self.lexicon.decrease_weights_for_other_words(word, category)

    def find_word_for_category(self, category):
        return self.lexicon.find_word_for_category(category)

    def get_words(self):
        return self.lexicon.get_words()
