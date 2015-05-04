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

def wait():
    m.getch()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--train', type=argparse.FileType('r'),
                        help=("path to an input file, this will "
                              "typically be train_2013.csv or "
                              "test_2014.csv"))
    parser.add_argument('--test', type=argparse.FileType('r'),
                        help=("path to an input file, this will "
                              "typically be train_2013.csv or "
                              "test_2014.csv"))
    
    parser.add_argument('--output', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help=("path to an output file, "
                          "defaults to stdout"))
    
    args = parser.parse_args()

    trainMax, testMax = 0, 0


    print 'finding max for test data'

    #testHeaders =   getHeaders(args.test)
    print 'processing training data'
    
    x, y = processData(args.train, False)
    print 'There is ' + str(len (x)) + ' examples'
    
    validateLinearSvm(x,y)
    validatePolySvm(x,y)
    validateRBFSvm(x,y)
    print 'done'
                
