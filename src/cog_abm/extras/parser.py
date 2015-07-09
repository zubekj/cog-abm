"""
Module provides parser for json documents.
"""
import json
from pygraph.readwrite import markup
from cog_abm.core.network import Network
from cog_abm.core.agent import *
from cog_abm.core.environment import *
from cog_abm.extras.color import Color
from cog_abm.extras.extract_colour_order import extract_colour_order


class Parser(object):
    """
    Parser class.

    Parser provides methods used to handle simulation input when given in json.

    @sort: __init__, open_document, parse_agent, parse_agents, parse_graph,
    parse_param
    """

    def __init__(self):
        """
        Initialize parser.
        """
        self.environment_parser_map = {}
        self.init_environment_dictionary()
        self.interaction_parser_map = {}
        self.init_interaction_dictionary()

    def init_environment_dictionary(self):
        self.environment_parser_map["CIELab"] = self.parse_munsell_environment

    def init_interaction_dictionary(self):
        self.interaction_parser_map["DiscriminationGame"] = \
            self.parse_discrimination_game
        self.interaction_parser_map["GuessingGame"] = self.parse_guessing_game
        # self.interaction_parser_map["3"] = self.parse_genetic_game

    def parse_agent(self, agent, network, network2=None):
        """
        Parse agent properties when given as map.

        @type agent: map
        @param agent: map representing agent.

        @type simulation: simulation
        @param simulation: Simulation object
        """
        # TODO:
        # id = self.value_if_exist("id", agent)
        # env_name = self.value_if_exist("environment", agent)
        node_name = self.value_if_exist("node_name", agent)
        # sensor = agent.getElementsByTagName("sensor")
        # sensor_type = sensor[0].getElementsByTagName("type")[0].firstChild.dat
        # lrn = agent.getElementsByTagName("classifier")
        # lrn_type = lrn[0].getElementsByTagName("type")[0].firstChild.data

        agent = Agent()
        if network is not None:
            network.add_agent(agent, node_name)
        if network2 is not None:
            network2.add_agent(agent, node_name)
        return agent

    def parse_agents(self, source, network, network2=None):
        """
        Parse agents when given in json.

        @type network: Network
        @param network: agents topology

        @type source: String
        @param source: json document for pygraph directory.
        """
        if source is None:
            return None

        with open("../../examples/agents/" + source, 'r') as f:
            agents_data = json.loads(f.read())

        agents = []

        for agent in agents_data:
            agents.append(self.parse_agent(agent, network, network2))

        return agents

    def parse_environment(self, doc, main_sock=None):
        """
        Parse environment parameters given in json document.

        @type doc: String
        @param doc: JSON document directory.

        @rtype: Environment
        @return: Parsed environment
        """
        with open(doc, 'r') as f:
            data = json.loads(f.read())

        env = self.value_if_exist("stimuli", data)
        env_type = self.value_if_exist("type", data)
        environment = self.environment_parser_map[env_type](env, main_sock)
        return environment

    @staticmethod
    def parse_graph(source):
        """
        Parse graph when given as pygraph in json.

        @type source: String
        @param source: json document for pygraph directory.

        @rtype: pygraph
        @return: Returns graph from pygraph library.
        """
        if source is None:
            return None
        with open("../../examples/networks/" + source, 'r') as f:
            graph = json.loads(f.read())

            x = '<?xml version="1.0" ?><graph>'
            for node in graph["nodes"]:
                x += '<node id="' + str(node) + '"/>'
            for edge in graph["edges"]:
                x += '<edge from="' + str(edge["from"]) + \
                     '" to="' + str(edge["to"]) + '" wt="' + str(edge["wt"]) + '"/>'
            x += "</graph>"
            return Network(markup.read(x))

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

        self.load_to_dictionary(dictionary, "dump_freq", source)
        networks_source = self.value_if_exist("networks", source)
        networks = []
        for net in networks_source:
            graph = self.parse_graph(net["source"])
            networks.append({"graph": graph, "start": net["start"]})
        dictionary["networks"] = networks

        environments = {}
        envs = self.value_if_exist("environment", source)
        for env in envs:
            env_name = self.value_if_exist("name", env)
            env_source = self.value_if_exist("source", env)
            environments[env_name] = self.parse_environment(env_source, env)

        dictionary['stimuli'] = environments['global'].stimuli
        dictionary['environment'] = environments['global']
        dictionary["agents"] = self.parse_agents(self.value_if_exist("agents", source),
                                                 dictionary["network"],
                                                 self.value_if_exist("network2", source))

        # inters = sock.getElementsByTagName("interaction")
        # inter = self.return_element_if_exist(sock, "interaction", False)
        # for i in inters:
        inter = self.value_if_exist("interaction", source)
        dictionary.update(self.interaction_parser_map[self.value_if_exist("type", inter)]
                          (self.value_if_exist("params", inter)))

        return dictionary

    def parse_munsell_environment(self, env, main_sock):
        list_of_stimuli = []

        for stimulus in env:
            l = self.value_if_exist("L", stimulus)
            a = self.value_if_exist("a", stimulus)
            b = self.value_if_exist("b", stimulus)
            list_of_stimuli.append(Color(l, a, b))

        params = self.value_if_exist("params", main_sock)

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
        params = self.value_if_exist("params", inter)
        if params is None:
            return {}

        parameters = ["num_iter", "num_iter2", "learning2", "context_size",
                      "alpha", "beta", "sigma", "inc_category_treshold", "classifier"]

        for p in parameters:
            self.load_to_dictionary(dictionary, p, params)

        return dictionary

    def parse_discrimination_game(self, inter):
        dictionary = {"interaction_type": "DG"}
        return self.parse_game(dictionary, inter)

    def parse_guessing_game(self, inter):
        dictionary = {"interaction_type": "GG"}
        return self.parse_game(dictionary, inter)

    @staticmethod
    def load_to_dictionary(dictionary, key, source, obligatory=False, function=None):
        if key in source:
            if function is None:
                dictionary[key] = source[key]
            else:
                dictionary[key] = function(source[key])
        elif obligatory:
            raise Exception("Information about " + key + " should be written in simulation file.")

    @staticmethod
    def value_if_exist(key, source, function=None):
        if key in source:
            if function is None:
                return source[key]
            else:
                return function(source[key])
        else:
            return None
