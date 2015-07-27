from nose.tools import assert_equals

from cog_classification.core.lexicon import Lexicon


class TestLexicon:

    def __init__(self):
        self.lexicon = None

    def setup(self):
        self.lexicon = Lexicon()

    def test_add_new_category(self):
        assert_equals(self.lexicon.add_new_category(1, 1), 1)
        assert_equals(self.lexicon.add_new_category(2, 2), 2)
        assert_equals(self.lexicon.add_new_category(3, 3), 3)

    def test_word_for_category(self):
        self.test_add_new_category()
        assert_equals(self.lexicon.word_for_category(1), 1)
        assert_equals(self.lexicon.word_for_category(2), 2)
        assert_equals(self.lexicon.word_for_category(3), 3)

    def test_category_for_word(self):
        self.test_add_new_category()
        assert_equals(self.lexicon.category_for_word(1), 1)
        assert_equals(self.lexicon.category_for_word(2), 2)
        assert_equals(self.lexicon.category_for_word(3), 3)