from cog_classification.core.discrimination_game import DiscriminationGame

class GuessingGame:

    def __init__(self, samples_number=4, good_agent_measure=0.95):
        self.samples_number = samples_number
        self.good_agent_measure = good_agent_measure

        self.game = DiscriminationGame(samples_number, good_agent_measure)

    def interact(self, agents, environment):
        agents = agents.get_agents(2)
        speaker = agents[0]
        hearer = agents[1]

        result, topic_index, topic_category, other_samples = self.game.play(speaker, environment)

        if result:
            speaker.update_fitness("DG", result)
            word = speaker.word_for_category(topic_category)
            guesses_category = hearer.category_for_word(word)

            if guesses_category is not None:
                guessed_topic = None
                the_best_probability = -float('inf')

                for sample in other_samples:
                    probability = hearer.probability_of_sample_in_category(sample, guesses_category)
                    if the_best_probability < probability:
                        the_best_probability = property
                        guessed_topic = sample

                if environment.get_sample(topic_index) == guessed_topic:
                    speaker.good_word_for_category(word, topic_category)
                    speaker.the_best_category_for_word(word, topic_category)
                    speaker.good_category_for_sample(topic_category, topic_index, environment)
                    speaker.update_fitness("GG", result)

                    hearer.good_word_for_category(word, guesses_category)
                    hearer.the_best_word_for_category(word, guesses_category)
                    hearer.good_category_for_sample(guesses_category, topic_index, environment)
                    hearer.update_fitness("GG", result)
            else:
                result, topic_index, topic_category, other_samples = self.game.play(speaker, environment)
                if result:
                    hearer.
        else:
            self.game.learning_after_game(speaker, topic_index, environment, topic_category, result)
            speaker.update_fitness("DG", result)



