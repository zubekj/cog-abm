import random


class Lexicon:
    """
    Class that contains information about associations between words and categories.

    Every word can be associated with multiple categories and vice versa.

    Association is described by weight.
    """

    def __init__(self, dictionary=None, classes=None, increase_strength=0.1, lateral_inhibition=0.1,
                 decrease_strength=0.1, initial_strength=0.5, min_strength=0, max_strength=1):
        """
        Parameters explanation:
        dictionary - dictionary which represents association between words and categories.
        Keys are words and values are dictionaries {category: weight}.
        categories - dictionary which represents association between categories and words.
        Keys are words and values are lists of words.
        increase_strength - how much increase association strength when strengthen
        lateral_inhibition - how much decrease association strength
            when weaken associations for list of words for category
            or for list of categories for word
        decrease_strength - how much decrease association strength
            when weaken association between specified word and category
        initial_strength - default strength in new association
        min_strength - minimal strength of association
        max_strength - maximal strength of association
        """
        self.dictionary = dictionary or {}
        self.classes = classes or {}

        self.increase_strength = increase_strength
        self.lateral_inhibition = lateral_inhibition
        self.decrease_strength = decrease_strength
        self.initial_strength = initial_strength
        self.min_strength = min_strength
        self.max_strength = max_strength

    def add_new_category(self, category, word=None, weight=None):
        """
        Adds new category to lexicon.

        If word isn't specified lexicon creates new unique word for category.
        If weight isn't specified lexicon uses initial strength.
        """
        weight = weight or self.initial_strength

        if word is None:
            new_word = random.randrange(10000)
            while new_word in self.dictionary:
                new_word = random.randrange(10000)
            word = new_word

        if word not in self.dictionary:
            self.dictionary[word] = {category: weight}

        self.classes[category] = [word]

        return word

    def word_for_category(self, category):
        """
        Finds word with the strongest association with category.
        """
        best_word = None
        best_weight = -float('inf')

        for word in self.classes[category]:
            element_weight = self.dictionary[word][category]
            if element_weight > best_weight:
                best_word = word
                best_weight = element_weight

        return best_word

    def category_for_word(self, word):
        """
        Finds category with the strongest association with word.
        """
        best_category = None
        best_weight = -float('inf')

        for category in self.dictionary[word]:
            element_weight = self.dictionary[word][category]
            if element_weight > best_weight:
                best_category = category
                best_weight = element_weight

        return best_category

    def strengthen_association(self, word, category):
        """
        Strengthen association between word and category.
        """
        self.dictionary[word][category] += self.increase_strength

    def weaken_other_associations_for_words(self, word, category):
        """
        Weaken association between words other than specified and category.
        """
        for other_word in self.classes(category):
            if not other_word == word:
                self.dictionary[word][category] -= self.lateral_inhibition

    def weaken_other_associations_for_categories(self, word, category):
        """
        Weaken association between categories other than specified and word.
        """
        for other_category in self.dictionary[word]:
            if not other_category == category:
                self.dictionary[word][category] -= self.lateral_inhibition

    def weaken_association(self, word, category):
        """
        Weaken association between word and category.
        """
        self.dictionary[word][category] -= self.decrease_strength

    def get_words(self):
        """
        Returns all known words.
        """
        return self.dictionary
