import numpy as np
from scipy.spatial import distance
import json

STIMULI_NUM = 600
STIM = (1,1,1)
SD = 2
STIMULI_FILE = '1269_munsell_chips.json'
DISTANCE = 50


def LAB_dist(stim_1, stim_2):
    return distance.euclidean(stim_1, stim_2)


def gaussian_divide(output_name, stim=STIM, stimuli_num=STIMULI_NUM, stimuli_file=STIMULI_FILE, distance=DISTANCE):
    gauss_divided = ""
    list = []
    #stimuli = json.loads(read_data)
    for i in stimuli['stimuli']:
        list = list+i.values()
    print list
#        
#    for i in xrange(stimuli_num):
#        x = np.random.multivariate_normal( ....)
#        if x out of borders
#            i = i-1
#        else:
#            gauss_divided = gauss_divided+x
#    
#    
#        

        
    with open(STIMULI_FILE, 'r') as f:
        stimuli = json.loads(f)

