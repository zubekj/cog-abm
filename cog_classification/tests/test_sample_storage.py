from nose.tools import assert_equals, raises

from cog_classification.core.sample_storage import SampleStorage

from itertools import izip_longest

import numpy as np


class DummyEnvironment:

    def __init__(self):
        pass

    @staticmethod
    def get_true_class(i):
        return i % 10

    @staticmethod
    def get_sample(i):
        return np.array([i])

    @staticmethod
    def get_samples(indexes):
        return np.array(indexes)


class TestSampleStorage:
    """
    Functions tested in TestSampleStorage:
    - add_sample
    - create_new_class
    - decrease_weights_in_class
    - export
    - increase_weights_in_class
    - remove_class
    - remove_sample_from_class
    - remove_weak_samples_from_class

    Functions not tested:
    - decrease_weights
    - empty
    - remove_weak_samples
    - sample_in_class
    - standard_distance
    - get_class_number
    - get_class_samples
    - get_class_samples_size
    - get_classes
    - get_classes_number
    - get_true_class
    - set_distance
    - set_weight
    """

    def __init__(self):
        self.storage = None
        self.env = None

    def assert_size(self, number):
        assert_equals(self.storage.get_classes_number(), number)

    def assert_samples_size(self, number, target_class):
        assert_equals(self.storage.get_class_samples_size(target_class), number)

    @staticmethod
    def make_numpy_array(s_list):
        return np.array(s_list)

    def setup(self):
        self.storage = SampleStorage()
        self.env = DummyEnvironment()

    def test_add_sample_classes_number(self):
        self.assert_size(0)

        # Adding new element to non existing class.
        self.storage.add_sample(1, self.env, 1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        # Adding old element to existing class.
        self.storage.add_sample(1, self.env, 1)
        self.assert_size(1)
        self.assert_samples_size(1, 1)

        # Adding new element to existing class.
        self.storage.add_sample(11, self.env, 1)
        self.assert_size(1)
        self.assert_samples_size(2, 1)

        # Adding new element to non existing class.
        self.storage.add_sample(31, self.env, 2)
        self.assert_size(2)
        self.assert_samples_size(2, 1)
        self.assert_samples_size(1, 2)

        # Adding new element to existing class.
        self.storage.add_sample(31, self.env, 1)
        self.assert_size(2)
        self.assert_samples_size(3, 1)
        self.assert_samples_size(1, 2)

        # Adding new element to non existing class.
        self.storage.add_sample(41, self.env, 3)
        self.assert_size(3)
        self.assert_samples_size(3, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element to existing class (different true classes).
        self.storage.add_sample(42, self.env, 3)
        self.assert_size(4)
        self.assert_samples_size(3, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element to existing class (different true classes).
        self.storage.add_sample(52, self.env, 1)
        self.assert_size(5)
        self.assert_samples_size(3, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

        # Adding new element without class.
        self.storage.add_sample(52, self.env)
        self.assert_size(6)
        self.assert_samples_size(3, 1)
        self.assert_samples_size(1, 2)
        self.assert_samples_size(1, 3)

    def test_add_sample_not_empty_after_adding(self):
        assert_equals(self.storage.empty(), True)
        self.storage.add_sample(1, self.env, 1)
        assert_equals(self.storage.empty(), False)

    def test_create_new_class_no_conflicts_with_analogous_class_names(self):
        self.storage.add_sample(1, self.env, "Class number: 0")
        self.storage.add_sample(1, self.env, "Class number: 1")
        self.storage.add_sample(1, self.env, "Class number: 2")
        self.storage.add_sample(1, self.env, "Class number: 4")

        self.assert_size(4)
        self.storage.add_sample(1, self.env)
        self.assert_size(5)
        self.storage.add_sample(1, self.env)
        self.assert_size(6)

        classes = self.storage.get_classes()

        for name in ["Class number: 3", "Class number: 5"]:
            find_class = False

            for c in classes:
                if name == c:
                    find_class = True
                    break

            assert find_class

    def test_decrease_weights_in_class_lowers_values(self):
        self.storage.add_sample(1, self.env, 1, 1)
        self.storage.add_sample(21, self.env, 1, 1)

        for _, _, weight in self.storage.get_class_samples(1):
            assert_equals(weight, 1)

        self.storage.decrease_weights_in_class(1)

        for _, _, weight in self.storage.get_class_samples(1):
            assert weight < 1

    def test_decrease_weights_in_class_no_under_zero(self):
        self.storage.add_sample(1, self.env, 1, 0.01)
        self.storage.add_sample(21, self.env, 1, 0.01)

        for _ in range(1000):
            self.storage.decrease_weights_in_class(1)

        for _, _, weight in self.storage.get_class_samples(1):
            assert weight > 0

    def test_export(self):
        true_data = []
        true_decisions = []

        for j in range(9):
            for i in range(9):
                self.storage.add_sample(i * 10 + j, self.env, j)
                true_data.append([i * 10 + j])
                true_decisions.append(j)

        data, decisions = self.storage.export()

        # Checking whether for every value decision pair in data and decisions
        # exist exactly same value pair in true data and true decisions.
        for value, decision in izip_longest(data, decisions):
            pair_find = False
            for true_value, true_decision in izip_longest(true_data, true_decisions):
                if value == true_value and decision == true_decision:
                    pair_find = True
                    break

            if not pair_find:
                print(value, decision)
                print(true_data, true_decisions)
            assert pair_find

        # Checking whether for every value, decision pair in true data and true decisions
        # exist exactly same value, decision pair in data and decisions.
        for true_value, true_decision in izip_longest(true_data, true_decisions):
            pair_find = False
            for value, decision in izip_longest(data, decisions):
                if value == true_value and decision == true_decision:
                    pair_find = True
                    break
            assert pair_find

    def test_increase_weights_in_class_higher_values(self):
        self.storage.add_sample(1, self.env, 1, 0)
        self.storage.add_sample(21, self.env, 1, 0)

        for _, _, weight in self.storage.get_class_samples(1):
            assert_equals(weight, 0)

        self.storage.increase_weights_in_class(1, self.env, 1)

        for _, _, weight in self.storage.get_class_samples(1):
            assert weight > 0

    def test_increase_weights_in_class_no_over_one(self):
        self.storage.add_sample(1, self.env, 1, 1)
        self.storage.add_sample(21, self.env, 1, 1)

        for _, _, weight in self.storage.get_class_samples(1):
            assert_equals(weight, 1)

        self.storage.increase_weights_in_class(1, self.env, 1)

        for _, _, weight in self.storage.get_class_samples(1):
            assert_equals(weight, 1)

    @raises(KeyError)
    def test_remove_class_from_empty_storage_fails(self):
        self.storage.remove_class(1)

    @raises(KeyError)
    def test_remove_class_other_class_fails(self):
        self.storage.add_sample(1, self.env, 1, 1)
        self.storage.remove_class(2)

    def test_remove_class_from_full_to_empty(self):
        self.test_add_sample_classes_number()
        classes = self.storage.get_classes()
        classes_number = self.storage.get_classes_number()

        for removed_class in classes:
            self.assert_size(classes_number)
            self.storage.remove_class(removed_class)
            classes_number -= 1

        self.assert_size(0)

    def test_remove_class_add_class_and_remove_class(self):
        self.assert_size(0)
        self.storage.add_sample(1, self.env, 1, 1)
        self.assert_size(1)
        self.storage.remove_class(1)
        self.assert_size(0)
        self.storage.add_sample(1, self.env, 1, 1)
        self.assert_size(1)
        assert 1 in self.storage.get_classes()

    @raises(KeyError)
    def test_remove_sample_from_class_empty_storage_fails(self):
        self.storage.remove_sample_from_class(1, self.env, self.env)

    def test_remove_sample_from_class_storage_without_sample(self):
        self.storage.add_sample(1, self.env, 1)
        self.storage.remove_sample_from_class(11, self.env, 1)

    @raises(KeyError)
    def test_remove_sample_from_class_other_class_fails(self):
        self.storage.add_sample(1, self.env, 1)
        self.storage.remove_sample_from_class(1, self.env, 2)

    def test_remove_sample_from_class_last_sample_removes_class(self):
        self.storage.add_sample(1, self.env, 1)
        self.assert_size(1)
        assert_equals(1, self.storage.get_class_samples_size(1))

        self.storage.remove_sample_from_class(1, self.env, 1)
        self.assert_size(0)

    @raises(KeyError)
    def test_remove_weak_samples_from_class_no_class(self):
        self.storage.remove_weak_samples_from_class(1)

    def test_remove_weak_samples_from_class_removes_class(self):
        self.storage.add_sample(1, self.env, 1, 0)
        self.storage.add_sample(11, self.env, 1, 0)
        self.storage.add_sample(21, self.env, 1, 0)

        self.assert_size(1)
        self.storage.remove_weak_samples_from_class(1)
        self.assert_size(0)

    def test_remove_weak_samples_from_class_doesnt_affect_other_classes(self):
        self.storage.add_sample(1, self.env, 1, 0)
        self.storage.add_sample(21, self.env, 1, 0)
        self.storage.add_sample(31, self.env, 1, 0)

        self.storage.add_sample(12, self.env, 2, 0)
        self.storage.add_sample(23, self.env, 3, 0)
        self.storage.add_sample(34, self.env, 4, 0)

        self.assert_size(4)
        self.storage.remove_weak_samples_from_class(1)
        self.assert_size(3)
