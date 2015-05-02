#linearRegressionTest.py
from linearRegression import *
from datamodelUtil import *
import mistakeMetric

devFilename = 'train_2013.csv'

maxDim_num = 18

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

    
inputFile = open(devFilename, 'r')
#needs to match current number of columns in examples
#sanitizeWeatherDataExample may change current dim num, so if you add dims, then make sure you update this value
currDim_num = maxDim_num - len(omitCols) + 1
print currDim_num
linReg = linearRegressor()
i = 0

mistakeCount = 0.0
#iterates up to this number of examples
totalElements = 800000

for ex in processDataGenerate(inputFile, False):
    example = sanitizeWeatherDataExample(ex)
    if i >= totalElements:
        prediction = linReg.predictOnExample(example)
        if mistakeMetric.difference(prediction, example.expected, 1.0):
            mistakeCount += 1
        if i % 10000 == 0:
            print "id: " + str(example.id) + " prediction: " + str(prediction) + " expected: " + str(example.expected) + " timesRR: " + str(example.columns['TimeToEndTimesRR1'])
    else:
        linReg.trainOnExample(example)
    i += 1
print "accuracy = " + str(1.0 - float(mistakeCount) / float(i - totalElements))
