import json
import os
import re
import logging


SIZES = [8, 12, 24, 32, 48]  # No 16!
DUMP_PER_8_NODES = 25
ITERS_PER_8_NODES = DUMP_PER_8_NODES * 200


logging.basicConfig(level=logging.INFO)


def main(base_dir, out_dir):
    base_sim_files = [
        (name, path) for name, path in
        ((name, os.path.join(base_dir, name)) for name in os.listdir(base_dir))
        if os.path.isfile(path) and re.match(r'^simulation_\w+\.json$', name)
    ]
    logging.info("Found %d base sim files.", len(base_sim_files))
    process(base_sim_files, out_dir)


def mk_source(source, n):
    measure = re.match(r'^\.\./\.\./networks/graph_(\w+)\.json$', source).group(1)
    # fn = '../../../networks/N{:03d}d03_{}weenness_best01.cogabm.json'.format(n, measure)
    fn = '../../networks/N{:03d}d03_{}weenness_best01.cogabm.json'.format(n, measure)
    return unicode(fn)


def process(base_sim_files, out_dir):
    for name, in_path in base_sim_files:
        logging.info("Processing file %s", in_path)
        for size in SIZES:
            with open(in_path)as f_in:
                sim = json.load(f_in)  # restore state
            sim['num_agents'] = size
            epoch_size = (size // 8) * ITERS_PER_8_NODES
            sim['num_iter'] = epoch_size * 2
            sim['dump_freq'] = (size // 8) * DUMP_PER_8_NODES
            if 'interactions_sets' in sim:
                for _, lst in sim['interactions_sets'].items():
                    for elem in lst:
                        if elem['network']['type'] == "Source":
                            elem['network']['source'] = mk_source(elem['network']['source'], size)
                sim['interactions_sets'][str(epoch_size)] = sim['interactions_sets']['10000']
                del sim['interactions_sets']['10000']
            network = re.match(r'simulation_(\w+)\.json', name).group(1)
            out_name = 'simulation_N{:02d}_{}.json'.format(size, network)
            out_path = os.path.join(out_dir, out_name)
            logging.info("Writing file %s", out_path)
            with open(out_path, 'w') as out_f:
                json.dump(sim, out_f, indent=4)


if __name__ == "__main__":
    main('ext_top_shift/base_sims', 'ext_top_shift')
    main('ext_env_shift/base_sims', 'ext_env_shift')
