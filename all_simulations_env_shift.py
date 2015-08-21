
# -*- coding: utf-8 -*-
# /COG_SIM
import os
import pandas as pd # must be python2
import numpy as np


networks = ["max_avg_bet", "max_avg_clust", "max_max_bet", "max_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "min_max_clos"]
networks2= ["line", "hub", "ring"]


# simulations

for i in xrange(20):
    
    for network in networks+networks2:
        os.system("python cog_simulations/steels/steels_main.py -s examples/simulations/env_shift_simulations_training/simulation_env_shift_training_{0}.json -r  results_of_simulation/env_shift_sim_results/results_env_training{0}{1}".format(network, i))

# analyzer

results = {"CSA", "DSA", "CLA", "DG_CLA"}
for i in xrange(20):
    for result in results:
        for network in networks+networks2:
            os.system("python cog_simulations/steels/analyzer.py -r results_of_simulation/env_shift_sim_results/results_env_training{0}{1} it {2} > env_shift_sim_data/data_env_training{0}{2}_{1}".format(network, i, results))

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
            data_sim = pd.DataFrame(pd.read_csv("env_shift_sim_data/data_env_training{0}{1}_{2}".format(network, result, i)), delim_whitespace=True, header=None, index_col=0)
            mean[i] = (data_sim.mean(1))
            var[i] = (data_sim.var(1))
        data[result + "_mean"][network] = mean.mean(1)
        data[result + "_var"][network] = var.mean(1)


# return stats

with open("simulations_env_shift_results.csv", 'w') as f:
    data.to_csv(f)



