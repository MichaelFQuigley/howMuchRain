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

	

def getHeaders(inputFile):
	reader   = csv.reader(inputFile, delimiter=',')
	headers  = reader.next()
	return headers
	
def processDataGenerate(inputFile, isTest, headers = None):
    reader = csv.reader(inputFile, delimiter=',')
    
    if headers is None:
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
		
		
		self.listOfData = [] 
		

		for header, column in itertools.izip(headers, row):
			temp = column.split(' ')
			for i in xrange(len(temp)):
				nextItem = float(temp[i])
				if self.isErrorValue(nextItem):
					nextItem = None
				if len(self.listOfData) <= i:
					self.listOfData.append({header: float(nextItem) })
				else:
					(self.listOfData[i])[header] = nextItem
	
			
	def getSortedColsArr(self):
		listIndex    = 1
		resultArr    = []
		sortedTupArr = sorted(self.columns.items())
		for element in sortedTupArr:
			resultArr.extend(element[listIndex])
		return resultArr
	
	def fixRR3(self):
		for data in self.listOfData:
			
			data['Kdp'] = math.exp( math.log(abs(data['RR3'] / 40.6)) / 0.866)

			if data['RR3'] < 0:
				data['Kdp'] *= -1


	def isErrorValue(self, item):
		
		if item == -99900.0:
			return True
		elif item == -99901.0:
			return True
		elif item == -99903.0:
			return True
		elif math.isnan(item):
			return True
		elif item == -999.0:
			return True
		elif item == 999.0:
			return True
		
		return False