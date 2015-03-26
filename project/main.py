import argparse
import sys
from dataModel import *
import simplePerceptron
from Winnow import Winnow

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

    print 'finding max for training data'
    trainHeaders, trainMax =  findMaxColumnDim(ColInd.TimeToEnd, args.train)

    print 'finding max for test data'
    testHeaders, testMax =  findMaxColumnDim(ColInd.TimeToEnd, args.test)
    
    maxDimension = max(trainMax, testMax)
    print 'processing training data'

    i = 0
    classifier = simplePerceptron.perceptron(.5, 5)
    winnow = Winnow(maxDimension, testHeaders, .05)
    
    for row in processDataGenerate(args.test, False):
        classifier.trainOnExample(row.getSortedColsArr(), row.expected)
        winnow.train(row)
        
    for row in processDataGenerate(args.test, False):
        if i % 1000 == 0:
            print classifier.getPredictionFromVec(row.getSortedColsArr())
        i += 1


