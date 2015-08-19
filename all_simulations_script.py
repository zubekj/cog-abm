# -*- coding: utf-8 -*-
# /COG_SIM

import os
import pandas as pd # must be python2
import numpy as np
import cPickle as pickle


networks = {"max_avg_bet", "max_avg_clust", "max_max_bet", "max_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "min_max_clos"}


# simulations

for i in xrange(20):
    
    for network in networks:
        os.system("python cog_simulations/steels/steels_main.py -s examples/simulations/shift_simulations/simulation_" + network + "_to_clique.json -r  results_of_simulation/shift_sim_results/results_" + network + "_to_clique" + format(i))
    
    os.system("python cog_simulations/steels/steels_main.py -s /../../examples/simulations/shift_simulations/simulation_line_to_clique.json -r  /../../results_of_simulation/shift_sim_results/results_line_to_clique" + format(i))
    os.system("python cog_simulations/steels/steels_main.py -s /../../examples/simulations/shift_simulations/simulation_hub_to_clique.json -r  /../../results_of_simulation/shift_sim_results/results_hub_to_clique" + format(i))
    os.system("python cog_simulations/steels/steels_main.py -s /../../examples/simulations/shift_simulations/simulation_ring_to_clique.json -r  /../../results_of_simulation/shift_sim_results/results_ring_to_clique" + format(i))


# analyzer

results = {"CSA", "DSA", "CLA", "DG_CLA"}
for i in xrange(20):
    for result in results:
        for network in networks:
            os.system("python cog_simulations/steels/analyzer.py -r /../../results_of_simulation/shift_sim_results/results_" + network + "_to_clique" + format(i) + " it " + result + " > data_" + network + "_to_clique_" + result + "_" + format(i))

        os.system("python cog_simulations/steels/analyzer.py -r /../..results_of_simulation/shift_sim_results/results_line_to_clique" + format(i) + " it " + result + " > data_line_to_clique_" + result + "_" + format(i))
        os.system("python cog_simulations/steels/analyzer.py -r /../..results_of_simulation/shift_sim_results/results_hub_to_clique" + format(i) + " it " + result + " > data_hub_to_clique_" + result + "_" + format(i))
        os.system("python cog_simulations/steels/analyzer.py -r /../..results_of_simulation/shift_sim_results/results_hub_to_clique" + format(i) + " it " + result + " > data_hub_to_clique_" + result + "_" + format(i))


# pandas
# stat [network][result][iter][DataFrame]

stat = []
for network in networks:
    stat.append([])
    for result in results:
        stat[-1].append([])
        for i in xrange(20):
            stat[-1][-1].append(pd.read_csv("data_" + network + "_" + result + format(i)), delim_whitespace=True, header=None, index_col=0)
# line, hub, ring
stat.append([])
for result in results:
    stat[-1].append([])
    for i in xrange(20):
        stat[-1][-1].append(pd.read_csv("data_line_" + result + format(i)), delim_whitespace=True, header=None, index_col=0)
stat.append([])
for result in results:
    stat[-1].append([])
    for i in xrange(20):
        stat[-1][-1].append(pd.read_csv("data_hub_" + result + format(i)), delim_whitespace=True, header=None, index_col=0)
stat.append([])
for result in results:
    stat[-1].append([])
    for i in xrange(20):
        stat[-1][-1].append(pd.read_csv("data_ring_" + result + format(i)), delim_whitespace=True, header=None, index_col=0)




#pd.read_csv('data_ring_DSA9.txt', delim_whitespace=True, header=None, idndex_col=0)

