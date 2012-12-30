'''
Module with functions for words storage.

Created on Dec 29, 2012

@author: mlukasik
'''
def extract_colour_order(stimuli, clab_name):
    '''
    Extract colour order from clab_fname and return stimuli in that order (exclude repetitions).
    '''
    chip_map = extract_chip_map(clab_name)
    return get_environment_in_order(stimuli, chip_map)
    
def get_environment_in_order(stimuli, chip_map):
    '''Return sorted list of stimuli from environment in order specified by chip_map.
    '''
    visited = set()
    colour_order_keyed = []
    #traverse all stimuli and add them to the list, excluding repetitions
    for s in stimuli:
        (L, a, b) = tuple(s.get_values())
        if (L, a, b) not in visited:
            visited.add((L, a, b))
            try:
                colour_name = chip_map[(float(L), float(a), float(b))]
            except:
                print "[get_environment_in_order]: ERROR! chip_map: ", chip_map
                import sys
                sys.exit(1)
            colour_order_keyed.append( (s, colour_name) )
    
    #sort by colour_name
    colour_order_keyed.sort(key = lambda x: x[1])
    #return only necessary part
    return map(lambda x: x[0], colour_order_keyed)


def extract_chip_map(fname):
    """
    Read a chipmap from fname, extract information about which ordinal number is
    given to each of the Lab coordinates.
    
    """
    chip_map = {}
    with open(fname) as f:
        #each line is read from a c-lab file
        for l in f:
            ll = l.split()
            #if it is already in a chip_map then there is some repetition!
            if (float(ll[6]), float(ll[7]), float(ll[8])) in chip_map:
                print "[extract_colour_order] ERROR!", (float(ll[6]), float(ll[7]), float(ll[8])), "in chip_map !!!"
                import sys
                sys.exit(1)
            else:#else everything is ok
                chip_map[(float(ll[6]), float(ll[7]), float(ll[8]))] = ll[0]
    return chip_map