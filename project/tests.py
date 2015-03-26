import sys
from dataModel import *
import simplePerceptron

def testPerceptron(args):
    trainMax, testMax = 0, 0

    print 'finding max for training data'
    trainHeaders, trainMax =  findMaxColumnDim(ColInd.TimeToEnd, args.train)

    print 'finding max for test data'
    testHeaders, testMax =  findMaxColumnDim(ColInd.TimeToEnd, args.test)
    
    maxDimension = max(trainMax, testMax)
    print 'processing training data'

    i = 0
    classifier = simplePerceptron.perceptron(0.0, 5)

    for row in processDataGenerate(args.train, False):
        if i == 100:
            break
        classifier.trainOnExample(row.columns, row.expected)
        i += 1
        
    i = 0
    for row in processDataGenerate(args.train, False):
        if i == 8:
            break
        print classifier.getPredictionFromVec(row.columns)
        i += 1
