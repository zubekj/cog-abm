"""
This module implements Steels experiment.
"""
import logging
import random

import numpy as np

from cog_simulations.cog_abm.ML.core import Classifier
from cog_simulations.cog_abm.core.interaction import Interaction
from cog_simulations.cog_abm.extras.tools import def_value
from cog_simulations.cog_abm.core.agent import Agent
from cog_simulations.cog_abm.extras.lexicon import Lexicon
from cog_simulations.cog_abm.agent.sensor import SimpleSensor
from cog_simulations.cog_abm.extras.additional_tools import generate_clique_network
from cog_simulations.cog_abm.core import Simulation

import metrics
from metrics import DS_A

log = logging.getLogger('steels')
log.level = logging.INFO


class ReactiveUnit(object):
    """ Reactive units are used in adaptive networks. """

    def_sigma = 1.

    def __init__(self, central_value, sigma=None):
        self.central_value = central_value
        sigma = sigma or ReactiveUnit.def_sigma
        self.sqr_sig = np.longdouble(-0.5 / (sigma ** 2.))

    def value_for(self, x):
        """ Calculate reaction for given vector """
        a = self.central_value.distance(x) ** 2.
        w = np.exp(a * self.sqr_sig)
        return w

    def __eq__(self,  other):
        if isinstance(other,  ReactiveUnit):
            return other.central_value == self.central_value
        else:
            return False


class AdaptiveNetwork(object):
    """ Adaptive network is some kind of classifier. """

    def_alpha = 0.1
    def_beta = 1.

    def __init__(self,  reactive_units=None, alpha=None, beta=None):
        """ Must be with weights ! """
        self.units = reactive_units or []
        self.alpha = np.longdouble(alpha or AdaptiveNetwork.def_alpha)
        self.beta = np.longdouble(beta or AdaptiveNetwork.def_beta)

    def _index_of(self, unit):
        """
        Finds index of given unit.
        Returns -1 if there is no such unit in this network.
        """
        for i, (u, _) in enumerate(self.units):
            if u == unit:
                return i
        return -1

    def add_reactive_unit(self, unit, weight=1.):
        index = self._index_of(unit)
        weight = np.longdouble(weight)
        if index == -1:
            self.units.append((unit, weight))
        else:
            self.units[index] = (unit, weight)

    def reaction(self, data):
        return sum((w * u.value_for(data) for u, w in self.units))

    def _update_units(self, update):
        tmp = [update(u, w) for u, w in self.units]
        self.units = filter(lambda x: x is not None,  tmp)

    def remove_low_units(self, threshold=0.1 ** 30):
        self.units = [(u, w) for u, w in self.units if w >= threshold]

    def increase_sample(self, sample):
        update = lambda u, w: (u,
                               # We don't want weight to exceed 1.
                               min(np.longdouble(1.), w + self.beta * u.value_for(sample)))
        self._update_units(update)

    def forgetting(self):
        self._update_units(lambda u, w: (u, self.alpha * w))


class SteelsClassifier(Classifier):

    def __init__(self):
        self.categories = {}
        self.new_category_id = 0

    def add_category(self, sample=None, class_id=None):
        if class_id is None:
            class_id = self.new_category_id
            self.new_category_id += 1
            adaptive_network = AdaptiveNetwork()
        else:
            adaptive_network = self.categories[class_id]

        if sample is not None:
            adaptive_network.add_reactive_unit(
                ReactiveUnit(sample)
            )

        self.categories[class_id] = adaptive_network
        return class_id

    def del_category(self, category_id):
        del self.categories[category_id]

    def classify(self, sample):
        if len(self.categories) == 0:
            return None
        return max(
            self.categories.iteritems(),
            key=lambda kr: kr[1].reaction(sample)
        )[0]

    def increase_samples_category(self, sample):
        category_id = self.classify(sample)
        self.categories[category_id].increase_sample(sample)

    def forgetting(self):
        for an in self.categories.itervalues():
            an.forgetting()

    def sample_strength(self, category_id, sample):
        return self.categories[category_id].reaction(sample)


