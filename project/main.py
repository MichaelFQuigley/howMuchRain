import argparse
import sys
from dataModel import *
import simplePerceptron
import tests
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
    trainHeaders = getHeaders(args.train)

    print 'finding max for test data'
<<<<<<< HEAD
    testHeaders =   getHeaders(args.test)
    
=======
    testHeaders, testMax =  findMaxColumnDim(ColInd.TimeToEnd, args.test)

>>>>>>> c830757188f5de11c54d3a327cd3ee89cd5c49ad
    maxDimension = max(trainMax, testMax)
    print 'processing training data'

    i = 0
    classifier = simplePerceptron.perceptron(.5, 5)
<<<<<<< HEAD
    winnow = Winnow(testHeaders, .05)
    
=======
    winnow = Winnow(maxDimension, testHeaders, .05)

>>>>>>> c830757188f5de11c54d3a327cd3ee89cd5c49ad
    for row in processDataGenerate(args.test, False):
        #classifier.trainOnExample(row.getSortedColsArr(), row.expected)
        winnow.train(row)
        
    for row in processDataGenerate(args.test, False):
<<<<<<< HEAD
        #if i % 1000 == 0:
            #print classifier.getPredictionFromVec(row.getSortedColsArr())
        #i += 1
        print 'predicted: ' + str(winnow.predict(row))
        print 'real: '  + str(row.expected)
        print '\n'
        print raw_input('press enter')
=======
        if i % 1000 == 0:
            print classifier.getPredictionFromVec(row.getSortedColsArr())
        i += 1

>>>>>>> c830757188f5de11c54d3a327cd3ee89cd5c49ad
