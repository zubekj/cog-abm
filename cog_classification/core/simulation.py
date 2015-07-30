class Simulation:
    """ This class represents general logic of multi-agent simulation. """

    def __init__(self, agents, interactions, environment, result, end_condition):
        """
        Args:
            agents (Network): source of agents.
            interactions (Interaction): source of interactions for agents.
            environment (Environment): source of samples for interactions.
            result (Result): object that will accumulate statistics of simulation.
            end_condition (Condition): object that determines end of simulation.
        """

        self.agents = agents
        self.interactions = interactions
        self.environment = environment
        self.result = result
        self.end_condition = end_condition

        self.iteration = 0

    def run(self):
        """
        Starts simulation.

        Returns:
            (Result) result of simulation.
        """
        self.result.save(**self.__dict__)

        while not self.end_condition.end(self.iteration):
            self.iteration += 1

            self.interactions.change(self.iteration)
            self.agents.change(self.iteration)
            self.environment.change(self.iteration)

            self.interactions.interact(self.agents, self.environment)

            self.result.save(**self.__dict__)

        return self.result

    def continue_simulation(self, agents=None, interactions=None, environment=None, result=None, end_condition=None):
        """
        Starts completed simulation from termination point with additional parameters.

        Args:
            like in __init__.

        Returns:
            (Result) result of whole simulation - form start of original simulation.
        """
        self.agents.update(agents, self.iteration)
        self.interactions.update(interactions, self.iteration)
        self.environment.update(environment, self.iteration)
        self.result.update(result, self.iteration)
        self.end_condition.update(end_condition, self.iteration)

        return self.run()
