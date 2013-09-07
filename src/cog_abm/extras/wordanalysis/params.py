'''
Created on Sep 7, 2013

@author: mlukasik
'''
def ellipse(x, y):
    q = (x-10)**2 + ((y-20)/1.3)**2 
    if q >= 7**2 and q <= 9**2:
        return True
    #print "BAD"
    return False

def H(x, y):
    if y == 30 or y == 31 or y == 10 or y == 11: 
        return True
    elif (x == 5 or x == 4) and (y >= 10 or y <= 30):
        return True
    else:
        return False


#This function returns boolean if a given point in 2d should be multiplied or not.
is_to_be_multiplied = ellipse
    