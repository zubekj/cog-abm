from multiprocessing import Lock


class Agent:
    """ Class representing agent in the system. """

    # AID is set that it will match networks nodes.
    AID = 0
    AID_lock = Lock()

    def __init__(self, aid=None):
        self.id = aid or Agent.get_next_id()

        # Fitness is dictionary of agent's fitness measures.
        self.fitness = {}

    def update_fitness(self, name, information):
        """
        Gives information to fitness measure with a specific name.
        """
        self.fitness[name].update(information)

    @classmethod
    def get_next_id(cls):
        """
        Generates new unique id for agent.

        It asserts that user doesn't specify id value for any agent.
        """
        cls.AID_lock.acquire()
        aid = cls.AID
        cls.AID += 1
        cls.AID_lock.release()
        return aid

    def get_fitness_measure(self, fitness_name):
        """
        Returns value of fitness measure with a specific fitness_name.
        """
        return self.fitness[fitness_name].get_measure()

    def get_fitness_measures(self):
        """
        Returns names of all agent fitness measures.
        """
        return self.fitness.keys()

    def get_id(self):
        return self.id

    def set_fitness(self, name, fitness_measure):
        """
        Adds given fitness measure with a specific name.
        """
        self.fitness[name] = fitness_measure
