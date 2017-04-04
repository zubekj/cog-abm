# -*- coding: utf-8 -*-
# /COG_SIM
import os
from multiprocessing import Pool
import pandas as pd # must be python2

N_PROC = 2
N_SIM = 10
SIMULATION_FILES = [
    "examples/simulations/naming_game_topology_shift/simulation_naming_game_topology_shift_clique.json",
    "examples/simulations/naming_game_topology_shift/simulation_naming_game_topology_shift_hub_hearer.json",
    "examples/simulations/naming_game_topology_shift/simulation_naming_game_topology_shift_hub.json",
    "examples/simulations/naming_game_topology_shift/simulation_naming_game_topology_shift_hub_speaker.json",
]
RESULTS_FILE = "naming_game_topology_shift_results.csv"


pool = Pool(processes=N_PROC)

# simulations
for i in xrange(N_SIM):
    for sim_fname in SIMULATION_FILES:
        res_fname = "results_of_simulation/{0}_{1}.csv".format(
            os.path.basename(sim_fname), i)
        if not os.path.isfile(res_fname):
            pool.apply_async(os.system, ["python2 cog_simulations/steels/steels_main.py -s {0} -r {1}".format(sim_fname, res_fname)])

pool.close()
pool.join()

res_dfs = []

# pandas
for i in xrange(N_SIM):
    for sim_fname in SIMULATION_FILES:
        res_fname = "results_of_simulation/{0}_{1}.csv".format(
            os.path.basename(sim_fname), i)
        res = pd.read_csv(res_fname).drop("agent", axis=1).groupby("it")
        res = pd.concat((res.mean().rename(columns=lambda c: "{0}_mean".format(c)),
                         res.var().rename(columns=lambda c: "{0}_avar".format(c))), axis=1)
        res["network"] = ".".join(os.path.basename(sim_fname).split(".")[:-1])
        res["simulation"] = i
        res_dfs.append(res)

res = pd.concat(res_dfs)
res.to_csv(RESULTS_FILE)
