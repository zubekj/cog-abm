import numpy as np
from scipy.spatial import distance
import json

STIMULI_NUM = 600
STIM = (1,1,1)
COV = np.array([[2, 1, 2],
                [1, 5, 4],
                [2, 4, 3]])
STIMULI_FILE = '1269_munsell_chips.json'
DISTANCE = 50


def LAB_dist(stim_1, stim_2):
    return distance.euclidean(stim_1, stim_2)+11


def gauss_divide(output_name, stim=STIM, stimuli_num=STIMULI_NUM, cov=COV, stimuli_file=STIMULI_FILE, distance=DISTANCE):
    gauss = ""
    list = []
    stimuli = []
    g = open(stimuli_file, 'r')
    stimuli = json.load(g)
    for i in stimuli['stimuli']:
        list = list+[i.values()]
    g.close()

    for i in range(stimuli_num):
        x = np.random.multivariate_normal(stim, cov)
        if LAB_dist(stim, x) > distance:
            i -= 1
        else:
            list.append({"a": x[0], "L": x[1], "b": x[2]})

    f = open(output_name+".json", 'w')
    json.dump({"stimuli": list, "type": "CIELab"}, f)

    f.close()
