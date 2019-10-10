from cog_classification.steels.guessing_game import GuessingGame
from cog_classification.steels.discrimination_game import DiscriminationGame
from cog_classification.steels.steels_agent import SteelsClassificationAgent
from cog_classification.steels.sample_storage import SampleStorage
from cog_classification.core.behavior_switcher import BehaviorSwitcher
from cog_classification.core import environment, fitness, network, condition,\
        simulation, result
from cog_classification.tools.topology_generator import generate_topology

from matplotlib import pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd


if __name__ == "__main__":

    agents = {}

    for _ in range(10):
        sample_storage = SampleStorage(alpha=0.1, max_weight=2,
                                       forgetting_threshold=0.0)
        the_agent = SteelsClassificationAgent(sample_storage=sample_storage)
        the_agent.set_fitness("DG", fitness.CurrentFitness(scope=50))
        the_agent.set_fitness("GG", fitness.CurrentFitness(scope=50))
        agents[the_agent.id] = the_agent

    topology = generate_topology("clique", agents_names=list(agents.keys()))

    complete_network = network.Network(agents, {1: topology})

    wcs_data = pd.read_csv("data/1269_munsell_chips.csv")
    the_environment = environment.NoClassEnvironment(wcs_data.values,
                                                     distance_threshold=50)

    sim = simulation.Simulation(complete_network,
                                BehaviorSwitcher({1: GuessingGame(good_agent_measure=0.95)}),
                                BehaviorSwitcher({1: the_environment}),
                                result.StandardResult(gap=50),
                                condition.IterationCondition(10000))
    results = sim.run().get_results()

    iters = []
    dg = []
    gg = []
    for k in sorted(results.keys()):
        iters.append(results[k]["iteration"])
        dg.append(np.mean(results[k]["DG"]))
        gg.append(np.mean(results[k]["GG"]))

    fig, axes = plt.subplots(2)
    axes[0].plot(iters, dg)
    axes[1].plot(iters, gg)
    plt.show()
