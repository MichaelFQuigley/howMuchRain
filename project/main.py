import argparse
import sys
from dataModel import *
import simplePerceptron
import tests
import msvcrt as m
from datamodelUtil import *
from sklearn.cross_validation import KFold
from sklearn import svm
from evaluateSVM import *
from argParseWrapper import *

def wait():
    m.getch()
        
if __name__ == "__main__":
    args = parseArgs()

    trainMax, testMax = 0, 0


    print 'finding max for test data'

    #testHeaders =   getHeaders(args.test)
    print 'processing training data'
    
    x, y = processData(args.train, False)
    print 'There is ' + str(len (x)) + ' examples'
    
    #validateLinearSvm(x,y)
    #validatePolySvm(x,y)
    validateRBFSvm(x,y)
    print 'done'
                
