import numpy as np
from scipy.spatial import distance
import json

STIMULI_NUM = 600
STIM = (1,1,1)
COV = np.array([[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]])
STIMULI_FILE = '1269_munsell_chips.json'
DISTANCE = 50


def LAB_dist(stim_1, stim_2):
    return distance.euclidean(stim_1, stim_2)+11


def gauss_divide(output_name, stim=STIM, stimuli_num=STIMULI_NUM, stimuli_file=STIMULI_FILE, cov=COV):
    with open(stimuli_file, 'r') as g:
        stimuli = json.load(g)
    chips = [i.values() for i in stimuli['stimuli']]
    dists = distance.pdist(chips, metric='euclidean')
    # print np.max(dists)
    # min=100
    # for i in dists:
    #     if (i != 0 & i < min):
    #         min = i
    #
    # print i



    for i in xrange(stimuli_num):
        x = np.random.multivariate_normal(stim, cov)

       # distances = distance.cdist([x], chips)



       # random_chips.append(chips[distances.argmin()])

        if LAB_dist(stim, x) > 50:
            i -= 1
        else:
            chips.append({"a": x[0], "L": x[1], "b": x[2]})
    with open(output_name+".json", 'w') as f:
        json.dump({"stimuli": chips, "type": "CIELab"}, f)

