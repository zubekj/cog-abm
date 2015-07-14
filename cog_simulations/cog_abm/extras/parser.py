"""
Module provides parser for json documents.
"""
import json
from pygraph.readwrite import markup
from cog_simulations.cog_abm.core.network import Network
from cog_simulations.cog_abm.core.agent import *
from cog_simulations.cog_abm.core.environment import *
from cog_simulations.cog_abm.extras.color import Color
from cog_simulations.cog_abm.extras.extract_colour_order import extract_colour_order
from cog_simulations.cog_abm.extras.additional_tools import generate_clique_network, generate_hub_network,\
    generate_line_network, generate_ring_network


class Parser(object):
    """
    Parser class.

    Parser provides methods used to handle simulation input when given in json.

    @sort: __init__
    """

    def __init__(self):
        """
        Initialize parser.
        """
        self.environment_parser_map = {}
        self.init_environment_dictionary()
        self.interaction_parser_map = {}
        self.init_interaction_dictionary()
        self.graph_parser_map = {}
        self.init_graph_dictionary()

    def init_environment_dictionary(self):
        self.environment_parser_map["CIELab"] = self.parse_munsell_environment

    def init_interaction_dictionary(self):
        self.interaction_parser_map["DiscriminationGame"] = \
            self.parse_discrimination_game
        self.interaction_parser_map["GuessingGame"] = self.parse_guessing_game

    def init_graph_dictionary(self):
        self.graph_parser_map["Line"] = generate_line_network
        self.graph_parser_map["Hub"] = generate_hub_network
        self.graph_parser_map["Ring"] = generate_ring_network
        self.graph_parser_map["Clique"] = generate_clique_network

    def parse_agent(self, agent, networks):
        """
        Parse agent properties when given as map.

        @type agent: Map
        @param agent: Map representing Agent.

        @type networks: List of Networks
        @param networks: List of Networks in which agent is set.

        @rtype: Agent
        @return: Parsed Agent.
        """

        node_name = self.value_if_exist("node_name", agent)
        agent = Agent()

        for network in networks:
            network["graph"].add_agent(agent, node_name)

        return agent

    def parse_agents(self, source, networks):
        """
        Parse agents when given in json.

        @type source: String
        @param source: Json document for pygraph directory.

        @type networks: Networks
        @param networks: List of Networks in which Agents are set.

        @rtype: List of Agent
        @return: List of parsed Agents.
        """
        if source is None:
            return None

        with open("../../examples/agents/" + source, 'r') as f:
            agents_data = json.loads(f.read())

        agents = []

        for agent in agents_data:
            agents.append(self.parse_agent(agent, networks))

        return agents

    def parse_environment(self, doc, source_map):
        """
        Parse environment parameters given in json document.

        @type doc: String
        @param doc: JSON document directory.

        @type doc: Map
        @param doc: Map with environment attributes described in simulation file.

        @rtype: Environment
        @return: Parsed Environment.
        """
        with open("../../examples/environment/" + doc, 'r') as f:
            data = json.loads(f.read())

        env = self.value_if_exist("stimuli", data)
        env_type = self.value_if_exist("type", data)
        environment = self.environment_parser_map[env_type](env, source_map)
        return environment

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

            return Network(markup.read(graph_s))

    def parse_graphs(self, graphs_data, n=None):
        networks = []
        for net in graphs_data:
            source = self.value_if_exist("source", net)
            if source is None:
                graph = self.graph_parser_map[net["Type"]](n)
            else:
                graph = self.parse_graph(source)
            networks.append({"graph": graph, "start": net["start"]})

        return networks

    def parse_simulation(self, source):
        """
        Parse simulation parameters given in json document.

        @type source: String
        @param source: Simulation JSON document directory.

        @rtype: Dictionary
        @return: Simulation params created from json document.
        """
        if source is None:
            return None

        with open("../../examples/simulations/" + source, 'r') as f:
            source = json.loads(f.read())

        dictionary = {}

        # Read standard simulation parameters.
        parameters = ["dump_freq", "num_iter", "learning"]
        for p in parameters:
            self.load_to_dictionary(dictionary, p, source)

        # Read Agents.
        agents = self.value_if_exist("agents", source)

        # Read Networks.
        networks_source = self.value_if_exist("networks", source)
        dictionary["networks"] = self.parse_graphs(networks_source)

        # Bind agents to network.
        dictionary["agents"] = self.parse_agents(agents, dictionary["networks"])

        # Read Environments and stimuli.
        environments = []
        envs = self.value_if_exist("environments", source)
        for env in envs:
            env_name = self.value_if_exist("name", env)
            env_source = self.value_if_exist("source", env)
            environment = self.parse_environment(env_source, env)
            if env_name == "global":
                dictionary['stimuli'] = environment.stimuli
                dictionary['environment'] = environment
            environments.append({"start": env["start"], "environment": environment})

        dictionary['environments'] = environments

        # Read Interactions.
        interactions_source = self.value_if_exist("interactions", source)
        interactions = []
        for i in interactions_source:
            int_type = self.value_if_exist("type", i)
            inter = self.interaction_parser_map[int_type](i)
            interactions.append({"start": i["start"], "interaction": inter})

        dictionary["interactions"] = interactions

        return dictionary

    def parse_munsell_environment(self, env, parameters):
        """
        Parse environment given in map.

        @type env: Map
        @param env: Map with environments stimuli.

        @type parameters: Map
        @param parameters: All environment attributes given in simulation.

        @rtype: Environment
        @return: Parsed Environment.
        """
        list_of_stimuli = []

        for stimulus in env:
            l = self.value_if_exist("L", stimulus)
            a = self.value_if_exist("a", stimulus)
            b = self.value_if_exist("b", stimulus)
            list_of_stimuli.append(Color(l, a, b))

        params = self.value_if_exist("params", parameters)

        colour_order = None
        if params is not None:
            dist = self.value_if_exist("distance", params)
            chooser = RandomStimuliChooser(use_distance=True, distance=dist)

            word_naming_per_color = self.value_if_exist("word_naming_per_color", params)
            if word_naming_per_color:
                colour_order = extract_colour_order(list_of_stimuli, word_naming_per_color)
        else:
            chooser = RandomStimuliChooser()

        return Environment(list_of_stimuli, chooser, colour_order)

    def parse_game(self, dictionary, inter):
        """
        Parse standard steels game parameters.

        @type dictionary: Map
        @param dictionary: Map with already read parameters.

        @type inter: Map
        @param inter: Map with other parameters.

        @rtype: Map
        @return: Map which contains all game parameters.
        """
        params = self.value_if_exist("params", inter)
        if params is None:
            return {}

        parameters = ["context_size", "learning", "inc_category_threshold"]

        for p in parameters:
            self.load_to_dictionary(dictionary, p, params)

        return dictionary

    def parse_discrimination_game(self, inter):
        """
        Parse discrimination game parameters.

        @type inter: Map
        @param inter: Map with game parameters.

        @rtype: Map
        @return: Map which contains all discrimination game parameters.
        """
        dictionary = {"interaction_type": "DG"}
        return self.parse_game(dictionary, inter)

    def parse_guessing_game(self, inter):
        """
        Parse guessing game parameters.

        @type inter: Map
        @param inter: Map with game parameters.

        @rtype: Map
        @return: Map which contains all guessing game parameters.
        """
        dictionary = {"interaction_type": "GG"}
        return self.parse_game(dictionary, inter)

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
