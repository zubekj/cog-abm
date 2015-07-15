"""
Module provides parser for json documents.
"""
import json
from pygraph.readwrite import markup
from cog_simulations.cog_abm.core.network import Network
from cog_simulations.cog_abm.generators.graph_generator import graph_generator


class Parser(object):
    """
    Parser class.

    Parser provides methods used to handle simulation input when given in json.

    @sort: __init__
    """

    def __init__(self):
        """ Initialize parser. """

    def parse_simulation(self, source):
        """
        Parse simulation parameters given in json document.

        @type source: String
        @param source: Simulation JSON document directory.

        @rtype: Dictionary
        @return: Simulation parameters created from json document.
        """

        if source is None:
            return None

        with open("../../examples/simulations/" + source, 'r') as f:
            source = json.loads(f.read())

        dictionary = {}

        self.load_parameters(dictionary, source)
        self.load_agents(dictionary, source)
        self.load_networks(dictionary, source)
        self.load_environments(dictionary, source)
        self.load_to_dictionary(dictionary, "interactions", source)

        return dictionary

    def load_parameters(self, dictionary, source):
        """ Load general simulation parameters given in source. """

        parameters = ["dump_freq", "num_iter", "alpha", "beta", "sigma"]
        for p in parameters:
            self.load_to_dictionary(dictionary, p, source)

    def load_agents(self, dictionary, source):
        """ Load simulation Agents given in source. """

        agents_source = self.value_if_exist("agents", source)
        agents = []

        if agents_source is not None:
            with open("../../examples/agents/" + agents_source, 'r') as f:
                agents_data = json.loads(f.read())
            source["num_agents"] = len(agents_data)
            for agent in agents_data:
                agents.append(agent)
        else:
            num_agents = self.value_if_exist("num_agents", source)
            for i in range(num_agents):
                agents.append({"node_name": i})

        dictionary["agents"] = agents

    def load_networks(self, dictionary, source):
        """ Load simulation networks given in source. """

        networks_source = self.value_if_exist("networks", source) or [{"type": "clique", "start": 1}]

        networks = []
        for network in networks_source:
            g_type = self.value_if_exist("type", network)
            if g_type is None:
                network_file = self.value_if_exist("source", network)
                g = self.parse_graph(network_file)
            else:
                n = self.value_if_exist("num_agents", source)
                g = graph_generator(g_type, n)
            networks.append({"start": network["start"], "graph": Network(g)})

        dictionary["networks"] = networks

    def load_environments(self, dictionary, source):
        """ Load simulation environments given in source. """

        environment_source = self.value_if_exist("environments", source)

        environments = []
        for environment in environment_source:
            environment_source = self.value_if_exist("source", environment)
            environment["source"] = self.parse_environment(environment_source)
            environments.append(environment)

        dictionary["environments"] = environments

    @staticmethod
    def parse_graph(source):
        """
        Parse graph when given as pygraph in json.

        @type source: String
        @param source: Json document for pygraph directory.

        @rtype: Pygraph
        @return: Returns graph from pygraph library.
        """
        if source is None:
            return None

        with open("../../examples/networks/" + source, 'r') as f:
            graph = json.loads(f.read())

            graph_s = '<?xml version="1.0" ?><graph>'

            for node in graph["nodes"]:
                graph_s += '<node id="%d"/>' % node

            for edge in graph["edges"]:
                graph_s += '<edge from="%d" to="%d" wt="%d"/>' % (edge["from"], edge["to"], edge["wt"])

            graph_s += "</graph>"

            return markup.read(graph_s)

    @staticmethod
    def parse_environment(doc):
        """ Parse environment parameters given in json document. """
        with open("../../examples/environment/" + doc, 'r') as f:
            environment = json.loads(f.read())

        return environment

    @staticmethod
    def load_to_dictionary(dictionary, key, source, obligatory=False, function=None):
        """
        Loads value from key in source to key in dictionary.

        @type dictionary: Map
        @param dictionary: Map which is loaded value.

        @type key: String
        @param key: Key of value loaded.

        @type source: Map
        @param source: Map with value.

        @type obligatory: Bool
        @param obligatory: Key have to be in source.

        @type obligatory: Function
        @param obligatory: Function that have to be used on value before loading into dictionary.
        """
        if key in source:
            if function is None:
                dictionary[key] = source[key]
            else:
                dictionary[key] = function(source[key])
        elif obligatory:
            raise Exception("Information about " + key + " should be written in simulation file.")

    @staticmethod
    def value_if_exist(key, source, function=None):
        """
        Reads value assigned to key from source. If source doesn't contain key return None.

        @type key: String
        @param key: Key of value read.

        @type source: Map
        @param source: Map with value.

        @type function: function
        @param function: Function that have to be used on value after reading.

        @rtype: Any
        @return: Value assigned to key in source or None.
        """
        if key in source:
            if function is None:
                return source[key]
            else:
                return function(source[key])
        else:
            return None
