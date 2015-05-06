#datamodelUtil

#cols is a string array of column names to remove
#returns new data  with removed cols
#data is dictionary of data

from dataModel import *
from math import *
from sklearn.cross_validation import train_test_split, StratifiedKFold
import numpy as np
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split

def removeColsFromData(data, cols):
    if data != None:
        for col_name in cols:
            data.pop(col_name, None)
        return data
        
#takes array produced by column and returns median
def medianOfCol(col):
    if len(col) == 0:
        return None
    elif len(col) % 2 == 0:
        return (col[len(col)//2 - 1] + col[len(col)//2]) / 2
    else:
        return col[len(col)//2]

def meanOfCol(col):
    if len(col) == 0:
        return None
    return float(sum(col)) / float(len(col))
    
#returns array in format [colA0 * colB0, ..., colAn*colBn]
#if arrays are not same size, then processing will stop after shortest array completes
def productOfCols(colA, colB):
    minLength = min(len(colA), len(colB))
    return [colA[i] * colB[i] for i in range(minLength)]

def flatten(dictionary):
    
    flattenList = []
    for key in dictionary:
        flattenList.append(dictionary[key])
        
    return flattenList


def processData(csvFile, isTest, headers = None, hasZeros = True):

    allData = []
    y = []
    medians = None
    
    zeroCount = 0
    
    for row in processDataGenerate(csvFile, isTest, headers):
        
        if not hasZeros and row.expected == 0: continue

        
        if medians == None:
            medians = [0] * len(row.listOfData[0])
        
        tempY = int(row.expected * 10)
        
        if tempY >= 256: continue
        
        for data in row.listOfData:
            flattenedList = flatten(data)
            allData.append(flattenedList)
            y.append(tempY)
            
            zeroCount += 1 if row.expected == 0 else 0
            
            medians = [ m if f is None else f + m for f,m in zip(flattenedList, medians)]
        
        if len(allData) >= 25000: break
                
    print "number of zeros\n", zeroCount
        
    medians = [ m / float(len (medians)) for m in medians]
    
    for data in allData:
        for i in xrange(len(data)):
            if data[i] == None:
                data[i] = medians[i]
    
    return train_test_split(np.array(allData), np.array(y))

    
#postProcLambda is a lambda that is called on the WeatherDataObject to do any post processing
#example: obj = postProcLambda(obj)
def processData2(csvFile, isTest, headers = None, postProcLambda = None):
    allData = []
    y       = []
    ids     = []
    medians = None
    for row in processDataGenerate(csvFile, isTest, headers):

        if postProcLambda != None:
            row = postProcLambda(row)
 
        if medians == None:
            medians = [0] * len(row.listOfData[0])
        '''    
        if row.expected < 0.5:
            tempY = 0.0
        elif row.expected < 1.0:
            tempY = 0.5
        elif row.expected < 1.5:
            tempY = 1
        else:
            tempY = 1.5'''
        if row.expected != None:
            tempY = (row.expected // 0.3) * 3
        else:
            tempY = 0
        #tempY = True if row.expected > 0.0  else False
        for data in row.listOfData:
            flattenedList = flatten(data)
            allData.append(flattenedList)
            y.append(tempY)
            medians = [ m if f is None 
                        else f + m 
                        for f,m in zip(flattenedList, medians)]
                
    medians = [ m / float(len (medians)) for m in medians]
    
    for data in allData:
        for i in xrange(min(len(data), len(medians))):
            if data[i] == None:
                data[i] = medians[i]
    dataType = 'int'
    return np.asarray(allData, dtype = 'float'), np.asarray(y, dtype = dataType), np.asarray(ids, dtype = dataType)

    
    
def logOfCol(colA):
    return [(log(colA[i] + 0.00001)
              if colA[i] >= 0 else log(-colA[i])) 
                  for i in range(len(colA))]
            
            
def crossValidate(algo, params, xTrain, xTest, yTrain, yTest, folds = 10):
    assert folds > 2, 'number of folds must be greater than 2'
    
    tenFold = StratifiedKFold(yTrain, n_folds = folds)
    gridSearch = GridSearchCV(algo, params, n_jobs= 4, cv=tenFold)
    gridSearch.fit(xTrain, yTrain)

    print "Best Params:", gridSearch.best_params_
    print "Best Score:", gridSearch.best_score_
    
    predictions = gridSearch.predict(xTest)
    print predictions
    accuracy = len(np.where(predictions == yTest)[0]) / float(len(predictions))
    print "Accuracy:", accuracy
    print classification_report(yTest, predictions)    

def crossValidateContinuous(algo, params, xTrain, xTest, yTrain, yTest, folds = 10):
    assert folds > 2, 'number of folds must be greater than 2'
    
    tenFold = StratifiedKFold(yTrain, n_folds = folds)
    gridSearch = GridSearchCV(algo, params, n_jobs= 4, cv=tenFold)
    gridSearch.fit(xTrain, yTrain)

    print "Best Params:", gridSearch.best_params_
    print "Best Score:", gridSearch.best_score_
    
    predictions = gridSearch.predict(xTest)
    print predictions
    accuracy = len(np.where(abs(predictions - yTest) >= 0.5)[0]) / float(len(predictions))
    print "Accuracy:", accuracy
    #print classification_report(yTest, predictions)   
