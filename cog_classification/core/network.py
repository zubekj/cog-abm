import random

from cog_classification.core.changing_class import ChangingClass


class Network(ChangingClass):
    """ This class implements set of agents with changing topology. """

    def __init__(self, agents, topologies, changes):
        """
        Args:
            agents ({agent_name: agent}).
            topologies ({agent_name: [neighbour_name, ...]}):
        """
        super(Network, self).__init__(topologies, changes)
        self.agents = agents

    def get_agent(self):
        """
        Returns:
            (Agent) random agent.
        """
        return random.choice(self.agents.values())

    def get_agents(self, number_of_agents):
        """"
            Returns list of number of agents agents.

            Each two agents in list are connected by the path created by agents in list.
            If in network are isolated subgraph of size less than number of agent then
            this method can return empty list.

            Returns:
                (list of Agents) list of agents in which each two agent are connected
                    by path created by other agents in list.
        """
        agents = []
        agents_names = []
        candidates = []

        # Choosing firs agent.
        agent_name = random.choice(self.agents)
        agents.append(self.agents[agent_name])
        agents_names.append(agent_name)

        current_topology = self.current_behavior
        candidates += current_topology[agent_name]

        for _ in range(number_of_agents - 1):

            if len(candidates) < 1:
                return []
            else:
                new_agent = random.choice(candidates)
                candidates.pop(new_agent)

                agent_name = new_agent
                agents.append(self.agents[agent_name])
                agents_names.append(agent_name)

                # We want to add to candidates only the neighbours of new agent
                # that aren't in chosen agents and candidates.
                agents_not_chosen_yet = set(current_topology[agent_name]) - set(agents)
                candidates += list(agents_not_chosen_yet - set(candidates))

        return agents

    def get_all_agents(self):
        return self.agents.values()
