import random


class Lexicon:

    def __init__(self, dictionary=None, classes=None, increase_strength=0.1, lateral_inhibition=0.1,
                 decrease_strength=0.1, initial_strength=0.5, min_strength=0, max_strength=1):
        self.dictionary = dictionary or {}
        self.classes = classes or {}

        self.increase_strength = increase_strength
        self.lateral_inhibition = lateral_inhibition
        self.decrease_strength = decrease_strength
        self.initial_strength = initial_strength
        self.min_strength = min_strength
        self.max_strength = max_strength

    def add_new_category(self, category, word=None, weight=None):
        weight = weight or self.initial_strength

        if word is None:
            new_word = random.choice(range(10000))
            while new_word in self.dictionary:
                new_word = random.choice(range(10000))
            word = new_word

        if word not in self.dictionary:
            self.dictionary[word] = {category: weight}

        self.classes[category] = [word]

        return word

    @staticmethod
    def _find_best_element(dictionary, chooser):
        best_element = None
        best_weight = -float('inf')
        for element in dictionary:
            element_weight = chooser(dictionary[element])
            if element_weight > best_weight:
                best_element = element
                best_weight = element_weight

        return best_element

    def word_for_category(self, category):
        best_word = None
        best_weight = -float('inf')

        for word in self.classes[category]:
            element_weight = self.dictionary[word][category]
            if element_weight > best_weight:
                best_word = word
                best_weight = element_weight

        return best_word

    def category_for_word(self, word):
        best_category = None
        best_weight = -float('inf')

        for category in self.dictionary[word]:
            element_weight = self.dictionary[word][category]
            if element_weight > best_weight:
                best_category = category
                best_weight = element_weight

        return best_category

    def strengthen_association(self, word, category):
        self.dictionary[word][category] += self.increase_strength

    def weaken_other_associations(self, word, category):
        for other_word in self.classes(category):
            if not other_word == word:
                self.dictionary[word][category] -= self.lateral_inhibition

    def weaken_association(self, word, category):
        self.dictionary[word][category] -= self.decrease_strength

    def get_words(self):
        return self.dictionary
