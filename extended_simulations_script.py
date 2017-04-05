# -*- coding: utf-8 -*-
# /COG_SIM
import os
import re
import concurrency.futures as cf
import pandas as pd  # must be python2


N_PROC = 6
N_SIM = 10


def run_simulations(sim_base_dir, res_base_dir, n_sim, n_proc):

    simulation_files = [
        os.path.join(sim_base_dir, fn)
        for fn in os.listdir(sim_base_dir)
        if fn.endswith('.json')
        ]
    print("Running %d simulations:" % len(simulation_files))
    for fn in simulation_files:
        print(fn)

    future_to_desc = {}
    with cf.ProcessPoolExecutor(max_workers=n_proc) as ex:
        # simulations
        for i in range(N_SIM):
            for sim_fname in simulation_files:
                res_fname = os.path.join(res_base_dir, "{0}_{1}.csv".format(os.path.basename(sim_fname), i))
                if not os.path.isfile(res_fname):
                    cmd = "python2 cog_simulations/steels/steels_main.py -s {0} -r {1}".format(sim_fname, res_fname)
                    f = ex.submit(os.system, cmd)
                    future_to_desc[f] = sim_fname
                else:
                    print(res_fname + ' already exists, skipping.')

        n_completed = 0
        for f in cf.as_completed(future_to_desc):
            n_completed += 1
            print("Completed {} ({}/{})".format(future_to_desc[f], n_completed, len(future_to_desc)))

    print("Simulations done.")


def merge_results(res_base_dir, results_file):
    print("Results file: " + results_file)
    if os.path.exists(results_file):
        print("Results file %s exists, exiting!" % results_file)
        return

    RESULTS_PARTS = [
        os.path.join(res_base_dir, fn)
        for fn in os.listdir(res_base_dir)
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
    res.to_csv(results_file)

    print("Stats done.")


def run_sim(name):
    sim_base_dir = 'examples/simulations/%s' % name
    res_base_dir = 'results_of_simulation/%s' % name
    results_file = '%s_results_vi.csv' % name
    run_simulations(sim_base_dir, res_base_dir, N_SIM, N_PROC)
    merge_results(res_base_dir, results_file)


if __name__ == "__main__":
    run_sim('ext_env_shift')
    run_sim('ext_top_shift')
