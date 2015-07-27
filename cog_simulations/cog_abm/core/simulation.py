"""
Module providing flow control in simulation
"""
import random
import logging
from time import time
import copy
import cPickle
from ..extras.tools import get_progressbar
from ..extras.words_storage import store_words

log = logging.getLogger('COG-ABM')

PICKLE_PROTOCOL = cPickle.HIGHEST_PROTOCOL


class Simulation(object):
    """
    This class defines what happens and when.
    """

    def __init__(self, graphs=None, interactions=None, environments=None, agents=None, pb=False,
                 colour_order=None, dump_often=None):
        """
        @type graphs: List of Maps
        @param graphs: List of Maps with two keys:
            'graph' - Network
            'start' - number of iteration when this Network begin to be used

        @type interactions: List of Maps
        @param interactions: List of Maps with two keys:
            'interaction' - Interaction
            'start' - number of iteration when this Interaction begin to be used

        @type environments: List of Maps
        @param environments: List of Maps with two keys:
            'environment' - Environment
            'start' - number of iteration when this Environment begin to be used

        @type agents: List of Agents
        @param agents: Agents used in simulation.

        @type pb: Bool
        @param pb: Show progress bar.

        @type environments: List of Colours
        @param colour_order: List of Colours in the order used when storing Agents words.
        """
        self.iteration_counter = 1
        self.environments = environments
        self.graph = None
        self.graphs = graphs
        self.interaction = None
        self.interactions = interactions
        self.agents = tuple(agents)
        self.statistic = []
        self.dump_often = dump_often
        self.pb = True
        self.colour_order = colour_order

    def dump_results(self, iter_num):
        cc = copy.deepcopy(self.agents)
        kr = (iter_num, cc)
        self.statistic.append(kr)
        if self.dump_often:
            f = open(self.dump_often + str(iter_num) + ".pout", "wb")
            cPickle.dump(kr, f, PICKLE_PROTOCOL)
            f.close()
            if self.colour_order:
                store_words(self.agents, self.colour_order, str(iter_num)+"words.pout")

    def get_iteration_counter(self):
        return self.iteration_counter

    def set_networks(self, networks):
        self.graphs = networks

    def set_environments(self, environments):
        self.environments = environments

    def set_colour_order(self, colour_order):
        self.colour_order = colour_order

    def get_agents(self):
        return self.agents

    def _change_graph(self):
        for graph in self.graphs:
            if graph["start"] == self.iteration_counter:
                self.graph = graph["graph"]
                for agent in self.agents:
                    self.graph.add_agent(agent)
                break

    def _change_interaction(self):
        for interaction in self.interactions:
            if interaction["start"] == self.iteration_counter:
                self.interaction = interaction["interaction"]
                break

    def _change_environment(self):
        for env in self.environments:
            if env["start"] == self.iteration_counter:
                self.interaction.change_environment(env["environment"])

    def _choose_agents(self):
        if self.interaction.num_agents() == 2:
            a = random.choice(self.agents)
            b = self.graph.get_random_neighbour(a)
            return [a, b]
        else:
            return [random.choice(self.agents)]

    def _start_interaction(self, agents):
        self.interaction.interact(*agents)

    def _do_iterations(self, num_iter):
        for _ in xrange(num_iter):
            self._change_graph()
            self._change_interaction()
            self._change_environment()
            agents = self._choose_agents()
            if abs(agents[0].get_id() - agents[1].get_id()) > 1:
                logging.debug(self.iteration_counter)
            self._start_interaction(agents)
            self.iteration_counter += 1

    def _do_main_loop(self, iterations, dump_freq):
        start_time = time()
        log.info("Simulation start...")
        it = xrange(iterations // dump_freq)
        if self.pb:
            it = get_progressbar()(it)
        for i in it:
            self._do_iterations(dump_freq)
            self.dump_results((i + 1) * dump_freq)

        log.info("Simulation end. Total time: " + str(time() - start_time))

    def continue_(self, iterations=1000, dump_freq=10):
        self._do_main_loop(iterations, dump_freq)
        return self.statistic

    def run(self, iterations=1000, dump_freq=10):
        """ Begins simulation. """
        self.dump_results(0)
        self._do_main_loop(iterations, dump_freq)
        return self.statistic
