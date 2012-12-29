'''

Created on Dec 29, 2012

@author: mlukasik
'''
import sys
sys.path.append('../')
import unittest
from cog_abm.extras.words_storage import *


class TestGetAgentsWords(unittest.TestCase):

    class Agent(object):
        def __init__(self):
            self.namings = {}
            self.state = self#state is agent itself
        def sense_and_classify(self, s):
            return self.namings[s]
        def word_for(self, s):#word_for does nothing - just passes the classification
            return s
    
    def test_divided_by_parity(self):
        #init:
        agents = [TestGetAgentsWords.Agent() for _ in xrange(10)]
        colours = range(15)
        for ind_a, a in enumerate(agents):
            for ind_col, col in enumerate(colours):
                a.namings[col] = str(ind_col)
        
        colour_order = [i for i in colours if i%2==0] + [i for i in colours if i%2!=0]
        #[0, 2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13]
        expected_names = [str(i) for i in colour_order]
        expected_result = {}
        for ind_a in xrange(len(agents)):
            expected_result[ind_a] = expected_names
        
        self.assertEqual(get_agents_words(agents, colour_order), expected_result)

class TestConvert2numerical(unittest.TestCase):

    def test_simple(self):
        numerical_d = convert2numerical({0: ["a", "b", "c", "b", 'None'], 1: ["a", "c", "e", "b", "f"]})
        self.assertEqual(numerical_d, {0: [1, 2, 3, 2, -1], 1: [1, 3, 4, 2, 5]})
        

if __name__ == '__main__':
    unittest.main()
