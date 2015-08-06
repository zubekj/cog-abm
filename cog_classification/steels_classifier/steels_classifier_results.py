from cog_classification.core.result import Result


class SteelsClassifierResults(Result):

    def __init__(self):
        Result.__init__(self)

    def save(self, agents, interactions, environment, result, end_condition, iteration):
        if end_condition.end(agents, interactions, environment, result, end_condition, iteration):
            self.results['agents'] = agents.get_all_agents()

    def predict(self, sample):
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

    def test_agents(self):
        for agent in self.results['agents']:
            print("Words: %s" % len(agent.get_words()))
            print("Categories: %s" % agent.get_categories_size())
