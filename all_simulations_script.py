# -*- coding: utf-8 -*-
# /COG_SIM
import os
import pandas as pd # must be python2

networks = ["max_avg_bet", "max_avg_clust", "max_max_bet", "max_max_clos",
            "max_var_cons", "min_avg_bet", "min_avg_clust", "min_max_clos"]
networks2= ["line", "hub", "ring"]
results = {"CSA", "DSA", "CLA", "DG_CLA"}

# simulations
for i in xrange(20):
    for network in networks+networks2:
        res_fname = "results_of_simulation/shift_sim_results/results_{0}_to_clique{1}".format(network, i)
        if not os.path.isfile(res_fname):
            os.system("python2 cog_simulations/steels/steels_main.py -s examples/simulations/shift_simulations/simulation_{0}_to_clique.json -r {1}".format(network, res_fname))

# analyzer
for i in xrange(20):
    for result in results:
        for network in networks+networks2:
            res_fname = "results_of_simulation/shift_sim_data/data_{0}_to_clique_{2}{1}".format(network, i, result)
            if not os.path.isfile(res_fname):
                os.system("python2 cog_simulations/steels/analyzer.py -r results_of_simulation/shift_sim_results/results_{0}_to_clique{1} it {2} > {3}".format(network, i, result, res_fname))

# pandas
# czy wywalamy co drugi wiersz?
index = range(0, 2010, 50)
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
                "results_of_simulation/shift_sim_data/data_{0}_to_clique_{1}{2}".format(network, result, i),
                delim_whitespace=True, header=None, index_col=0)
            mean[i] = (data_sim.mean(1))
            var[i] = (data_sim.var(1))
        data[result + "_mean"][network] = mean.mean(1)
        data[result + "_var"][network] = var.mean(1)

with open("simulations_results.csv", 'w') as f:
    data.to_csv(f)
