#SKLinearRegression
#Currently: Support Vector Regression
#Author: Michael
import numpy as np
from argParseWrapper import *
from datamodelUtil import *
from sklearn.svm import SVR
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from sklearn.metrics import classification_report

omitCols = ['ReflectivityQC', 'HybridScan', 'Velocity', 'Reflectivity', 'Composite']
omitCols.extend([ 'HydrometeorType', 'DistanceToRadar', 'Zdr', 'RhoHV', 'Kdp'])
#does preprocessing on data, expects WeatherData object
def sanitizeWeatherDataExample(example):
    example.removeListOfDataCols(omitCols)
    multiplyLambda = lambda x, y: x * y
    example.addListOfDataCol('TimeToEndTimesRR1',example.operationOnCols(multiplyLambda, 'TimeToEnd', 'RR1'))
    example.addListOfDataCol('TimeToEndTimesRR2',example.operationOnCols(multiplyLambda, 'TimeToEnd', 'RR2'))
    example.addListOfDataCol('TimeToEndTimesRR3',example.operationOnCols(multiplyLambda, 'TimeToEnd', 'RR3'))
    return example
    
def sanitizeWeatherDataExample2(example):
    example.removeListOfDataCols(['HydrometeorType'])
    return example

def validateSVR(x, y):
    xTrain, xTest, yTrain, yTest = train_test_split(x, y)
    params = {'kernel': ['rbf'], 
                'C':1e1,
                'epsilon':  1e-1,
                'degree': 2,
                'shrinking': True}
    svr = SVR(**params)
    #crossValidateContinuous(svr, params, xTrain, xTest, yTrain, yTest, folds = 4)
    for i in range(len(xTest)):
        if i % 100 == 0:
            print 'prediction: ' + str(svr.predict(xTest[i])) + '   label: ' + str(yTest[i]) 

def validateLinReg(x, y):
    xTrain, xTest, yTrain, yTest = train_test_split(x, y)
    params = {'fit_intercept': True,
                    'n_jobs': 4}
    #linReg = linear_model.LinearRegression(**params)
    linReg = linear_model.TheilSenRegressor(random_state=42, **params)
    linReg.fit(xTrain, yTrain)
    
    for i in range(len(xTest)):
        if i % 10000 == 0:
            print 'prediction: ' + str(linReg.predict(xTest[i])) + '   label: ' + str(yTest[i])


    
if __name__ == "__main__":  
    trainFile = parseArgs().train 
    x, y      = processData2(trainFile, False) #postProcLambda = lambda x : sanitizeWeatherDataExample(x))
    validateSVR(x, y)
    #validateLinReg(x, y)
    