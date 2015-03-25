import argparse
import sys
from dataModel import *

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
    for row in processDataGenerate(args.test, False, maxPad):
        print row.getSortedColsArr()
        print '\n'
        if i == 0:
            break
        i += 1

