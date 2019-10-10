import random
from collections import defaultdict


class Lexicon(object):
    """
    Storage of associations between categories and words.

    :param dictionary dictionary: representation of associations between words and categories. \
        Words are keys and dictionaries - {category: weight} are values.
    :param dictionary categories: represents lists of words that have association with given category. \
        Categories are keys and lists of words are values.
    :param float min_weight: minimal weight of association. Values from 0 to infinity.
    :param float max_weight: maximal weight of association. Values from min weight to infinity.
    :param float new_weight: the weight of new association added to lexicon. Value form min_weight to max weight.
    :param float weight_increase: how much weight of association will be increased. Value from 0 to max weight.
    :param float weight_decrease: how much weights of associations will be decreased when we inhibit associations \
        between category and words. value from 0 to max weight.
    :param float lateral_inhibition: how much weights of associations will be decreased when we inhibit associations \
        between word and categories. value from 0 to max weight.
    :param long word_range: the size of pool of words in word generator. \
        The generated words are longs from range(word_range). Value from 0 to infinity.

    Every word can be associated with multiple categories and vice versa.

    Association is described by weight.
    """

    def __init__(self, min_weight=0, max_weight=1, new_weight=0.5,
                 weight_increase=0.1, weight_decrease=0.1,
                 lateral_inhibition=0.1, word_range=100000):

        assert min_weight >= 0
        self.min_weight = min_weight

        assert max_weight >= min_weight
        self.max_weight = max_weight

        assert new_weight >= min_weight
        assert new_weight <= max_weight
        self.new_weight = new_weight

        assert weight_increase >= 0
        assert weight_increase <= max_weight
        self.weight_increase = weight_increase

        assert lateral_inhibition >= 0
        assert lateral_inhibition <= max_weight
        self.lateral_inhibition = lateral_inhibition

        assert weight_decrease >= 0
        assert weight_decrease <= max_weight
        self.weight_decrease = weight_decrease

        assert word_range > 0
        self.word_range = word_range

        # Dictionary: {word: {category: weight}}
        self.word2cat = defaultdict(lambda: defaultdict(lambda: self.new_weight))
        # Dictionary: {category: {word: weight}}
        self.cat2word = defaultdict(lambda: defaultdict(lambda: self.new_weight))

    def update_weight(self, word, category, weight=None):
        """
        Sets association's weight between word and category.

        :param hashable word: the word.
        :param hashable category: the category.

        If word and category don't have any association yet, then new association between them is added.
        """
        if weight is None:
            weight = self.new_weight
        new_weight = max(self.min_weight, min(self.max_weight, weight))
        self.cat2word[category][word] = new_weight
        self.word2cat[word][category] = new_weight

    def decrease_weight(self, word, category):
        """
        Decreases association's weight between word and category.

        :param hashable word: the word.
        :param hashable category: the category.

        :raise: **KeyError** - if word isn't in lexicon or no association between word and category.
        """
        new_weight = self.word2cat[word][category] - self.weight_decrease
        self.update_weight(word, category, new_weight)

    def increase_weight(self, word, category):
        """
        Increases association's weight between word and category.

        :param hashable word: the word.
        :param hashable category: the category.

        :raise: **KeyError** - if word isn't in lexicon or no association between word and category.
        """
        new_weight = self.word2cat[word][category] + self.weight_increase
        self.update_weight(word, category, new_weight)

    def decrease_weights_for_other_categories(self, word, category):
        """
        Decreases association's weights between categories other than specified and word.

        :param hashable word: the word.
        :param hashable category: the only category which association's weight won't be decreased.

        :raise: **KeyError** - if word isn't in lexicon.
        """
        for other_category in self.word2cat[word]:
            if not other_category == category:
                new_weight = self.word2cat[word][other_category] - self.lateral_inhibition
                self.update_weight(word, other_category, new_weight)

    def decrease_weights_for_other_words(self, word, category):
        """
        Decreases association's weights between words other than specified and category.

        :param hashable word: the only word, which association's weight won't be decreased.
        :param hashable category: the category.

        :raise: **KeyError** - if word or category isn't in lexicon or no association between word and category.
        """
        for other_word in self.cat2word[category]:
            if not other_word == word:
                new_weight = self.cat2word[category][other_word] - self.lateral_inhibition
                self.update_weight(other_word, category, new_weight)

    def find_category_for_word(self, word):
        """
        Finds category with the strongest association with word.

        :param hashable word: the word for which the best category is searched.

        :return: the category with the strongest association with word or None if word isn't in lexicon.
        :rtype: hashable or None
        """
        if word not in self.word2cat:
            return None
        return max(self.word2cat[word], key=lambda k: self.word2cat[word][k])

    def find_word_for_category(self, category):
        """
        Finds word with the strongest association with category.

        :param hashable category: the category for which the best word is searched.

        :return: the word with the strongest association with category.
        :rtype: hashable or None
        """
        if category not in self.cat2word:
            return None
        return max(self.cat2word[category], key=lambda k: self.cat2word[category][k])

    def generate_word(self):
        """
        :return: new word that isn't in lexicon.
        :rtype: long
        """
        new_word = random.randrange(self.word_range)
        while new_word in self.word2cat:
            new_word = random.randrange(self.word_range)
        return new_word

    def get_categories(self):
        """
        :return: all categories of lexicon.
        :rtype: list of hashable
        """
        return self.cat2word.keys()

    def get_categories_size(self):
        """
        :return: number of categories in the lexicon.
        :rtype: long
        """
        return len(self.cat2word)

    def get_words(self):
        """
        :return: all words of lexicon.
        :rtype: list of hashable
        """
        return self.word2cat.keys()

    def get_words_size(self):
        """
        :return: number of words in the lexicon.
        :rtype: long
        """
        return len(self.word2cat)

    def remove_category(self, category):
        """
        Removes given category.

        :param hashable category: the category to remove.

        If it was the last category for word it removes this word, too.
        """
        if category not in self.cat2word:
            return

        cat_words = self.cat2word[category].keys()

        for word in cat_words:
            self.word2cat[word].pop(category)
            if len(self.word2cat[word]) == 0:
                self.word2cat.pop(word)

        self.cat2word.pop(category)
