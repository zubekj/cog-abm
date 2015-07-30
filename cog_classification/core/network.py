import random


class Network:

    def __init__(self, agents, topologies, changes):
        self.agents = agents
        self.topologies = topologies
        self.changes = changes
        self.current_topology = None

    def change(self, iteration_number):
        if iteration_number in self.changes:
            self.current_topology = self.topologies[self.changes[iteration_number]]
            self.changes.pop(iteration_number)

    def get_agent(self):
        return random.choice(self.agents.values())

    def get_agents(self, number_of_agents):
        agents = []
        agents_names = []

        agent_name = random.choice(self.agents)
        agents.append(self.agents[agent_name])
        agents_names.append(agent_name)

        for _ in range(number_of_agents - 1):

            new_agent = None
            while new_agent is None:
                agent_name = random.choice(agents_names)
                new_agent = self.get_neighbour_other_than_agents(agent_name, agents_names)

            agent_name = new_agent
            agents.append(self.agents[agent_name])
            agents_names.append(agent_name)

        return agents

    def get_all_agents(self):
        return self.agents.values()

    def get_neighbour_other_than_agents(self, agent_name, agents):
        candidates = list(set(self.current_topology[agent_name]) - set(agents))
        if candidates is []:
            return None
        else:
            return random.choice(candidates)
