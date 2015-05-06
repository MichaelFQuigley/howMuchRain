import argparse
import sys
from dataModel import *
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
    
    xTrain, xTest, yTrain, yTest =  processData(args.train, False, None, True)
    print 'Training with ' + str(len (xTrain)) + ' examples'
    print 'Testing with '   + str(len(xTest)) + ' examples'
    
    #validateLinearSvm(xTrain, xTest, yTrain, yTest)
    #validatePolySvm(xTrain, xTest, yTrain, yTest)
    params = [(1.0, 0.1), (1.0, 0.1), (1, 0.1), (100, 0.01), (100, 0.01), (1000, 0.01), (1, 0.1), (1, 0.1)]

    bitResults = []
    for i in xrange(0, 8):
        print 'evaluating bit\t', i
        
        c, gamma = params[i]

        yBitTrain = np.array([ (y >> i) % 2 for y in yTrain])
        yBitTest = np.array([ (y >> i) % 2 for y in yTest])
        
        bitResults.append(validateRBFSvm(xTrain, xTest, yBitTrain, yBitTest, c, gamma))
    
    finalResults = []
    messUpResults = []
    
    for i in xrange(0, len(yTest)):
        tmpStr = ''
        for bit in xrange(0, 8):
            tmpStr = str(bitResults[bit][i]) + tmpStr
            
        finalResults.append( tmpStr)
        
    
    print 'finalResults:\n', finalResults

    finalResults = [int(i, 2) for i in finalResults]
    messUpResults = [int(i, 2) for i in messUpResults]
           
    print 'final results\n'
    print classification_report(yTest, finalResults)

    accuracy = len(np.where(finalResults == yTest)[0]) / float(len(finalResults))
    print "Accuracy:", accuracy
    notZeroCount = 0
    for i in xrange(0, len(yTest)):
        if yTest[i] != 0 and yTest[i] == finalResults[i]:
            notZeroCount += 1
            
    print 'there were ', notZeroCount, ' predictions correct that werent 0'



    xTrain, xTest, yTrain, yTest =  processData(args.train, False, None, False)
    print 'Training with ' + str(len (xTrain)) + ' examples'
    print 'Testing with '   + str(len(xTest)) + ' examples'
    
    #validateLinearSvm(xTrain, xTest, yTrain, yTest)
    #validatePolySvm(xTrain, xTest, yTrain, yTest)
    params = [(10.0, 0.01), (100.0, 0.001), (10, 0.001), (10, 0.001), (10, 0.001), (100, 0.01), (100, 0.01), (1, 0.1)]
    bitResults = []
    for i in xrange(0, 8):
        print 'evaluating bit\t', i
        
        c, gamma = params[i]
        yBitTrain = np.array([ (y >> i) % 2 for y in yTrain])
        yBitTest = np.array([ (y >> i) % 2 for y in yTest])
        
        bitResults.append(validateRBFSvm(xTrain, xTest, yBitTrain, yBitTest, c, gamma))
    
    finalResults = []
    messUpResults = []
    
    for i in xrange(0, len(yTest)):
        tmpStr = ''
        for bit in xrange(0, 8):
            tmpStr = str(bitResults[bit][i]) + tmpStr
            
        finalResults.append( tmpStr)
        
    
    print 'finalResults:\n', finalResults

    finalResults = [int(i, 2) for i in finalResults]
           
    print 'final results\n'
    print classification_report(yTest, finalResults)

    accuracy = len(np.where(finalResults == yTest)[0]) / float(len(finalResults))
    print "Accuracy:", accuracy
    notZeroCount = 0
    for i in xrange(0, len(yTest)):
        if yTest[i] != 0 and yTest[i] == finalResults[i]:
            notZeroCount += 1
            
    print 'there were ', notZeroCount, ' predictions correct that werent 0'

    print 'done'
                

    

