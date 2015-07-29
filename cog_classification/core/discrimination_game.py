class DiscriminationGame:

    def __init__(self, samples_number=4, good_agent_measure=0.95, number_of_agents=1):

        assert samples_number > 1
        self.samples_number = samples_number

        assert good_agent_measure >= 0
        assert good_agent_measure <= 1
        self.good_agent_measure = good_agent_measure

        assert number_of_agents > 0
        self.number_of_agents = number_of_agents

    def interact(self, agents, environment):
        for i in range(self.number_of_agents):
            agent = agents.get_agent()
            result, topic_index, topic_category = self.play(agent, environment)
            agent.update_fitness("DG", result)
            self.learning_after_game(agent, topic_index, environment, topic_category, result)

    def learning_after_game(self, agent, topic_index, environment, topic_category, result):

        if result:
            agent.good_category_for_sample(topic_category, topic_index, environment)
        elif agent.get_measure("DG") >= self.good_agent_measure:
            agent.add_sample(topic_index, environment, topic_category)
        else:
            agent.add_sample(topic_index, environment)

        agent.forget()

    def play(self, agent, environment):
        topic_index = environment.get_random_sample_index()
        topic_class = environment.get_class(topic_index)
        other_samples = [self.sample_from_other_class(topic_class, environment) for _ in range(self.samples_number - 1)]

        topic = environment.get_sample(topic_index)
        topic_category = agent.classify(topic)
        other_categories = [agent.classify(sample) for sample in other_samples]

        if topic_category is None:
            result = False
        else:
            result = topic_category in other_categories

        return result, topic_index, topic_category

    @staticmethod
    def sample_from_other_class(sample_class, environment):
        while True:
            sample_index = environment.get_random_sample_index()
            if not environment.get_class(sample_index) == sample_class:
                return environment.get_sample(sample_index)
