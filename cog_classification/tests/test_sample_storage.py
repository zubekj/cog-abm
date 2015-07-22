from nose.tools import assert_equals, raises

from cog_classification.core.sample_storage import SampleStorage

from itertools import izip_longest


class SimpleSample:

        def __init__(self, number):
            self.number = number

        def distance(self, number):
            return abs(self.number - number.get_attributes()[0])

        def get_attributes(self):
            return [self.number]


class TestSampleStorage:

    def __init__(self):
        self.test_storage = SampleStorage()

    def assert_size(self, number):
        assert_equals(self.test_storage.get_classes_number(), number)

    def setup(self):
        self.test_storage = SampleStorage()

    def test_add_sample_not_empty_after_adding(self):
        assert_equals(self.test_storage.empty(), True)
        self.test_storage.add_sample(SimpleSample(1), 1)
        assert_equals(self.test_storage.empty(), False)

    def test_add_sample_classes_number(self):
        self.assert_size(0)

        # Adding new element to non existing class.
        self.test_storage.add_sample(SimpleSample(1), 1, 1)
        self.assert_size(1)

        # Adding old element to existing class.
        self.test_storage.add_sample(SimpleSample(1), 1, 1)
        self.assert_size(1)

        # Adding new element to existing class.
        self.test_storage.add_sample(SimpleSample(2), 1, 1)
        self.assert_size(1)

        # Adding new element to non existing class.
        self.test_storage.add_sample(SimpleSample(3), 1, 2)
        self.assert_size(2)

        # Adding new element to existing class.
        self.test_storage.add_sample(SimpleSample(3), 1, 1)
        self.assert_size(2)

        # Adding new element to non existing class.
        self.test_storage.add_sample(SimpleSample(4), 1, 3)
        self.assert_size(3)

        # Adding old element to existing class (different true classes).
        self.test_storage.add_sample(SimpleSample(4), 2, 3)
        self.assert_size(4)

        # Adding new element to existing class (different true classes).
        self.test_storage.add_sample(SimpleSample(5), 2, 1)
        self.assert_size(5)

        # Adding new element without class.
        self.test_storage.add_sample(SimpleSample(5), 2)
        self.assert_size(6)

    def test_decrease_weights_in_class_lowers_values(self):
        self.test_storage.add_sample(SimpleSample(1), 1, 1, 1)
        self.test_storage.add_sample(SimpleSample(2), 1, 1, 1)

        for _, weight in self.test_storage.get_class_samples(1):
            assert_equals(weight, 1)

        self.test_storage.decrease_weights_in_class(1)

        for _, weight in self.test_storage.get_class_samples(1):
            assert weight < 1

    def test_decrease_weights_in_class_no_under_zero(self):
        self.test_storage.add_sample(SimpleSample(1), 1, 1, 0.01)
        self.test_storage.add_sample(SimpleSample(2), 1, 1, 0.01)

        for _ in range(1000):
            self.test_storage.decrease_weights_in_class(1)

        for _, weight in self.test_storage.get_class_samples(1):
            assert weight > 0

    def test_export(self):
        true_data = []
        true_decisions = []

        for j in range(4, 40, 5):
            for i in range(j, j + 3):
                self.test_storage.add_sample(SimpleSample(i), j)
                true_data.append([i])
                true_decisions.append(j)

        data, decisions = self.test_storage.export()

        # Checking whether for every value decision pair in data and decisions
        # exist exactly same value pair in true data and true decisions.
        for value, decision in izip_longest(data, decisions):
            pair_find = False
            for true_value, true_decision in izip_longest(true_data, true_decisions):
                if value == true_value and decision == true_decision:
                    pair_find = True
                    break
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
        self.test_storage.add_sample(SimpleSample(1), 1, 1, 0)
        self.test_storage.add_sample(SimpleSample(2), 1, 1, 0)

        for _, weight in self.test_storage.get_class_samples(1):
            assert_equals(weight, 0)

        self.test_storage.increase_weights_in_class(SimpleSample(1), 1)

        for _, weight in self.test_storage.get_class_samples(1):
            assert weight > 0

    def test_increase_weights_in_class_no_over_one(self):
        self.test_storage.add_sample(SimpleSample(1), 1, 1, 1)
        self.test_storage.add_sample(SimpleSample(2), 1, 1, 1)

        for _, weight in self.test_storage.get_class_samples(1):
            assert_equals(weight, 1)

        self.test_storage.increase_weights_in_class(SimpleSample(1), 1)

        for _, weight in self.test_storage.get_class_samples(1):
            assert_equals(weight, 1)

    @raises(KeyError)
    def test_remove_class_from_empty_storage_fails(self):
        self.test_storage.remove_class(1)

    @raises(KeyError)
    def test_remove_class_other_class_fails(self):
        self.test_storage.add_sample(SimpleSample(1), 1, 1, 1)
        self.test_storage.remove_class(2)

    def test_remove_class_from_full_to_empty(self):
        self.test_add_sample_classes_number()
        classes = self.test_storage.get_classes()
        classes_number = self.test_storage.get_classes_number()

        for removed_class in classes:
            self.assert_size(classes_number)
            self.test_storage.remove_class(removed_class)
            classes_number -= 1

        self.assert_size(0)

    def test_remove_class_add_class_and_remove_class(self):
        self.assert_size(0)
        self.test_storage.add_sample(SimpleSample(1), 1, 1, 1)
        self.assert_size(1)
        self.test_storage.remove_class(1)
        self.assert_size(0)
        self.test_storage.add_sample(SimpleSample(1), 1, 1, 1)
        self.assert_size(1)
        assert 1 in self.test_storage.get_classes()

    @raises(KeyError)
    def test_remove_sample_from_class_empty_storage_fails(self):
        self.test_storage.remove_sample_from_class(1, 1)

    @raises(KeyError)
    def test_remove_sample_from_class_storage_without_sample_fails(self):
        self.test_storage.add_sample(2, 1, 1)
        self.test_storage.remove_sample_from_class(3, 1)

    @raises(KeyError)
    def test_remove_sample_from_class_other_class_fails(self):
        self.test_storage.add_sample(1, 1, 1)
        self.test_storage.remove_sample_from_class(1, 2)

    def test_remove_sample_from_class_last_sample_removes_class(self):
        self.test_storage.add_sample(1, 1, 1)
        self.assert_size(1)
        assert_equals(1, self.test_storage.get_class_samples_size(1))

        self.test_storage.remove_sample_from_class(1, 1)
        self.assert_size(0)
