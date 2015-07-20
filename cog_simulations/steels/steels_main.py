import sys
import logging
import cPickle
from time import localtime, strftime

sys.path.append('../../')
sys.path.append('../')
sys.path.append('')

from cog_simulations.parser import Parser
from cog_simulations.steels.core.steels_experiment import steels_experiment
from cog_simulations.steels.core.steels_experiment_continuation import steels_experiment_continuation

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

    parser.add_argument('-l', '--log_file', dest='log_file', action='store',
                        help='Name of file in which will be stored log information.'
                             'It will be write in directory cog_abm/logs.'
                             'Default: no file will be writen.')

    parser.add_argument('-ss', '--save_simulation', dest='save_simulation', action='store',
                        help='Name of file in which will be stored simulation after its run.'
                             'It will be write in directory cog_abm/results_of_simulation/simulations.'
                             'Default: no file will be writen.')

    parser.add_argument('-c', '--load_simulation', dest='load_simulation', action='store',
                        help='Name of file in which is stimulation to continue.'
                             'It will be read files from directory cog_abm/results_of_simulation/simulations.'
                             'Default: new simulation.')

    parser.add_argument('-n', '--load_network', dest='networks', action='store',
                        help='Name of file in which are networks used in stimulation continuation.'
                             'It will be read files from directory cog_abm/examples/simulations. '
                             'Default: new simulation.')

    parser.add_argument('-v', '--verbose', dest='verbose', action='count',
                        help='Increase verbosity. '
                             '-v - INFO level'
                             '-vv - DEBUG level'
                             'Default: WARNING level')

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

    # Check whether start new simulation or continue old.
    new_simulation = args.simulation_file
    if new_simulation is not None:
        params = Parser().parse_simulation(new_simulation)
        # Main part - running steels experiment.
        results, simulation = steels_experiment(**params)
    else:
        simulation, old_params, new_params = Parser.parse_simulation_continuation(args.load_simulation, args.networks)
        results, simulation, params = steels_experiment_continuation(simulation, old_params, new_params)

    # Saving results of simulation - always.
    path_to_results = "../../results_of_simulation/"
    with open(path_to_results + args.results_file, "w") as f:
        cPickle.dump((results, params), f)

    # Saving whole simulation - only when specified.
    save_simulation = args.save_simulation
    if save_simulation is not None:
        path_to_simulations = "../../results_of_simulation/simulations/"
        with open(path_to_simulations + save_simulation, 'w') as f:
            cPickle.dump((simulation, params), f)
