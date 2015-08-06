""" Module implementing universal steels agent in the system. """

from cog_classification.core.agent import Agent
from cog_classification.data_storage.lexicon import Lexicon


class SteelsAgent(Agent):
    """
    Class representing agent in the system.

    SteelsAgent remember old samples from environment and can classify new ones. It can name categories.

    SteelsAgent has some mechanisms that will help it forget the samples if needed.

    There is an option of monitoring agent fitness.
    """

    def __init__(self, aid=None, lexicon=None):
        """
        Parameters explanation:
        aid - an agent id
        classifier - machine learning algorithm
            which implements functions fit and predict as defined in sklearn library.
        sample_storage - storage all samples used to teach classifier
        lexicon - storage associations between sample storage categories and words.
        """
        Agent.__init__(self, aid)
        self.lexicon = lexicon or Lexicon()

    def add_word_to_category(self, word, category):
        self.get_categories_size()
        return self.lexicon.add_word_to_category(word, category)
        self.get_categories_size()

    def weaken_association_word_category(self, word, category):
        """
        Weakens association between word and category in lexicon.
        """
        self.lexicon.weaken_association(word, category)

    def find_category_for_word(self, word):
        return self.lexicon.find_category_for_word(word)

    def strengthen_association_word_category(self, word, category):
        """
        Strengthen association between word and category.
        """
        self.lexicon.strengthen_association(word, category)

    def weaken_association_word_other_categories(self, word, category):
        """
        Weakens associations between other categories and word.
        """
        self.lexicon.weaken_other_associations_for_categories(word, category)

    def weaken_association_other_word_categories(self, word, category):
        """
        Weakens associations between other words and category.
        """
        self.lexicon.weaken_other_associations_for_words(word, category)

    def find_word_for_category(self, category):
        return self.lexicon.find_word_for_category(category)

    def get_words(self):
        """
        Returns all words known by agents.
        """
        return self.lexicon.get_words()
