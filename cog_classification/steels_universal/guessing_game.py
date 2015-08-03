import random

from cog_classification.steels_universal.discrimination_game import DiscriminationGame


class GuessingGame:

    def __init__(self, samples_number=4, good_agent_measure=0.95):
        self.samples_number = samples_number
        self.good_agent_measure = good_agent_measure

        self.game = DiscriminationGame(samples_number, good_agent_measure)

    def interact(self, agents, environment):
        agents = agents.get_agents(2)
        speaker = agents[0]
        hearer = agents[1]

        topic_index, topic, topic_class = environment.get_random_sample()

        other_samples = [DiscriminationGame.sample_from_other_class(topic_class, environment)
                         for _ in range(self.samples_number - 1)]

        # Speaker is trying to discriminate topic from other samples.
        result, speaker_category = self.game.play_with_given_samples(speaker, topic, other_samples)

        # If speaker can discriminate topic from other_samples.
        if result:
            # Speaker is looking for word that suits topic category.
            word = speaker.find_word_for_category(speaker_category)

            # Hearer is looking for category that suits speaker word.
            hearer_category = hearer.find_category_for_word(word)

            # If hearer finds such category.
            if hearer_category is not None:

                guessed_topic = hearer.choose_the_best_sample_for_category(hearer_category,
                                                                           random.shuffle(other_samples + [topic]))

                # If hearer correctly assumed that topic belongs to guesses category the most.
                if topic == guessed_topic:
                    result = "Success"

                # If hearer didn't assume that topic belongs to guesses category the most.
                else:
                    result = "Not matching samples."

            # If hearer doesn't find such category for word.
            else:
                result = "Hearer didn't know word."

        # If speaker cannot discriminate topic from other_samples.
        else:
            result = "Speaker failed discrimination."

        # Actions taken up depending on game results.
        if result == "Success":

            # Strengthen association between word and category.
            speaker.strengthen_association_word_category(word, speaker_category)
            # Strengthen association between word and category.
            hearer.strengthen_association_word_category(word, hearer_category)

            # Weaken associations between other categories and word.
            speaker.weaken_association_word_other_categories(word, speaker_category)
            # Weaken associations between other words and category.
            hearer.weaken_association_other_word_categories(word, hearer_category)

            # Strengthen memory of category.
            speaker.strengthen_memory_sample_category(speaker_category, topic_index, environment)
            # Strengthen memory of category.
            hearer.strengthen_memory_sample_category(hearer_category, topic_index, environment)

            speaker.update_fitness("GG", True)
            speaker.update_fitness("DG", True)
            hearer.update_fitness("GG", True)

        elif result == "Speaker failed discrimination.":
            self.game.learning_after_game(speaker, topic_index, environment, speaker_category, False)

            speaker.update_fitness("DG", False)

        elif result == "Hearer didn't know word.":
            result, hearer_category = self.game.play_with_given_samples(hearer, environment.get_sample(topic_index),
                                                                        other_samples)

            if not result:
                    self.game.learning_after_game(hearer, topic_index, environment, hearer_category, result)

            # Associating the category for topic with word.
            hearer.strengthen_association_word_category(word, hearer_category)

            speaker.update_fitness("GG", False)
            speaker.update_fitness("DG", True)
            hearer.update_fitness("GG", False)

        elif result == "Not matching samples.":

            speaker.weaken_association_word_category(word, speaker_category)
            hearer.weaken_association_word_category(word, hearer_category)

            self.game.learning_after_game(hearer, topic_index, environment, hearer_category, result=False)

            speaker.update_fitness("GG", False)
            speaker.update_fitness("DG", True)
            hearer.update_fitness("GG", False)
        else:
            raise ValueError
