"""Makes tests and simple simulations easier"""
import os

from ..core.network import Network
from ..core.interaction import Interaction
from ..core.agent import Agent
from cog_simulations.cog_abm.ML.core import Classifier
from pygraph.algorithms.generators import generate
from pygraph.classes.graph import graph


def parse_to_json_graph(file_name):
    f = open(file_name, 'r')

    nodes = f.readline().split()
    edges = []
    for line in f:
        edge = line.split()
        edges.append({"to": edge[0], "from": edge[1], "wt": 1})

    f.close()
    f = open(file_name + '.json', 'w')

    import json

    json.dump({"nodes": nodes, "edges": edges}, f)
    f.close()

def generate_clique_network(n):
    network = Network(generate(n, n * (n - 1) // 2, directed=False))
    return network

def generate_line_network(n):
    g = graph()

    for i in range(0, n):
        g.add_node(i)
    for i in range(0, n-1):
        g.add_edge((i, i+1))

    network = Network(g)
    return network

def generate_ring_network(n):
    g = graph()

    for i in range(0, n):
        g.add_node(i)
    for i in range(0, n-1):
        g.add_edge((i, i+1))
    g.add_edge((0, n-1))

    network = Network(g)
    return network

def generate_hub_network(n):
    g = graph()

    for i in range(0, n):
        g.add_node(i)
    for i in range(1, n):
        g.add_edge((0, i))

    network = Network(g)
    return network

def generate_network_with_agents(n):
    agents = [Agent(aid=i) for i in xrange(n)]
    return generate_clique_network(agents), agents

def extract_classes(samples):
    return list(set((s.get_cls() for s in samples)))

class SimpleInteraction(Interaction):
    """ Very simple interaction. Just prints agents involved and takes time.
    """
    def __init__(self, num_agents=2):
        self._num_agents = num_agents

    def num_agents(self):
        return self._num_agents

    def interact(self, *agents):
        print "Interaction with: " + str(agents) + "  in: " + str(os.getpid())
        for i in xrange(10 ** 5):
            i ** 0.5
        return [i ** 0.1 for i in xrange(len(agents))]


class SimpleClassifier(Classifier):

    def classify_pval(self, sample):
        return self.classify(sample), 1.

    def class_probabilities(self, sample):
        d = {}
        for c in self.classes:
            d[c] = 0.
        d[self.classify(sample)] = 1.
        return d

    def train(self, samples):
        self.classes = extract_classes(samples)


class PerfectClassifer(SimpleClassifier):
    """ If given sample has class, it returns it
    """

    def classify(self, sample):
        return sample.get_cls()


class StupidClassifer(SimpleClassifier):
    """ Always returns the same class
    """

    def __init__(self, cls=0):
        self.cls = str(cls)

    def classify(self, sample):
        return self.cls