class DiscriminationGame(Interaction):

    def __init__(self, context_len=4, inc_category_threshold=0.95, environment=None):
        self.context_len = context_len
        self.inc_category_threshold = inc_category_threshold
        self.environment = environment

    def change_environment(self, environment):
        self.environment = environment

    @staticmethod
    def num_agents():
        return 2

    def set_inc_category_threshold(self, new_inc_category_threshold):
        self.inc_category_threshold = new_inc_category_threshold

    @staticmethod
    def save_result(agent, result):
        agent.add_payoff("DG", int(result))

    @staticmethod
    def disc_game(agent, context, topic):
        """
        Checking whether agent can discriminate topic from context.
        Topic is element of context.
        """
        c_topic = agent.sense_and_classify(topic)
        # No problem if c_topic is None => count>1 so it will add new category.

        c_context = [agent.sense_and_classify(c) for c in context]
        count = c_context.count(c_topic)
        return count == 1, c_topic

    def learning_after(self, agent, topic, success, c_topic=None):
        success_rate = DS_A(agent)
        sensed_topic = agent.sense(topic)

        if success:
            agent.state.classifier.increase_samples_category(sensed_topic)
        elif success_rate >= self.inc_category_threshold:
            if c_topic is None:
                c_topic = agent.state.classifier.classify(sensed_topic)
            agent.state.classifier.add_category(sensed_topic, c_topic)
        else:
            agent.state.classifier.add_category(sensed_topic)

        # Lower strength of memory.
        agent.state.classifier.forgetting()

    def play_with_learning(self, agent, context, topic):
        success, c_topic = self.disc_game(agent, context, topic)
        self.learning_after(agent, topic, success, c_topic)
        return success, c_topic, topic, context

    def play_save(self, agent, context, topic):
        success, c_topic = self.disc_game(agent, context, topic)
        self.save_result(agent, success)
        return success, c_topic

    def play_learn_save(self, agent, context, topic):
        success, c_topic, topic, context = self.play_with_learning(agent, context, topic)
        self.save_result(agent, success)
        return success, c_topic, topic, context

    def get_setup(self):
        context = self.environment.get_stimuli(self.context_len)
        topic = context[0]
        # ^^^^ They are already shuffled - and needed when different classes.
        return context, topic

    def interact_one_agent(self, agent, context=None, topic=None):
        if context is None or topic is None:
            context, topic = self.get_setup()
        success, _, _, _ = self.play_with_learning(agent, context, topic)
        self.save_result(agent, success)
        return success

    def interact(self, agent1, agent2):
        context, topic = self.get_setup()
        return (
            ("DG", self.interact_one_agent(agent1, context, topic)),
            ("DG", self.interact_one_agent(agent2, context, topic))
        )

    def __repr__(self):
        return "DiscriminationGame: context_len=%s;" \
               " inc_category_threshold=%s" % \
               (self.context_len, self.inc_category_threshold)


class GuessingGame(Interaction):
    """
    Based mostly on work "Colourful language and colour categories"
    of Tony Belpaeme and Joris Bleys.
    """

    def __init__(self, disc_game=None, context_size=None, learning_mode=True, environment=None):
        if disc_game is None:
            disc_game = DiscriminationGame(environment=environment)
            if context_size is not None:
                disc_game.context_len = context_size

        self.disc_game = disc_game
        self.learning_mode = learning_mode
        self.environment = environment

    def change_environment(self, environment):
        self.environment = environment
        self.disc_game.change_environment(environment)

    @staticmethod
    def num_agents():
        return 2

    def set_inc_category_threshold(self, new_inc_category_threshold):
        self.disc_game.set_inc_category_threshold(new_inc_category_threshold)

    @staticmethod
    def save_result(agent, result):
        agent.add_payoff("GG", int(result))

    def guess_game(self, speaker, hearer):
        """
        The most important method: the guessing game logic.

        Each line explained by a comment.
        """

        # Get a random list of stimuli from environment of size self.disc_game.context_len:
        context = self.environment.get_stimuli(self.disc_game.context_len)

        # The first element of this context is topic:
        topic = context[0]

        """
        The speaker plays the discrimination game on the selected context and topic.
        The game returns: success (boolean whether the game ended in success)
        and s_category (the speaker's category to which topic belongs)
        """
        success, s_category = self.disc_game.play_save(speaker, context, topic)

        # If the speaker did not discriminate the topic from the rest of the context himself:
        if not success:
            # If agents can learn:
            if self.learning_mode:
                # Learn by himself this discrimination:
                self.disc_game.learning_after(speaker, topic, False, s_category)
            # Do not proceed further:
            return False

        # word = word that speaker uses to call the s_category category.
        word = speaker.state.word_for(s_category)
        # If there is no word that speaker has for this category:
        if word is None:
            # A random word is chosen for this category and added:
            word = speaker.state.lexicon.add_element(s_category)

        # h_word_category = a category that hearer thinks of when using the word:
        h_word_category = hearer.state.category_for(word)
        # If there is no category for word in hearer's memory:
        if h_word_category is None:
            """
            The hearer learns a new word:
            If he discriminates topic from context, a new word is added.
            If he does not, he first learns to discriminate and only then learns a new word.
            """

            # If agents can learn:
            if self.learning_mode:
                """
                Agent hearer plays discrimination game on context and topic.
                The game returns: success (boolean whether the game ended in success)
                and h_category (the category to which topic belongs).
                """
                success, h_category = self.disc_game.play_save(hearer, context, topic)

                # If hearer successfully played discrimination game:
                if success:
                    # Add word to category h_category.
                    hearer.state.lexicon.add_element(h_category, word)
                # If hearer does not discriminate the topic from context:
                else:
                    # Hearer learns to discriminate:
                    self.disc_game.learning_after(hearer, topic, success, h_category)
                    # Get the category of hr to which topic belongs to after learning:
                    class_id = hearer.sense_and_classify(topic)
                    # Add word to category h_category in agent hr.
                    hearer.state.lexicon.add_element(class_id, word)
            return False

        # Randomly shuffle the context:
        random.shuffle(context)
        # Choose a stimulus from context, which is most characteristic to the h_word_category
        max_hr_sample = self.find_best_matching_sample_to_category(hearer, context, h_word_category)

        # Checking game result: is the strongest activated stimulus same as topic?
        success = max_hr_sample == topic

        # If it is the same:
        if success:
            """
            Increase the confidence in word for topic in both speaker and hearer:
            This is a symmetric function from the perspective of speaker and hearer:
            """

            # If agents can learn:
            if self.learning_mode:
                speaker.state.lexicon.inc_dec_categories(s_category, word)
                # ^^ as in 4.2 1.(a)
                hearer.state.lexicon.inc_dec_words(h_word_category, word)
                # ^^ as in 4.2 2.(a)

                for a in [speaker, hearer]:
                    a.state.classifier.increase_samples_category(a.sense(topic))

        # If it is different:
        else:
            """
            Decrease the confidence in word for topic in both speaker and hearer:
            Further, learning on hearer performed but without use of word.
            """

            # If agents can learn:
            if not self.learning_mode:
                speaker.state.lexicon.decrease(s_category, word)
                # ^^ as in 4.2 1.(b)
                hearer.state.lexicon.decrease(h_word_category, word)
                # ^^ as in 4.2 2.(b)

                self.disc_game.learning_after(hearer, topic, False)

        return success

    @staticmethod
    def find_best_matching_sample_to_category(agent, samples, category):
        max_reaction, max_sample = float("-inf"), None
        for sample in samples:
            strength = agent.state.sample_strength(category, agent.sense(sample))
            if strength > max_reaction:
                max_reaction, max_sample = strength, sample
        return max_sample

    def interact(self, speaker, hearer):
        r = self.guess_game(speaker, hearer)
        self.save_result(speaker, r)
        self.save_result(hearer, r)
        return ("GG", r), ("GG", r)

    def __repr__(self):
        return "GuessingGame: %s" % self.disc_game


