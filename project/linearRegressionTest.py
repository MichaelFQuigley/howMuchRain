#linearRegressionTest.py
from linearRegression import *
from datamodelUtil import *
import mistakeMetric
from submissionCreator import submissionCreator


trainFilename = 'train_2013.csv'
testFilename  = 'test_2014.csv'

omitCols = ['ReflectivityQC', 'HybridScan', 'Velocity', 'Reflectivity', 'Composite']
omitCols.extend([ 'HydrometeorType', 'DistanceToRadar', 'Zdr', 'RhoHV', 'Kdp'])

#does preprocessing on data, expects WeatherData object
def sanitizeWeatherDataExample(example):
    newExampleCols = removeColsFromData(example.columns, omitCols)
    newExampleCols['TimeToEndTimesRR1'] = productOfCols(newExampleCols['TimeToEnd'], [i / 60.0 for i in newExampleCols['RR1']])
    newExampleCols['TimeToEndTimesRR2'] = productOfCols(newExampleCols['TimeToEnd'], [i / 60.0 for i in newExampleCols['RR2']])
    newExampleCols['TimeToEndTimesRR3'] = productOfCols(newExampleCols['TimeToEnd'], [i / 60.0 for i in newExampleCols['RR3']])
    newExampleCols = removeColsFromData(example.columns, ['TimeToEnd', 'RR1'])
    example.columns = newExampleCols
    #just uses median for now
    example.columns = {col : [medianOfCol(example.columns[col])] for col in example.columns}
    example.dealWithMissingData()
    return example

def sanitizeWeatherDataExampleSquared(example):
    newExampleCols = {}
    example.dealWithMissingData()
    newExampleCols = removeColsFromData(example.columns, ['Kdp', 'HydrometeorType',  'DistanceToRadar', 'Zdr'])
    newExampleCols['RR1'] =[i / 60.0 for i in newExampleCols['RR1']]
    newExampleCols['RR2'] =[i / 60.0 for i in newExampleCols['RR2']]
    newExampleCols['RR3'] =[i / 60.0 for i in newExampleCols['RR3']]
    newExampleCols = {col : [medianOfCol(example.columns[col])] for col in example.columns}

    for colI in example.columns:
        for colJ in example.columns:
            if colI == colJ:
                newExampleCols[colI] = example.columns[colI]
            else:
                newExampleCols[colI + colJ] = logOfCol(productOfCols(example.columns[colI], example.columns[colJ]))
    i = 0
    for col in range(len(newExampleCols)):
        if i % 3 == 0:
            newExampleCols.pop(col, None)
        i += 1
    example.columns = newExampleCols
    
    return example
   

def createLinRegSubmission(inputFile, submissionFilename):
    subMission = submissionCreator(submissionFilename)
    for ex in processDataGenerate(inputFile, True):
        example    = sanitizeWeatherDataExample(ex)
        prediction = linReg.predictOnExample(example)
        prediction = prediction if prediction > 0.2 else 0.0
        subMission.addRow(example.id, prediction)

    subMission.close()

   
inputFile = open(trainFilename, 'r')
linReg = linearRegressor()
i = 0

mistakeCountA = 0.0
mistakeCountB = 0.0
#iterates up to this number of examples
totalElements = -1
trainElements = 100000

#training
for ex in processDataGenerate(inputFile, False):
    example = sanitizeWeatherDataExample(ex)
    prediction = linReg.predictOnExample(example)
    prediction = prediction if prediction > 0.2 else 0.0
    if trainElements != -1 and i >= trainElements:
        if mistakeMetric.difference(prediction, example.expected, 0.5):
            mistakeCountA += 1
        if mistakeMetric.zeroNonZero(prediction, example.expected):
            mistakeCountB += 1
    linReg.trainOnExample(example)
    if totalElements != -1 and i >= totalElements:
        break
    if i % 1000 == 0:
        print "id: " + str(example.id) + " prediction: " + str(prediction) + " expected: " + str(example.expected)# + " timesRR: " + str(example.columns['TimeToEndTimesRR1'])
  
    i += 1
    
#testing
#createLinRegSubmission(open(testFilename, 'r'), 'LinSubmissionModified.csv')

print "accuracy diff = " + str(1.0 - float(mistakeCountA) / float(i - trainElements))
print "accuracy Z non Z = " + str(1.0 - float(mistakeCountB) / float(i - trainElements))
