class SampleStorage:
    """
        Sample storage provides a way to store samples and gives you a easy way to export this samples to format
    designed for machine learning algorithms.

    Every sample is associated with true class of sample,
    class of sample storage (one sample can be associated with more than one class),
    weight of association to this class, which can affect removing of sample if weight is lower than fixed
    forgetting threshold.

    Each sample of the same class from sample storage has the same true class. Every try to add sample with different
    true class will result in creating new class add adding this sample to it.

    Weights can be increased and decreased but it will not remove samples from class directly. Even if weight of
    sample will drop to 0 (minimum weight), sample will be still part of class. To remove sample with weights lower
    than forgetting threshold methods remove weak samples and remove weak samples from class should be used.

    Sample storage is implementation of the class described in Konrad Kurdej's master's thesis:
    "Modelowanie procesow poznawczych: konsensusowa metoda klasyfikacji z komunikacja miedzy agentami".
    """

    def __init__(self, alpha=0.99, beta=1, sigma=1, new_weight=1, max_weight=1, forgetting_threshold=0.05):
        """
        Parameters explanation:
        alpha - how fast samples are forgotten. Values from 0 (total sclerosis) to 1 (perfect memory).
        beta - how much weights of samples will be increased. Values from 0 (no strengthening) to infinity.
        sigma - affects how factor of similarity affects strengthening of weights.
                Value form 0 (similarity doesn't affects strengthening)
                      to infinity (the less similar samples the weaker strengthen).
        max_weight - the maximum weight of sample. Value from 0 to infinity.
        new_weight - the weight of new sample added to sample storage if no other value were given.
                     Value from 0 to max weight.
        forgetting_threshold - the samples with lower weight value than forgetting threshold value are removed.
                               Value from 0 to max weight.
        """

        self.class_name = 0

        self.alpha = alpha
        assert alpha >= 0
        assert alpha <= 1

        self.beta = beta
        assert beta >= 0

        self.sigma = sigma
        assert sigma >= 0

        self.max_weight = max_weight
        assert max_weight >= 0

        self.new_weight = new_weight
        assert new_weight >= 0
        assert new_weight <= max_weight

        self.forgetting_threshold = forgetting_threshold
        assert new_weight >= 0
        assert new_weight <= max_weight

        self.classes = {}

    def add_sample(self, sample, true_class, target_class=None, sample_weight=None):
        """
        Adds the sample to given target class or created new class if no target class is given.
        Sample has sample weight if given or default new weight of sample storage.
        Sample weight should be larger than or equal 0.

        If sample would be add to class, which true class is different then for sample, there is generated new class.
        If sample would be add to class, that already contains this sample, then method do nothing.

        Sample can be added to multiple classes.
        """

        if sample_weight is None:
            sample_weight = self.new_weight
        else:
            assert sample_weight >= 0
            assert sample_weight <= self.max_weight

        if target_class in self.classes:
            if true_class == self.classes[target_class]["true_class"]:

                if not self.sample_in_class(sample, target_class):
                    # Adding new sample to class
                    self.set_weight(sample, target_class, sample_weight)
            else:
                # There is difference in true classes of sample and given target class.
                # So we are adding sample to empty class (it forces creation of new class for sample).
                self.add_sample(sample, true_class, sample_weight=sample_weight)
        else:
            # No target class in sample storage.
            # So we create new class for sample (and new name if target_class is None).
            target_class, new_class = self.create_new_class(target_class, true_class)
            new_class["samples"][sample] = sample_weight
            self.classes[target_class] = new_class

    def create_new_class(self, target_class, true_class):
        """
        Creation of new sample storage class.

        If target class is given then we assert that this class is not in classes.
        This method doesn't add this new created class to sample storage classes.

        Create new class returns correct name of target class and target class body (dictionary).
        """

        if target_class is None:
            # We create new name for target class.

            # First we finds the name that wasn't used.
            name_in_classes = True
            name = None

            while name_in_classes:
                name_in_classes = False
                name = "Class number: " + str(self.class_name)
                for class_name in self.classes:
                    if class_name == name:
                        name_in_classes = True
                        break
                self.class_name += 1

            target_class = name
            # We didn't increase self.class_name because after finding unique name
            # we increased this value on the end of while loop.

        new_class = {"true_class": true_class, "samples": {}}
        return target_class, new_class

    def decrease_weights_in_class(self, target_class):
        """
        Decrease weights of every sample in target class according to alpha value.

        The weights will never drop below 0.

        This method didn't remove any sample.
        """

        for sample, weight in self.get_class_samples(target_class):
            new_weight = weight * self.alpha
            self.set_weight(sample, target_class, new_weight)

    def decrease_weights(self):
        """
        Decrease weights of every sample according to alpha value.

        The weights will never drop below 0.

        This method didn't remove any sample.
        """
        for target_class in self.get_classes():
            self.decrease_weights_in_class(target_class)

    def empty(self):
        return len(self.classes) == 0

    def export(self):
        """
        Returns list of list of all attributes of every sample
        and second list of class in which sample is in sample storage.
        """
        data = []
        decisions = []

        for target_class in self.get_classes():
            for sample, _ in self.get_class_samples(target_class):
                data.append(sample.get_attributes())
                decisions.append(self.get_true_class(target_class))

        return data, decisions

    def increase_weights_in_class(self, sample, target_class, distance):
        """
        Increase the weights of samples in target class
        according to their distance to sample modified by sigma and beta.

        Distance is calculated by given distance function.

        Weights will never rise above max weight.
        """

        for class_sample, old_weight in self.get_class_samples(target_class):
            weight_change = self.beta * 0.1 ** (self.sigma * distance(class_sample, sample))
            new_weight = min(old_weight + weight_change, self.max_weight)
            self.set_weight(class_sample, target_class, new_weight)

    def remove_class(self, target_class):
        """ Removes class and all its samples from sample storage. """
        try:
            self.classes.pop(target_class)
        except KeyError:
            for c in self.classes:
                if target_class == c:
                    target_class = c
                    break

            self.classes.pop(target_class)

    def remove_sample_from_class(self, sample, target_class):
        """
        Removes sample from target class.

        If it was last sample then removes target class, too.
        """

        try:
            self.classes[target_class]["samples"].pop(sample)
        except KeyError:
            for s in self.classes[target_class]["samples"]:
                # We don't use sample in class method, because it didn't returns reference to analogous sample.
                if sample.equals(s):
                    sample = s
                    break

            self.classes[target_class]["samples"].pop(sample)

        if self.get_class_number(target_class) == 0:
            self.remove_class(target_class)

    def remove_weak_samples(self):
        """
        Removes samples, which weight is lower than forgetting threshold, in each class.
        """
        for target_class in self.get_classes():
            self.remove_weak_samples_from_class(target_class)

    def remove_weak_samples_from_class(self, target_class):
        """
        Removes all samples which weight is lower than forgetting threshold.

        If all samples are removed from class, the class is removed too.
        """

        to_remove = []
        all_class_samples = self.get_class_samples(target_class)
        for sample, weight in all_class_samples:
            if weight < self.forgetting_threshold:
                to_remove.append(sample)

        if len(to_remove) == len(all_class_samples):
            self.remove_class(target_class)
        else:
            for sample in to_remove:
                self.remove_sample_from_class(sample, target_class)

    def sample_in_class(self, sample, target_class):
        """ Checking if given sample is in target class. """
        sample_in_class = False

        for s in self.classes[target_class]["samples"]:
                    # We are compare true values of sample and s not references so we cannot use in.
                    if sample.equals(s):
                        sample_in_class = True
                        break

        return sample_in_class

    def get_class_number(self, target_class):

        return len(self.classes[target_class]["samples"])

    def get_class_samples(self, target_class):
        """ Returns list of pair (sample, weight) of given target class. """
        samples = self.classes[target_class]["samples"]
        return [(sample, samples[sample]) for sample in samples]

    def get_class_samples_size(self, target_class):
        """ Returns number of samples in given target class. """
        return len(self.classes[target_class]["samples"])

    def get_classes(self):
        """ Returns labels of all classes of sample storage. """
        return self.classes.keys()

    def get_classes_number(self):
        """ Returns number of all classes of sample storage. """
        return len(self.classes)

    def get_true_class(self, target_class):
        """ Returns true class of given target class. """
        return self.classes[target_class]["true_class"]

    def set_weight(self, sample, target_class, new_weight):
        """ Sets weight of given sample in given target class to new weight. """
        assert new_weight >= 0
        assert new_weight <= self.max_weight

        self.classes[target_class]["samples"][sample] = new_weight