# class SteelsAgentState(AgentState):
class SteelsAgentState(object):

    def __init__(self, classifier):
        self.classifier = classifier

    def classify(self, sample):
        return self.classifier.classify(sample)

    def classify_p_val(self, sample):
        return self.classifier.classify_p_val(sample)

    def class_probabilities(self, sample):
        return self.classifier.class_probabilities(sample)

    def sample_strength(self, category, sample):
        return self.classifier.sample_strength(category, sample)


class SteelsAgentStateWithLexicon(SteelsAgentState):

    def __init__(self, classifier, initial_lexicon=None):
        super(SteelsAgentStateWithLexicon, self).__init__(classifier)
        self.lexicon = initial_lexicon or Lexicon()

    def category_for(self, word):
        return self.lexicon.category_for(word)

    def word_for(self, category):
        return self.lexicon.word_for(category)


# Steels experiment main part
def steels_advanced_experiment(num_iter=1000, dump_freq=50, learning=None, agents=None, num_agents=10,
                               stimuli=None, environments=None, environment=None, networks=None, interactions=None):
    """
    An experiment in which topology, type and learning can change after some number of iterations.
    """

    classifier, classifier_arg = SteelsClassifier, []
    classifier_arg = def_value(classifier_arg, [])

    has_gg = False
    for i in interactions:
        if i["interaction"]["interaction_type"] is "GG":
            has_gg = True
            break

    if agents is None:
        agents = []
        for _ in range(0, num_agents):
            agents.append(Agent())

    for agent in agents:
        state = SteelsAgentStateWithLexicon(classifier(*classifier_arg))
        agent.set_state(state)
        agent.set_sensor(SimpleSensor())
        agent.set_fitness_measure("DG", metrics.get_DS_fitness())
        if has_gg:
            agent.set_fitness_measure("GG", metrics.get_CS_fitness())

    AdaptiveNetwork.def_alpha = float(learning["alpha"])
    AdaptiveNetwork.def_beta = float(learning["beta"])
    ReactiveUnit.def_sigma = float(learning["sigma"])

    if networks is None:
        network = generate_clique_network(len(agents))
        for i, a in enumerate(agents):
            network.add_agent(a, i)
        networks = [{"graph": network, "start": 1}]

    interaction_list = []

    for interaction in interactions:
        i = interaction["interaction"]
        dg = DiscriminationGame(i["context_size"], float(i["inc_category_threshold"]))
        if i["interaction_type"] is "GG":
            inter = GuessingGame(dg)
        else:
            inter = dg
        interaction_list.append({"start": interaction["start"], "interaction": inter})

    log.info("Running steels experiment with: %s",
             str({'stimuli num': len(stimuli),
                  'num agents': len(agents)}))

    if environment is None:
        colour_order = None
    else:
        colour_order = environment.colour_order

    s = Simulation(networks, interaction_list, agents=agents,
                   environments=environments, colour_order=colour_order)
    res = s.run(num_iter, dump_freq)

    return res
