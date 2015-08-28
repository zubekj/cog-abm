import os
import json
import numpy as np
import time
from itertools import imap

repetition = 5

for j in xrange(0, 100):
    alpha = float(j) / 100
    for i in xrange(repetition):
        os.system("python run.py "
                  "-c ../examples/class_KNN1_10_test.json "
                  "-t ../examples/task_glass_test.json "
                  "-o ../results_of_simulation/KNN1_10_glass_test_%s_%s "
                  "-a %s" % (alpha, i, alpha))
    time.sleep(1)
    print "alpha %s done" % alpha

statistics_labels = ["category_minimum",
                     "category_maximum",
                     "category_avenge",
                     "agent_avenge_sample",
                     "avenge_sample_number",
                     "accuracy"]

statistics = {"alpha": []}
for label in statistics_labels:
    statistics[label] = []

for j in xrange(0, 100):
    alpha = float(j) / 100
    statistics['alpha'].append(alpha)
    tmp_statistics = {}

    for label in statistics_labels:
        tmp_statistics[label] = []

    for i in xrange(repetition):
        with open("../results_of_simulation/KNN1_10_glass_test_%s_%s" % (alpha, i), 'r') as f:
            file_stats = json.loads(f.read())
            for label in statistics_labels:
                tmp_statistics[label].append(file_stats[label])

    for label in statistics_labels:
        statistics[label].append(np.mean(tmp_statistics[label]))

with open("../results_of_simulation/KNN1_10_glass_alpha_compare", 'w') as f:
    f.write("alpha\t")
    f.write("\t".join(imap(str, statistics['alpha'])))
    f.write("\n")

    for label in statistics_labels:
        f.write(label + "\t")
        f.write("\t".join(imap(str, statistics[label])))
        f.write("\n")
