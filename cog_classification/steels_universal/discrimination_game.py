class DiscriminationGame:
    """
    This class implements discrimination game.

    Discrimination game was described in Luc Steels and Tony Belpaeme
    "Coordinating perceptually grounded categories through language: A case study for colour".
    """

    def __init__(self, samples_number=4, good_agent_measure=0.95):
        """
        Parameters explanation:
        samples number - the number of samples shown to agent in one interaction including topic.
            Value from 2 to infinity.
        good_agent_measure - the threshold which affects generation of new categories. Value from 0 to 1.
        """
        assert samples_number > 1
        self.samples_number = samples_number

        assert good_agent_measure >= 0
        assert good_agent_measure <= 1
        self.good_agent_measure = good_agent_measure

    def interact(self, agents, environment):
        """
        One turn of interaction in discrimination game.
        """
        agent = agents.get_agent()
        result, topic_index, topic_category, _ = self.play(agent, environment)
        self.learning_after_game(agent, topic_index, environment, topic_category, result)
        agent.update_fitness("DG", result)

    def learning_after_game(self, agent, topic_index, environment, topic_category, result):
        """
        Changes inner agent state depending on result
        and agent "DG" - discrimination game, success.
        """

        if result:
            agent.strengthen_memory_sample_category(topic_category, topic_index, environment)
        elif agent.get_fitness_measure("DG") >= self.good_agent_measure:
            agent.add_sample(topic_index, environment, topic_category)
        else:
            agent.add_sample(topic_index, environment)

        agent.forget()

    def play(self, agent, environment):
        """
        The core implementation of single game.

        SteelsAgent gets sets of samples in which one is chosen as topic.

        SteelsAgent task is to classify this topic as different from other samples.
        """
        topic_index = environment.get_random_sample_index()
        topic_class = environment.get_class(topic_index)
        other_samples = [self.sample_from_other_class(topic_class, environment) for _ in range(self.samples_number - 1)]

        topic = environment.get_sample(topic_index)
        return self.play_with_given_samples(agent, topic, topic_index, other_samples)

    @staticmethod
    def play_with_given_samples(agent, topic, other_samples):
        topic_category = agent.classify(topic)
        other_categories = [agent.classify(sample) for sample in other_samples]

        if topic_category is None:
            result = False
        else:
            result = topic_category in other_categories

        return result, topic_category

    @staticmethod
    def sample_from_other_class(sample_class, environment):
        """
        Finds in environment sample that has different class than sample class.
        """
        while True:
            index, sample, taken_class = environment.get_random_sample()
            if not taken_class == sample_class:
                return sample
