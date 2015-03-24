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
    
    print 'processing training data'
    trainData, trainMax = processData(args.train, False)

#    print 'processing test data'
#    testData, testMax = processData(args.test, True)
    
    padMax = max(trainMax, testMax)

    print 'padding train'    
    for data in trainData:
        data.padColumns(padMax)
        
#    print 'padding test'
#     for data in testData:
#         data.padColumns(padMax)

