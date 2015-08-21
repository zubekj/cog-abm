from cog_classification.core.result import Result


class SteelsClassifierResults(Result):
    """
    Set of agents which have taken part in steels simulation.

    They can serves as classifier.
    """

    def __init__(self):
        Result.__init__(self)

    def save(self, agents, interactions, environment, result, end_condition, iteration):
        """
        Save agents if it is the last iteration of simulation.

        :param Network agents: The source of agents.
        :param Condition end_condition: The condition that tells whether simulation ends.
        """
        if end_condition.end(agents, interactions, environment, result, end_condition, iteration):
            self.results['agents'] = agents.get_all_agents()

    def predict(self, sample):
        """
        Predicts class of sample based on voting of agents.

        :param sample: The sample which class is predicted.

        :return: Predicted class of sample.
        :rtype: hashable
        """
        classes_voting = {}

        for agent in self.results['agents']:
            class_vote = int(agent.get_category_class(agent.classify(sample)))
            if class_vote in classes_voting:
                classes_voting[class_vote] += 1
            else:
                classes_voting[class_vote] = 1

        best_class = None
        most_votes = 0

        for class_vote, number in classes_voting.iteritems():
            if number > most_votes:
                most_votes = number
                best_class = class_vote

        return best_class
