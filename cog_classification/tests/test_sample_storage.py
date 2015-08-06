from itertools import izip_longest

from nose.tools import assert_equals, raises
from sklearn import datasets

from cog_classification.data_storage.sample_storage import SampleStorage
from cog_classification.core.environment import Environment


class TestSampleStorage:
    """
    Functions tested in TestSampleStorage:
    - add_sample
    - create_new_category
    - decrease_weights_in_category
    - export
    - increase_weights_in_category
    - remove_category
    - remove_sample_from_category
    - remove_weak_samples_from_category

    Functions not tested:
    - __init__
    - decrease_weights
    - empty
    - remove_weak_samples
    - sample_in_category
    - get_category_samples
    - get_category_samples_size
    - get_categories
    - get_categories_size
    - get_class
    - set_distance
    - set_weight
    """

    def __init__(self):
        self.storage = None

        irises = datasets.load_iris()
        self.env = Environment(irises.data, irises.target)

    def assert_size(self, number):
        assert_equals(self.storage.get_categories_size(), number)

    def assert_samples_size(self, number, category):
        assert_equals(self.storage.get_category_samples_size(category), number)

    def add(self, sample, environment=None, category=None, sample_weight=None):
        environment = environment or self.env

        self.storage.add_sample(sample, environment, category, sample_weight)

    def setup(self):
        self.storage = SampleStorage()

    def test_add_sample_classes_number(self):
        self.assert_size(0)

        # Adding new element to non existing class.
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        # Adding old element to existing class.
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        # Adding new element to existing class.
        self.add(11, category=1)
        self.assert_size(1)
        self.assert_samples_size(2, 1)

        # Adding new element to non existing class.
        self.add(31, category=2)
        self.assert_size(2)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)

        # Adding existing element to existing class.
        self.add(31, category=1)
        self.assert_size(2)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)

        # Adding new element to non existing class.
        self.add(41, category=3)
        self.assert_size(3)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element to existing class (different true categories).
        self.add(52, category=3)
        self.assert_size(4)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element to existing class (different true categories).
        self.add(53, category=1)
        self.assert_size(5)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element without class.
        self.add(54)
        self.assert_size(6)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        irises = datasets.load_iris()
        env = Environment(irises.data, irises.target)
        # Adding element with the same index but with different environment.
        self.add(1, env, 1)
        self.assert_size(6)
        self.assert_samples_size(3, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element with different environment and true class.
        self.add(63, env, 3)
        self.assert_size(7)
        self.assert_samples_size(3, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

    def test_add_sample_not_empty_after_adding(self):
        assert self.storage.empty()
        self.add(1)
        assert not self.storage.empty()

    def test_create_new_category_no_conflicts_with_analogous_category_names(self):
        self.add(1, category="Category number: 0")
        self.add(2, category="Category number: 1")
        self.add(3, category="Category number: 2")
        self.add(4, category="Category number: 4")

        self.assert_size(4)
        self.add(5)
        self.assert_size(5)
        self.add(6)
        self.assert_size(6)

        categories = self.storage.get_categories()

        for name in ["Category number: 3", "Category number: 5"]:
            find_class = False

            for c in categories:
                if name == c:
                    find_class = True
                    break

            assert find_class

    def test_decrease_weights_in_category_lowers_values(self):
        self.add(1, self.env, 1, 1)
        self.add(21, self.env, 1, 1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert_equals(weight, 1)

        self.storage.decrease_weights_in_category(1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert weight < 1

    def test_decrease_weights_in_category_no_under_zero(self):
        self.add(1, self.env, 1, 0.01)
        self.add(21, self.env, 1, 0.01)

        for _ in range(1000):
            self.storage.decrease_weights_in_category(1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert weight >= 0

    def test_export(self):
        samples1 = []
        classes1 = []

        irises = datasets.load_iris()

        for i in range(3):
            for j in range(0, 50, 5):
                self.add(i * 50 + j, category=i)
                samples1.append(irises.data[i * 50 + j])
                classes1.append(i)

        samples2, classes2 = self.storage.export()

        # Checking whether for every sample and class in samples1 and classes1
        # exist exactly same pair in samples2 and classes2.
        for sample1, class1 in izip_longest(samples1, classes1):
            pair_find = False
            for sample2, class2 in izip_longest(samples2, classes2):
                if (sample1 == sample2).all() and class1 == class2:
                    pair_find = True
                    break

            if not pair_find:
                print(sample1, class1)
                print(samples2, classes2)
            assert pair_find

        # Checking whether for every sample and class in samples2 and classes2
        # exist exactly same pair in samples1 and classes1.
        for sample2, class2 in izip_longest(samples2, classes2):
            pair_find = False
            for sample1, class1 in izip_longest(samples1, classes1):
                if (sample1 == sample2).all() and class1 == class2:
                    pair_find = True
                    break

            if not pair_find:
                print(sample2, class2)
                print(samples1, classes1)
            assert pair_find

    def test_increase_weights_in_category_higher_values(self):
        self.add(1, self.env, 1, 0)
        self.add(21, self.env, 1, 0)

        for _, _, weight in self.storage.get_category_samples(1):
            assert_equals(weight, 0)

        self.storage.increase_weights_in_category(1, self.env, 1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert weight > 0

    def test_increase_weights_in_category_no_over_one(self):
        self.add(1, self.env, 1, 1)
        self.add(21, self.env, 1, 1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert_equals(weight, 1)

        self.storage.increase_weights_in_category(1, self.env, 1)

        for _, _, weight in self.storage.get_category_samples(1):
            assert_equals(weight, 1)

    @raises(KeyError)
    def test_remove_category_from_empty_storage_fails(self):
        self.storage.remove_category(1)

    @raises(KeyError)
    def test_remove_category_other_category_fails(self):
        self.add(1, category=1)
        self.storage.remove_category(2)

    def test_remove_category_from_full_to_empty(self):
        self.test_add_sample_classes_number()
        categories = self.storage.get_categories()
        categories_size = self.storage.get_categories_size()

        for removed_category in categories:
            self.assert_size(categories_size)
            self.storage.remove_category(removed_category)
            categories_size -= 1

        self.assert_size(0)

    def test_remove_category_add_category_and_remove_category(self):
        self.assert_size(0)
        self.add(1, category=1)
        self.assert_size(1)
        self.storage.remove_category(1)
        self.assert_size(0)
        self.add(1, category=1)
        self.assert_size(1)
        assert 1 in self.storage.get_categories()

    @raises(KeyError)
    def test_remove_sample_from_category_empty_storage_fails(self):
        self.storage.remove_sample_from_category(self.env, 1, sample_index=1)

    @raises(TypeError)
    def test_remove_sample_from_category_storage_without_sample(self):
        self.storage.add_sample(1, self.env, 1)
        self.storage.remove_sample_from_category(self.env, 1, sample=11)

    @raises(KeyError)
    def test_remove_sample_from_category_other_category_fails(self):
        self.add(1, category=1)
        self.storage.remove_sample_from_category(self.env, 2, sample_index=1)

    def test_remove_sample_from_category_last_sample_removes_category(self):
        self.add(1, category=1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        self.storage.remove_sample_from_category(self.env, 1, sample_index=1)
        self.assert_size(0)

    @raises(KeyError)
    def test_remove_weak_samples_from_category_no_category(self):
        self.storage.remove_weak_samples_from_category(1)

    def test_remove_weak_samples_from_category_removes_category(self):
        self.add(1, self.env, 1, 0)
        self.add(11, self.env, 1, 0)
        self.add(21, self.env, 1, 0)

        self.assert_size(1)
        self.storage.remove_weak_samples_from_category(1)
        self.assert_size(0)

    def test_remove_weak_samples_from_category_doesnt_affect_other_categories(self):
        self.add(1, self.env, 1, 0)
        self.add(21, self.env, 1, 0)
        self.add(31, self.env, 1, 0)

        self.add(12, self.env, 2, 0)
        self.add(23, self.env, 3, 0)
        self.add(34, self.env, 4, 0)

        self.assert_size(4)
        self.storage.remove_weak_samples_from_category(1)
        self.assert_size(3)
