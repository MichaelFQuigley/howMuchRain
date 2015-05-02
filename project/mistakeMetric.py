#mistake metrics
#used to measure accuracy on train set
#they return true if a mistake was made given the following metric
from math import *

def difference(prediction, label, delta):
    return abs(prediction - label) >= delta
    
#mistake if one is zero, other is nonzero  
def zeroNonZero(prediction, label):
    return (prediction != 0.0 and label == 0.0) or (prediction == 0.0 and label != 0.0)
