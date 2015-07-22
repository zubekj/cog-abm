from nose.tools import assert_equals

from cog_classification.core.agent import Agent


def test_id_creation_exact_numbers():
    for i in range(100):
        assert_equals(Agent().get_id(), i)
