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
# data[i][j][0] - mean and variance statistics of particular network, result in 20 iterations
# czy wywalamy co drugi wiersz?
index=range(2010)[::10]     # jak zrobić listę z krokiem 10?
data = []
mean_index = []
var_index = []

for network in networks:
    data.append([])
    for result in results:
        data[-1].append([])
        data[-1][-1].append(pd.DataFrame(index=index))#, index_col=[mean_0, var_0,mean_1, var_1, mean_2, var_2, mean_3, var_3, mean_4, var_4, mean_5, var_5, mean_6, var_6, mean_7, var_7, mean_8, var_8, mean_9, var_9, mean_10, var_10, mean_11, var_11, mean_12, var_12, mean_13, var_13, mean_14, var_14, mean_15, var_15, mean_16, var_16, mean_17, var_17, mean_18, var_18, mean_19, var_19])
        for i in xrange(20):
            data[-1][-1].append(pd.read_csv("data_" + network + "_" + result + format(i)), delim_whitespace=True, header=None, index_col=0)
            data[-1][-1][0]["mean_" + result + network + "_" + format(i)] = data[-1][-1][-1].mean(1)  # mean of i-th simulation
            mean_index.append("mean_" + result + network + "_" + format(i))
            data[-1][-1][0]["var_" + result + network + "_" + format(i)] = data[-1][-1][-1].var(1)
            var_index.append("var_" + result + network + "_" + format(i))

# line, hub, ring
for network2 in networks2:
    data.append([])
    for result in results:
        data[-1].append([])
        data[-1][-1].append(pd.DataFrame(index=index))
        for i in xrange(20):
            data[-1][-1].append(pd.read_csv("data_" + network2 + "_" + result + format(i)), delim_whitespace=True, header=None, index_col=0)
            data[-1][-1][0]["mean_" + result + network2 + "_" + format(i)] = data[-1][-1][-1].mean(1)  # mean of i-th simulation
            data[-1][-1][0]["var_" + result + network2 + "_" + format(i)] = data[-1][-1][-1].var(1)

stats = pd.DataFrame(index=index) # final statistics with mean and variance
i = 0   #networks count
j = 0   #resuts count
for result in results:
    for network in networks:
        stats[result + network + "mean"] = data[i][j][0][mean_index].mean(1)
        stats[result + network + "var"] = data[i][j][0][var_index].mean(1)
        i += 1
    for network2 in networks2:
        i += 1
        stats[result + network + "mean"] = data[i][j][0][mean_index].mean(1)
        stats[result + network + "var"] = data[i][j][0][var_index].mean(1)
    j += 1
    i = 0

# return stats




