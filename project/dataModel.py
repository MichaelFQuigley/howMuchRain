'''
Created on Mar 22, 2015

@author: Zach
'''
import csv
import sys
import itertools
import math


#names for column indexes
class ColInd:
	Id                = 0
	TimeToEnd         = 1
	DistanceToRadar   = 2
	Composite         = 3
	HybridScan        = 4
	HydrometeorType   = 5
	Kdp               = 6
	RR1               = 7
	RR2               = 8
	RR3               = 9
	RadarQualityIndex = 10
	Reflectivity      = 11
	ReflectivityQC    = 12
	RhoHV             = 13
	Velocity          = 14
	Zdr               = 15
	LogWaterVolume    = 16
	MassWeightedMean  = 17
	MassWeightedSD    = 18
	Expected          = 19

	
	
	
def makeDevData(inputfile, amount):
    reader = csv.reader(inputfile, delimiter=',')
    headers = reader.next()
    f = open('devData.csv', 'wb')    
    try:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        count = 0
        for i, row in enumerate(reader):
            writer.writerow(row)
            count += 1
            
            if count > amount:
                break
    finally:
        f.close()

	

def findMaxColumnDim(index, inputFile):
    reader   = csv.reader(inputFile, delimiter=',')
    maxValue = 0
    headers  = reader.next()

    for i, row in enumerate(reader):
        rowId =  int(row[ColInd.Id])
        
        if rowId % 1000 == 0:
            print "Finding max column dimension for row: " + str(rowId)
        
        firstColumn = row[index].split(' ')
        maxValue = max(maxValue, len(firstColumn))
    
    inputFile.close()
    
    return headers, maxValue
	

def processDataGenerate(inputFile, isTest):
    inputFile = open(inputFile.name, 'r')
    reader = csv.reader(inputFile, delimiter=',')
    headers = reader.next()

    for i, row in enumerate(reader):
        rowId =  row[ColInd.Id]
        
        if int(rowId) % 1000 == 0:
            print "processing data row: " + rowId
        
        data = WeatherData(headers, row, isTest)

        yield data
        
    inputFile.close()
    
class WeatherData(object):
    
    def __init__(self, headers, row, isTest=False):
        
        self.id = int( row.pop(ColInd.Id) )
        if isTest:
            self.expected = None
            headers = headers[1 : len(headers)] # get rid of id header and expected
        else:
            self.expected = float (row[len(row) - 1])
            headers = headers[1 : len(headers) - 1] # get rid of id header and expected
        
        self.columns = {}
        
        for header, column in itertools.izip(headers, row):
            self.columns[header] = column.split(' ')
        
        #convert strings to floats
        for key, value in self.columns.iteritems():
            self.columns[key] = map(float, value)
        
        self.dealWithMissingData()
    
    
    
    def getSortedColsArr(self):
        listIndex    = 1
        resultArr    = []
        sortedTupArr = sorted(self.columns.items())
        for element in sortedTupArr:
            resultArr.extend(element[listIndex])
        return resultArr
	
    
    
    def dealWithMissingData(self):
        for value in self.columns.itervalues():
            for index, item in enumerate(value):
                if item == -99900.0:
                    value[index] = 0
                elif item == -99901.0:
                    value[index] = 0
                elif item == -99903.0:
                    value[index] = 0
                elif math.isnan(item):
                    value[index] = 0
                elif item == -999.0:
                    value[index] = 0
    