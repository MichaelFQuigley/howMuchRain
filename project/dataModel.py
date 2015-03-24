'''
Created on Mar 22, 2015

@author: Zach
'''
import csv
import sys
import itertools
import math
    
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

def findMaxRadar(inputFile):
    reader = csv.reader(inputFile, delimiter=',')
    
    maxValue = -1 * sys.maxint
    headers = reader.next()
        
    for i, row in enumerate(reader):
        rowId =  int(row.pop(0))
        
        if rowId % 1000 == 0:
            print "Finding max row: " + str(rowId)
        
        firstColumn = row[0].split(' ')
        maxValue = max(maxValue, len(firstColumn))
    
    inputFile.close()
    
    return maxValue

def processData(inputFile, isTest, padAmount):
    inputFile = open(inputFile.name, 'r')
    reader = csv.reader(inputFile, delimiter=',')
    headers = reader.next()

    for i, row in enumerate(reader):
        rowId =  row[0]
        
        if int(rowId) % 1000 == 0:
            print "processing data row: " + rowId
        
        data = WeatherData(headers, row, isTest)
        data.padColumns(padAmount)
        
    inputFile.close()
class WeatherData(object):
    
    def __init__(self, headers, row, isTest=False):
        
        self.id = int( row.pop(0) )
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
    
    
    def dealWithMissingData(self):
        for value in self.columns.itervalues():
            for index, item in enumerate(value):
                if item == -99000.0:
                    value[index] = 0
                elif item == -99901.0:
                    value[index] = 0
                elif item == -99903.0:
                    value[index] = 0
                elif math.isnan(item):
                    value[index] = 0
                elif item == -999.0:
                    value[index] = 0
    
    def padColumns(self, maxLength):
        for key, value  in self.columns.iteritems():
            padded = [0] * (maxLength - len(value))
            self.columns[key] = value + padded
