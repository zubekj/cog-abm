class Result:
    """
    Class that collects results of simulation.
    """

    def __init__(self):
        self.results = {}

    def save(self, agents, interactions, environment, result, end_condition, iteration):
        pass

    def get_results(self):
        return self.results

class StandardResult(Result):
    """
    Class that saves all agents statistics every given time.
    """

    def __init__(self, gap=50):
        Result.__init__(self)
        self.gap = gap

    def save(self, agents, interactions, environment, result, end_condition, iteration):
        """
        Saves all agents fitness measures if iteration number is divided by gap.
        """
        if iteration % self.gap == 0:

            results = {"iteration": iteration}

            for agent in agents.get_all_agents():
                for fitness_name in agent.get_fitness_measures():

                    fitness_measure = agent.get_fitness_measure(fitness_name)

                    if fitness_name in results:
                        results[fitness_name].append(fitness_measure)
                    else:
                        results[fitness_name] = [fitness_measure]

            self.results[iteration / self.gap] = results
