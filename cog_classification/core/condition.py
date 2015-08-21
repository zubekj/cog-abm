class Condition:
    """ Class wrapping condition of experiment end. """

    def __init__(self):
        pass

    def end(self, simulation):
        """ Test whether simulation parameters are suitable for simulation end. """
        pass

    def update(self, condition):
        """ Changes behavior of self depending on condition. """
        pass


class IterationCondition(Condition):
    """ Class implementing plain stop iteration. """

    def __init__(self, max_iterations):
        self.max_iterations = max_iterations

    def end(self, simulation):
        return simulation.iteration >= self.max_iterations

    def update(self, condition):
        self.max_iterations += condition.get_max_iterations

    def get_max_iterations(self):
        return self.max_iterations
