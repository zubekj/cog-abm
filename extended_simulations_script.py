# -*- coding: utf-8 -*-
# /COG_SIM
import os
import re
from multiprocessing import Pool
import pandas as pd  # must be python2


N_PROC = 6

N_SIM = 10

SIM_BASE_DIR = 'examples/simulations/ext_env_shift'
RES_BASE_DIR = 'results_of_simulation/ext_env_shift'
RESULTS_FILE = 'ext_env_shift_results.csv'


def run_simulations():
    print("Results file: " + RESULTS_FILE)
    if os.path.exists(RESULTS_FILE):
        print("Results file exists, exiting!")
        return

    SIMULATION_FILES = [
        os.path.join(SIM_BASE_DIR, fn)
        for fn in os.listdir(SIM_BASE_DIR)
        if fn.endswith('.json')
        ]
    print("Running %d simulations:" % len(SIMULATION_FILES))
    for fn in SIMULATION_FILES:
        print(fn)

    pool = Pool(processes=N_PROC)

    # simulations
    for i in xrange(N_SIM):
        for sim_fname in SIMULATION_FILES:
            res_fname = os.path.join(RES_BASE_DIR, "{0}_{1}.csv".format(os.path.basename(sim_fname), i))
            if not os.path.isfile(res_fname):
                pool.apply_async(os.system, ["python2 cog_simulations/steels/steels_main.py -s {0} -r {1}".format(sim_fname, res_fname)])

    pool.close()
    pool.join()

    print("Simulations done.")


def merge_results():
    RESULTS_PARTS = [
        os.path.join(RES_BASE_DIR, fn)
        for fn in os.listdir(RES_BASE_DIR)
        if fn.endswith('.csv')
    ]

    print("Merging %d results:" % len(RESULTS_PARTS))
    for fn in RESULTS_PARTS:
        print(fn)

    res_dfs = []

    # pandas
    for res_fname in RESULTS_PARTS:
        res = pd.read_csv(res_fname).drop("agent", axis=1).groupby("it")
        res = pd.concat(
            (
                res.mean().rename(columns=lambda c: "{0}_mean".format(c)),
                res.var().rename(columns=lambda c: "{0}_avar".format(c))
            ),
            axis=1
        )
        m = re.match(r"^simulation_N(?P<size>\d+)_(?P<network>\w+)\.json_(?P<isim>\d+)\.csv$", os.path.basename(res_fname))
        res["network"] = m.group('network')
        res["simulation"] = int(m.group('isim'))
        res["network_size"] = int(m.group('size'))
        res_dfs.append(res)

    res = pd.concat(res_dfs)
    res.to_csv(RESULTS_FILE)

    print("Stats done.")


if __name__ == "__main__":
    run_simulations()
    merge_results()
