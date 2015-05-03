#linearRegressionTest.py
from linearRegression import *
from datamodelUtil import *
import mistakeMetric

devFilename = 'train_2013.csv'

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
    newExampleCols = removeColsFromData(example.columns, ['Kdp', 'HydrometeorType', 'DistanceToRadar'])
    newExampleCols = {col : [medianOfCol(example.columns[col])] for col in example.columns}
    
    #newExampleCols['Kdp'] = [(0.0 if newExampleCols['RR3'][0] < 0.1 else (log(newExampleCols['RR3'][0] / 40.6)/0.866))]
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
    
inputFile = open(devFilename, 'r')
linReg = linearRegressor()
i = 0

mistakeCount = 0.0
#iterates up to this number of examples
totalElements = 10000

for ex in processDataGenerate(inputFile, False):
    example = sanitizeWeatherDataExampleSquared(ex)
    prediction = linReg.predictOnExample(example)
    if i >= totalElements:
        if mistakeMetric.difference(prediction, example.expected, 1.0):
            mistakeCount += 1
    else:
        linReg.trainOnExample(example)
    if i % 1000 == 0:
        print "id: " + str(example.id) + " prediction: " + str(prediction) + " expected: " + str(example.expected)# + " timesRR: " + str(example.columns['TimeToEndTimesRR1'])
  
    i += 1
print "accuracy = " + str(1.0 - float(mistakeCount) / float(i - totalElements))
