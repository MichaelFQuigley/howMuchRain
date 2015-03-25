import argparse
import sys
from dataModel import *
import simplePerceptron

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
    trainMax =  findMaxColumnDim(ColInd.TimeToEnd, args.train)

    print 'finding max for test data'
    testMax =  findMaxColumnDim(ColInd.TimeToEnd, args.test)
    
    print 'processing training data'

    maxPad = max(testMax, trainMax)

    i = 0
    classifier = simplePerceptron.perceptron(.5, 5)
    for row in processDataGenerate(args.test, False, maxPad):
        classifier.trainOnExample(row.getSortedColsArr(), row.expected)
        
    for row in processDataGenerate(args.test, False, maxPad):
        if i % 1000 == 0:
            print classifier.getPredictionFromVec(row.getSortedColsArr())
        i += 1


