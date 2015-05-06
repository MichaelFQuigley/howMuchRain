#mistake metrics
#used to measure accuracy on train set
#they return true if a mistake was made given the following metric
from math import *

def difference(prediction, label, delta):
    return abs(prediction - label) >= delta
    
#mistake if one is zero, other is nonzero  
def zeroNonZero(prediction, label):
    return (prediction != 0.0 and label == 0.0) or (prediction == 0.0 and label != 0.0)
    
#uses both metrics
def getAlgoAccuracies(predictions, labels, differenceDelta = 0.5):
    assert len(predictions) == len(labels), 'label and prediction lengths must match'
    zNonZMistakeCount = 0
    diffMistakeCount      = 0
    for i in range(len(predictions)):
        if difference(predictions[i], labels[i], differenceDelta):
            diffMistakeCount += 1
        if zeroNonZero(predictions[i], labels[i]):
            zNonZMistakeCount += 1
    print "accuracy diff = " + str(1.0 - float(diffMistakeCount) / float(len(predictions)))
    print "accuracy Z non Z = " + str(1.0 - float(zNonZMistakeCount) / float(len(predictions)))