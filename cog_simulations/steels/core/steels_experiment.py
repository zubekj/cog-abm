"""
This module implements Steels experiment.
"""
import logging

from cog_simulations.cog_abm.core import Simulation
from reactive_unit import ReactiveUnit
from adaptative_network import AdaptiveNetwork
from steels_classifier import SteelsClassifier


log = logging.getLogger('steels')
log.level = logging.INFO


# Steels experiment main part
def steels_experiment(num_iter=1000, dump_freq=50, alpha=0.1, beta=1, sigma=10, agents=None,
                      environments=None,  networks=None, interactions=None, dump_often=None,
                      num_agents=None):
    # Don't remove num_agents it is required in experiment continuation,
    """
    An experiment in which topology, type and learning can change after some number of iterations.
    """

    games_labels = load_games_labels(interactions)
    agents = load_agents(agents, games_labels)
    interactions = load_interactions(interactions)
    colour_order, environments = load_environment(environments)

    AdaptiveNetwork.def_alpha = float(alpha)
    AdaptiveNetwork.def_beta = float(beta)
    ReactiveUnit.def_sigma = float(sigma)

    log.info("Running steels experiment with: %s",
             str({'num agents': len(agents)}))

    s = Simulation(graphs=networks, interactions=interactions, agents=agents,
                   environments=environments, colour_order=colour_order, dump_often=dump_often)
    res = s.run(num_iter, dump_freq)

    return res, s


def load_games_labels(interactions):
    labels = ["DG"]

    for interaction in interactions:
        if "game_name" in interaction:
            labels.append(interaction["game_name"])
            if interaction["type"] == "GuessingGame":
                labels.append("DG_%s" % interaction["game_name"])
        else:
            if interaction["type"] == "GuessingGame":
                labels.append("GG")

    return list(set(labels))



def load_agents(agents, games_labels):
    from cog_simulations.cog_abm.core.agent import Agent
    from cog_simulations.steels.core.steels_agent_state_with_lexicon import SteelsAgentStateWithLexicon
    from cog_simulations.cog_abm.agent.sensor import SimpleSensor
    from cog_simulations.steels import metrics
    from cog_simulations.cog_abm.extras.tools import def_value

    classifier, classifier_arg = SteelsClassifier, []
    classifier_arg = def_value(classifier_arg, [])

    true_agents = []
    for _ in agents:
        state = SteelsAgentStateWithLexicon(classifier(*classifier_arg))
        true_agent = Agent(state=state, sensor=SimpleSensor())
        true_agent.set_fitness_measure("DG", metrics.get_ds_fitness())
        for label in games_labels:
            metric = metrics.get_cs_fitness()
            true_agent.set_fitness_measure(label, metric)
        true_agents.append(true_agent)

    return true_agents


def load_interactions(interactions):
    from discrimination_game import DiscriminationGame
    from guessing_game import GuessingGame

    interaction_list = []

    for interaction in interactions:

        context_size = interaction["context_size"]
        learning = interaction["learning"]
        start = interaction["start"]
        inc_category_threshold = interaction["inc_category_threshold"]

        game_name = None
        if "game_name" in interaction:
            game_name = interaction["game_name"]

        role_model = "RANDOM"
        if "role_model" in interaction:
            role_model = interaction["role_model"]

        if interaction["type"] == "GuessingGame":
            inter = GuessingGame(learning_mode=learning, game_name=game_name, role_model=role_model)
        else:
            inter = DiscriminationGame(context_size, float(inc_category_threshold), game_name=game_name)
        interaction_list.append({"start": start, "interaction": inter})

    return interaction_list


def load_environment(environments):
    from cog_simulations.cog_abm.extras.color import Color
    from cog_simulations.cog_abm.extras.extract_colour_order import extract_colour_order
    from cog_simulations.cog_abm.core.environment import Environment, RandomStimuliChooser

    colour_order = None

    real_environments = []
    for environment in environments:
        start = environment["start"]

        list_of_stimuli = []

        for stimulus in environment["source"]["stimuli"]:
            l = stimulus["L"]
            a = stimulus["a"]
            b = stimulus["b"]
            list_of_stimuli.append(Color(l, a, b))

        if "distance" in environment:
            dist = environment["distance"]
            chooser = RandomStimuliChooser(use_distance=True, distance=dist)
        else:
            chooser = RandomStimuliChooser()

        if "word_naming_per_color" in environment:
            word_naming_per_color = environment["word_naming_per_color"]
            colour_order = extract_colour_order(list_of_stimuli, word_naming_per_color)

        env = Environment(list_of_stimuli, chooser, colour_order)
        real_environments.append({"start": start, "environment": env})

    return colour_order, real_environments
