import json
import os
import re
import logging


BASE_DIR = 'base_sims'
OUT_DIR = '.'
SIZES = [8, 12, 24, 32]  # No 16!


logging.basicConfig(level=logging.INFO)

base_sim_files = [
    (name, path) for name, path in
    ((name, os.path.join(BASE_DIR, name)) for name in os.listdir(BASE_DIR))
    if os.path.isfile(path) and re.match(r'^simulation_\w+\.json$', name)
]

logging.info("Found %d base sim files.", len(base_sim_files))


def mk_source(source, n):
    measure = re.match(r'^\.\./\.\./networks/graph_(\w+)\.json$', source).group(1)
    fn = '../../../networks/N{:03d}d03_{}weenness_best01.cogabm.json'.format(n, measure)
    return unicode(fn)


def main():
    for name, in_path in base_sim_files:
        logging.info("Processing file %s", in_path)
        for size in SIZES:
            size_dir = os.path.join(OUT_DIR, 'N{:02d}'.format(size))
            if not os.path.exists(size_dir):
                os.mkdir(size_dir)
            with open(in_path)as f_in:
                sim = json.load(f_in)  # restore state
            sim['num_agents'] = size
            for _, lst in sim['interactions_sets'].items():
                for elem in lst:
                    if elem['network']['type'] == "Source":
                        elem['network']['source'] = mk_source(elem['network']['source'], size)
                    elem['environment']['source'] = u'../' + elem['environment']['source']
            out_name = name
            out_path = os.path.join(size_dir, out_name)
            logging.info("Writing file %s", out_path)
            with open(out_path, 'w') as out_f:
                json.dump(sim, out_f, indent=4)


if __name__ == "__main__":
    main()
