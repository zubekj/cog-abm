""" Module implementing agent in the system. """

from multiprocessing import Lock


class Agent(object):
    """
    Class representing agent in the system.
    """

    # AID is set that it will match networks nodes.
    AID = 0
    AID_lock = Lock()

    def __init__(self, aid=None, classifier=None):
        self.id = aid or Agent.get_next_id()

    @classmethod
    def get_next_id(cls):
        cls.AID_lock.acquire()
        aid = cls.AID
        cls.AID += 1
        cls.AID_lock.release()
        return aid

    def get_id(self):
        return self.id


