
# -*- coding: utf-8 -*-
# /COG_SIM
import os
import pandas as pd # must be python2
import numpy as np


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
            os.system("python cog_simulations/steels/analyzer.py -r results_of_simulation/shift_sim_results/results" + network2 + "_to_clique" + format(i) + " it " + result + " > data_" + network2 + "_to_clique_" + result + "_" + format(i))

# pandas
# czy wywalamy co drugi wiersz?
index = range(0, 2010, 10)
columns = []

for result in results:
    columns.append(result + "_mean")
    columns.append(result + "_var")
data = pd.DataFrame(index = networks + networks2, columns = columns)

for result in results:
    for network in networks+networks2:
        mean = pd.DataFrame(index=index)
        var = pd.DataFrame(index=index)
        for i in xrange(20):
            data_sim = pd.DataFrame(pd.read_csv("data_" + network + "_" + result + format(i)), delim_whitespace=True, header=None, index_col=0)
            mean[i] = (data_sim.mean(1))
            var[i] = (data_sim.var(1))
        data[result + "_mean"][network] = mean.mean(1)
        data[result + "_var"][network] = var.mean(1)


# return stats

f=open("simulations_results.csv", 'w')
data.to_csv(f)
f.close()



