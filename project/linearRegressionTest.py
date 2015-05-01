#linearRegressionTest.py
from linearRegression import *
from datamodelUtil import *

devFilename = 'train_2013.csv'

maxDim_num = 18

omitCols = ['ReflectivityQC', 'HybridScan', 'Velocity', 'Reflectivity', 'Composite']
omitCols.extend(['RadarQualityIndex', 'HydrometeorType', 'DistanceToRadar', 'Zdr', 'RhoHV', 'Kdp'])
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
currDim_num = maxDim_num - len(omitCols) + 1
print currDim_num
linReg = linearRegressor(currDim_num)
i = 0

mistakeCount = 0.0
totalElements = 180000

for ex in processDataGenerate(inputFile, False):
    if i == totalElements:
        break
    i += 1
    example = sanitizeWeatherDataExample(ex)
    linReg.trainOnExample(example)
    prediction = linReg.predictOnExample(example)

    if (prediction != 0.0 and example.expected == 0.0) or (prediction == 0.0 and example.expected != 0.0):
        mistakeCount += 1
    elif prediction != 0.0 and i % 100 == 0:
        print "id: " + str(example.id) + " prediction: " + str(prediction) + " expected: " + str(example.expected) + " timesRR: " + str(example.columns['TimeToEndTimesRR1'])
print "accuracy = " + str(1.0 - float(mistakeCount) / float(totalElements))
