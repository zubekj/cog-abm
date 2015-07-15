import sys
import logging
import cPickle
from time import localtime, strftime

sys.path.append('../../')
sys.path.append('../')
sys.path.append('')

from cog_simulations.cog_abm.extras.parser import Parser
from steels_experiment import steels_advanced_experiment


if __name__ == "__main__":

    # Setting command lines arguments options.
    import argparse

    parser = argparse.ArgumentParser(description="This program is implementation of Steels simulation.")

    parser.add_argument('-s', '--simulation_file', dest='simulation_file', action='store',
                        default='basic_simulation.json',
                        help="Name of file with simulation parameters."
                             "File should be in directory cog_abm/examples/simulations/ . "
                             "Default: basic_simulation.json")

    parser.add_argument('-r', '--results_file', dest='results_file', action='store',
                        default=strftime("experiment_%Y%m%d_%H_%M_%S.result", localtime()),
                        help='Name of results file. '
                             'It will be write in directory cog_abm/results_of_simulation. '
                             'Default: experiment_date.result')

    parser.add_argument('-v', '--verbose', dest='verbose', action='count',
                        help='Increase verbosity. '
                             '-v - INFO level'
                             '-vv - DEBUG level'
                             'Default: WARNING level')

    parser.add_argument('-l', '--log_file', dest='log_file', action='store',
                        help='Name of file in which will be stored log informations.'
                             'It will be write in directory cog_abm/logs.'
                             'Default: no file will be writen.')

    args = parser.parse_args()

    # Setting log_level and log file whether specified.
    log_level = logging.WARNING

    if args.verbose == 1:
        log_level = logging.INFO

    elif args.verbose >= 2:
        log_level = logging.DEBUG
    # Set up basic configuration, out to std err with a reasonable default format.
    path_to_logs = '../../logs/'
    if args.log_file is not None:
        logging.basicConfig(filename=path_to_logs+args.log_file, level=log_level)
    else:
        logging.basicConfig(level=log_level)

    # Loading parameters from given or default simulation file.
    source_file = args.simulation_file
    params = Parser().parse_simulation(source_file)

    # Main part - running steels experiment.
    r = steels_advanced_experiment(**params)

    # Saving results of simulation.
    path_to_results = "../../results_of_simulation/"
    results_name = args.results_file

    f = open(results_name, "w")
    cPickle.dump((r, params), f)
    f.close()
