import sys
import logging
import cPickle
from time import localtime, strftime
from src.cog_abm.core.environment import *


def save_res(results, f_name=None):
    """
    Write results to file.

    @type results: Object
    @param results: Object to be saved.

    @type f_name: String
    @param f_name: Name of file we want to save results in.
    """
    if f_name is None:
        f_name = strftime("experiment_%Y%m%d_%H_%M_%S.result", localtime())
    f = open(f_name, "w")
    cPickle.dump(results, f)
    f.close()


def load_params(simulation):
    """
    Loads parameters from simulation file or set default.

    @type simulation: String
    @param simulation: Path to simulation file.
    """
    if simulation is None:
        return default_params()

    from src.cog_abm.extras.parser import Parser
    return Parser().parse_simulation(simulation)


def default_params():
    from src.cog_abm.extras.color import get_1269Munsell_chips
    return {
        'dump_freq': 100,
        'num_iter': 1000,
        'learning': {
            'alpha': 0.1,
            'beta': 1.,
            'sigma': 10.
        },
        'stimuli': get_1269Munsell_chips(),
        'environments': [{'start': 1,
                          'environment': Environment(get_1269Munsell_chips(), RandomStimuliChooser(), None)}],
        'environment': Environment(get_1269Munsell_chips(), RandomStimuliChooser(), None),
        'interactions': [
            {'start': 1,
             'interaction': {
                 'interaction_type': 'DG',
                 'context_size': 4,
                 'inc_category_threshold': 0.95
             }}
        ],
        'num_agents': 10
    }


if __name__ == "__main__":

    import optparse

    opt_p = optparse.OptionParser()

    opt_p.add_option('-v', '--verbose', dest='verbose', action='count',
                     help="Increase verbosity (specify multiple times for more)")
    opt_p.add_option('-f', '--file', action="store", dest='file', type="string",
                     help="output file with results")
    opt_p.add_option('-p', '--params_file', action="store", dest='param_file',
                     type="string", help="file with parameters")

    # Parse the arguments (defaults to parsing sys.argv).
    opts, args = opt_p.parse_args()

    log_level = logging.DEBUG  # default logging.WARNING

    if opts.verbose == 1:
        log_level = logging.INFO

    elif opts.verbose >= 2:
        log_level = logging.DEBUG
    # Set up basic configuration, out to stderr with a reasonable default format.
    logging.basicConfig(level=log_level)

    sys.path.append('../')
    sys.path.append('')
    from src.steels.steels_experiment import steels_advanced_experiment

    params = load_params(opts.param_file)

    r = steels_advanced_experiment(**params)
    save_res((r, params), "../../results/" + opts.file)
