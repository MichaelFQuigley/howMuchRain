#datamodelUtil

#cols is a string array of column names to remove
#returns new data  with removed cols
#data is dictionary of data
from dataModel import *
import numpy as np

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

def processData(csvFile, isTest, headers = None):
    allData = []
    y = []
    medians = None
    for row in processDataGenerate(csvFile, isTest, headers):
        
        if medians == None:
            medians = [0] * len(row.listOfData[0])
            
        tempY = -1 if int(row.expected * 10) % 2 == 0  else 1
            
        for data in row.listOfData:
            flattenedList = flatten(data)
            allData.append(flattenedList)
            y.append(tempY)
            medians = [ m if f is None else f + m for f,m in zip(flattenedList, medians)]
                
        
    medians = [ m / float(len (medians)) for m in medians]
    
    for data in allData:
        for i in xrange(len(data)):
            if data[i] == None:
                data[i] = medians[i]
    
    return np.array(allData), np.array(y)