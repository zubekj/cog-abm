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

    def __init__(self, graph=None, interaction=None, agents=None, pb=False, 
                 dump_words=True, colour_order=None):
        ''' pb - show progress bar
            dump_words - dump words in seperate files
            colour_order - list of colours in the order used when storing agents words
        '''
        self.graph = graph
        self.interaction = interaction
        self.agents = tuple(agents)
        self.statistic = []
        self.dump_often = True
        self.pb = True#pb
        self.dump_words = dump_words
        self.colour_order = colour_order

    def dump_results(self, iter_num):
        cc = copy.deepcopy(self.agents)
        #cc = [a.deepcopy() for a in self.agents]
        kr = (iter_num, cc)
        self.statistic.append(kr)
        if self.dump_often:
            f = open(str(iter_num) + ".pout", "wb")
            cPickle.dump(kr, f, PICKLE_PROTOCOL)
            f.close()
            if self.dump_words:
                store_words(self.agents, self.colour_order, str(iter_num)+"words.pout")

    def _choose_agents(self):
        if self.interaction.num_agents() == 2:
            a = random.choice(self.agents)
            b = self.graph.get_random_neighbour(a)
            return [a, b]
        else:
            return [random.choice(self.agents)]

    def _start_interaction(self, agents):
        self.interaction.interact(*agents)
#               results = self.interaction.interact(*agents)
#               for r, a in izip(results, agents):
#                       a.add_inter_result(r)

    def _do_iterations(self, num_iter):
        for _ in xrange(num_iter):
            agents = self._choose_agents()
            self._start_interaction(agents)

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
        """
        Begins simulation.

        iterations
        """
        self.dump_results(0)
        self._do_main_loop(iterations, dump_freq)
        return self.statistic
