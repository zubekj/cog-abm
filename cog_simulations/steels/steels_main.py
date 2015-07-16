import sys
import json
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

    # Loading parameters from given or default simulation file.
    path_to_simulations = "../../results_of_simulation/simulations/"
    open_simulation = args.load_simulation
    if open_simulation is not None:
        f = open(path_to_simulations + open_simulation, 'r')
        (loaded_simulation, params) = cPickle.load(f)
        f.close()

        path_to_networks = "../../examples/simulations/"
        f = open(path_to_networks + args.networks, 'r')
        networks_source = json.load(f)

        logging.debug(loaded_simulation.get_agents())
        logging.debug(len(loaded_simulation.get_agents()))

        networks_source["num_agents"] = len(loaded_simulation.get_agents())
        f.close()
        networks = {}
        Parser.load_networks(Parser(), networks, networks_source)

        params["num_iter"] += networks_source["num_iter"]
        old_iteration = loaded_simulation.get_iteration_counter()
        networks = networks["networks"]
        for network in networks:
            logging.debug(network)
            network["start"] += old_iteration - 1
            params["networks"].append(network)


        logging.debug('Networks: ' + str(networks))

        logging.debug(networks)
        iteration_number = networks_source["num_iter"]
        dump_freq = params["dump_freq"]
        # Main part - continuing steels experiment.
        results, simulation = steels_experiment_continuation(loaded_simulation, networks, iteration_number, dump_freq)
    else:
        source_file = args.simulation_file
        params = Parser().parse_simulation(source_file)
        # Main part - running steels experiment.
        results, simulation = steels_experiment(**params)

    # Saving results of simulation.
    path_to_results = "../../results_of_simulation/"
    results_name = path_to_results + args.results_file
    f = open(results_name, "w")
    cPickle.dump((results, params), f)
    f.close()

    save_simulation = args.save_simulation
    if save_simulation is not None:
        f = open(path_to_simulations + save_simulation, 'w')
        cPickle.dump((simulation, params), f)
        f.close()
