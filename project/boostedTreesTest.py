#SKLinearRegression
#Currently: Support Vector Regression
#Author: Michael
import numpy as np
from argParseWrapper import *
from datamodelUtil import *
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from submissionCreator import submissionCreator
import mistakeMetric

omitCols = ['ReflectivityQC', 'HybridScan', 'Velocity', 'Reflectivity', 'Composite']
omitCols.extend([ 'HydrometeorType', 'DistanceToRadar', 'Zdr', 'RhoHV', 'Kdp'])

def sanitizeWeatherDataExample2(example):
    example.removeListOfDataCols(['HydrometeorType',  'Kdp', 'Composite'])
    multiplyLambda = lambda x, y: x * y
    example.addListOfDataCol('TimeToEndTimesRR1',example.operationOnCols(multiplyLambda, 'TimeToEnd', 'RR1'))
    example.addListOfDataCol('TimeToEndTimesRR2',example.operationOnCols(multiplyLambda, 'TimeToEnd', 'RR2'))
    #example.addListOfDataCol('TimeToEndTimesRR3',example.operationOnCols(multiplyLambda, 'TimeToEnd', 'RR3'))
    return example
    
def validateBoostedTree(x, y):
    xTrain, xTest, yTrain, yTest = train_test_split(x, y)
    boostParams = {'learning_rate':1.0,
                    'algorithm':"SAMME"}
                    
    boostedTree = AdaBoostClassifier(DecisionTreeClassifier(max_depth=10, criterion='entropy'), **boostParams)
    boostedTree.fit(xTrain, yTrain)
    '''
    for i in range(len(xTest)):
        if i % 50 == 0:
            print 'prediction: ' + str(boostedTree.predict(xTest[i])) + '   label: ' + str(yTest[i]) '''
    predictions = boostedTree.predict(xTest)
    print predictions
    print classification_report(yTest, predictions)    
    mistakeMetric.getAlgoAccuracies(predictions, yTest)
    return boostedTree
            
def createSubmission(classifier, testFile):
    subMission = submissionCreator('treeSubmission.csv')
    try:
            x, y,ids          = processData2(testFile, False, postProcLambda = lambda x : sanitizeWeatherDataExample2(x))
            i = 0
            for ex in x:
                prediction = float(classifier.predict(ex)) * 0.1
                subMission.addRow(ids[i], prediction)
                i += 1
    finally:
        subMission.close()
    
#boostedTrees test
if __name__ == "__main__":  
    parsedArgs  = parseArgs()
    trainFile      = parsedArgs.train 
    testFile        = parsedArgs.test
    x, y, ids            = processData2(trainFile, False, postProcLambda = lambda x : sanitizeWeatherDataExample2(x))
    boostedTree = validateBoostedTree(x, y)
    if testFile != None:
        createSubmission(boostedTree, testFile)