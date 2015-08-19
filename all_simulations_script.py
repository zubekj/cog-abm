# -*- coding: utf-8 -*-
# /COG_SIM

import os
import pandas as pd # must be python2
import numpy as np
import cPickle as pickle


networks = {"max_avg_bet", "max_avg_clust", "max_max_bet", "max_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "min_max_clos"}
networks2= {"line", "hub", "ring"}


# simulations

for i in xrange(20):
    
    for network in networks:
        os.system("python cog_simulations/steels/steels_main.py -s examples/simulations/shift_simulations/simulation_" + network + "_to_clique.json -r  results_of_simulation/shift_sim_results/results_" + network + "_to_clique" + format(i))
    for network2 in networks2:
        os.system("python cog_simulations/steels/steels_main.py -s examples/simulations/shift_simulations/simulation_" + network2 + "_to_clique.json -r  results_of_simulation/shift_sim_results/results_" + network2 + "_to_clique" + format(i))


# analyzer

results = {"CSA", "DSA", "CLA", "DG_CLA"}
for i in xrange(20):
    for result in results:
        for network in networks:
            os.system("python cog_simulations/steels/analyzer.py -r results_of_simulation/shift_sim_results/results_" + network + "_to_clique" + format(i) + " it " + result + " > data_" + network + "_to_clique_" + result + "_" + format(i))
        for network2 in networks2:
            os.system("python cog_simulations/steels/analyzer.py -r results_of_simulation/shift_sim_results/results" + network2 + "_to_clique" + format(i) + " it " + result + " > data_" network2 + "_to_clique_" + result + "_" + format(i))

# pandas
# data [network][result][iter][DataFrame]
# czy wywalamy co drugi wiersz?
index=range(2010)[::10]     # jak zrobić listę z krokiem 10?
data = []
stats = pd.DataFrame(index=index)

for network in networks:
    data.append([])
    for result in results:
        data[-1].append([])
        data[-1][-1].append(pd.DataFrame(index=index))#, index_col=[mean_0, var_0,mean_1, var_1, mean_2, var_2, mean_3, var_3, mean_4, var_4, mean_5, var_5, mean_6, var_6, mean_7, var_7, mean_8, var_8, mean_9, var_9, mean_10, var_10, mean_11, var_11, mean_12, var_12, mean_13, var_13, mean_14, var_14, mean_15, var_15, mean_16, var_16, mean_17, var_17, mean_18, var_18, mean_19, var_19])
        for i in xrange(20):
            data[-1][-1].append(pd.read_csv("data_" + network + "_" + result + format(i)), delim_whitespace=True, header=None, index_col=0)
            data[-1][-1][0]["mean_" + format(i)] = data[-1][-1][-1].mean(1)  # mean of i-th simulation
            data[-1][-1][0]["var_" + format(i)] = data[-1][-1][-1].var(1)

# line, hub, ring
for network2 in networks2:
    data.append([])
    for result in results:
        data[-1].append([])
        data[-1][-1].append(pd.DataFrame(index=index))
        for i in xrange(20):
            data[-1][-1].append(pd.read_csv("data_" + network2 + "_" + result + format(i)), delim_whitespace=True, header=None, index_col=0)
            data[-1][-1][0]["mean_" + format(i)] = data[-1][-1][-1].mean(1)  # mean of i-th simulation
            data[-1][-1][0]["var_" + format(i)] = data[-1][-1][-1].var(1)




#   python2 cog_simulations/steels/analyzer.py -r results_of_simulation/shift_sim_results/results_max_max_bet_to_clique0 it CLA > data_max_max_bet_to_clique_0.txt




