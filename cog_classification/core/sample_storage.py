class SampleStorage:
    """
    Sample storage is a class whose mission is to store and manage samples with corresponding classes.

    Sample storage implements both adding and forgetting samples and can export all samples with classes to
    format suitable in machine learning.

    Every sample has a class and weight which affects forgetting.
    """

    def __init__(self, alpha=0.99, beta=1, sigma=1, new_weight=1, max_weight=1, forgetting_threshold=0.05):
        """
        Parameters explanation:
        alpha - how fast samples are forgotten. Values from 0 (total sclerosis) to 1 (perfect memory).
        beta - how much weights of samples will be strengthen. Values from 0 (no strengthening) to infinity.
        sigma - affects how factor of similarity affects strengthening of weights.
                Value form 0 (similarity doesn't affects strengthening)
                      to infinity (the less similar samples the weaker strengthen).
        new_weight - the weight of new sample added to sample storage if no other value were given.
        max_weight - the maximum weight of sample.
        forgetting_threshold - the samples with lower weight value than forgetting threshold value are removed
        """

        self.class_name = 0

        self.alpha = alpha
        self.beta = beta
        self.sigma = sigma

        self.new_weight = new_weight
        self.max_weight = max_weight
        self.forgetting_threshold = forgetting_threshold

        self.classes = {}

    def add_sample(self, sample, true_class, sample_class=None, sample_weight=None):
        """
        Adds the sample to given sample class or created new class if no sample class is given.
        Sample has sample weight if given or default new weight of sample storage.
        If sample would be add to class which true class is different then for sample is generated new class.
        Sample can be added to multiple classes.
        """

        sample_weight = sample_weight or self.new_weight

        if sample_class in self.classes:
            if true_class == self.classes[sample_class]["true_class"]:
                if sample not in self.classes[sample_class]["samples"]:
                    self.classes[sample_class]["samples"][sample] = sample_weight
                else:
                    # If sample has already existed in sample class, then we strengthen this class with sample.
                    self.increase_weights_in_class(sample, sample_class)
            else:
                # There is difference in true classes of sample and given sample class.
                # So we are adding sample to empty class (it forces creation of new class for sample).
                self.add_sample(sample, true_class, sample_weight=sample_weight)
        else:
            # No sample class in sample storage.
            # So we create new class for sample (and new name if sample_class is None).
            sample_class, new_class = self.create_new_class(sample_class, true_class)
            new_class["samples"][sample] = sample_weight
            self.classes[sample_class] = new_class

    def create_new_class(self, sample_class, true_class):
        """
        Creation of new class in sample storage.
        If sample class is given then we assert that this class is not in classes.
        Create new class returns correct name of sample class and sample class body (dictionary).
        """

        if sample_class is None:
            # We create new name for sample class.

            # First we finds the name that wasn't used.
            while self.class_name in self.classes:
                self.class_name += 1

            sample_class = self.class_name
            self.class_name += 1

        new_class = {"true_class": true_class, "samples": {}}
        return sample_class, new_class

    def increase_weights_in_class(self, sample, sample_class):
        """ Increase the weights of samples in sample class according to their distance to sample. """

        for class_sample, old_weight in self.get_class_samples(sample_class):
            weight_change = self.beta * 0.1 ** (self.sigma * sample.distance(class_sample))
            new_weight = min(old_weight + weight_change, self.max_weight)
            self.set_weight(class_sample, sample_class, new_weight)

    def decrease_weights_in_class(self, target_class):
        """ Decrease weights of every sample in target class according to alpha value. """

        for sample, weight in self.get_class_samples(target_class):
            new_weight = weight * self.alpha
            self.set_weight(sample, target_class, new_weight)

    def decrease_weights(self):
        """ Decrease weights of every sample according to alpha value. """
        for target_class in self.get_classes():
            self.decrease_weights_in_class(target_class)

    def get_class_samples(self, sample_class):
        """ Returns list of pair (sample, weight). """
        samples = self.classes[sample_class]["samples"]
        return [(sample, samples[sample]) for sample in samples]

    def get_classes(self):
        return self.classes.keys()

    def set_weight(self, sample, sample_class, new_weight):
        """ Sets weight of given sample in given sample class to new weight. """
        self.classes[sample_class]["samples"][sample] = new_weight
