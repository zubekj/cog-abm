# -*- coding: utf-8 -*-
# /COG_SIM
import os
from multiprocessing import Pool
import pandas as pd # must be python2

N_PROC = 2



networks = ["max_avg_bet", "max_avg_clust", "max_max_bet", "max_max_clos",
            "max_var_cons", "min_avg_bet", "min_avg_clust", "min_max_clos"]
networks2= ["line", "hub", "ring", "clique"]
results = {"CSA", "DSA", "CLA", "DG_CLA", "cc"}

pool = Pool(processes=N_PROC)

# simulations
for i in xrange(20):
    for network in networks+networks2:
        res_fname = "results_of_simulation/env_shift_sim_results/results_{0}{1}".format(network, i)
        if not os.path.isfile(res_fname):
            pool.apply_async(os.system, ["python2 cog_simulations/steels/steels_main.py -s examples/simulations/env_shift_simulations/simulation_env_shift_training_{0}.json -r {1}".format(network, res_fname)])

pool.close()
pool.join()

pool = Pool(processes=N_PROC)

# analyzer
for i in xrange(20):
    for result in results:
        for network in networks+networks2:
            res_fname = "results_of_simulation/env_shift_sim_data/data_env_training{0}{2}_{1}".format(network, i, result)
            if not os.path.isfile(res_fname):
                pool.apply_async(os.system, ["python2 cog_simulations/steels/analyzer.py -r results_of_simulation/env_shift_sim_results/results_{0}{1} it {2} > {3}".format(network, i, result, res_fname)])

pool.close()
pool.join()

# pandas
# czy wywalamy co drugi wiersz?
index = range(0, 20010, 50)
columns = []

for result in results:
    columns.append(result + "_mean")
    columns.append(result + "_var")

mindex = pd.MultiIndex.from_product((networks + networks2, index))
data = pd.DataFrame(index=mindex, columns=columns)

for result in results:
    for network in networks+networks2:
        mean = pd.DataFrame(index=index)
        var = pd.DataFrame(index=index)
        for i in xrange(20):
            data_sim = pd.read_csv(
                "results_of_simulation/env_shift_sim_data/data_env_training{0}{1}_{2}".format(network, result, i),
                delim_whitespace=True, header=None, index_col=0)
            mean[i] = (data_sim.mean(1))
            var[i] = (data_sim.var(1))
        data[result + "_mean"][network] = mean.mean(1)
        data[result + "_var"][network] = var.mean(1)

for network in networks+networks2:
    data2 = pd.concat([pd.read_csv("results_of_simulation/env/shift_sim_data/data_env_training{0}cc_{1}".format(network, i), delim_whitespace=True, header=None, index_col=0)
                       for i in xrange(20)], axis=2)
    data2 = data2.mean(axis=2)


with open("env_shift_sim_results.csv", 'w') as f:
    data.to_csv(f)

with open("env_shift_sim_cc_extended.csv", 'w') as f:
    data2.to_csv(f)
