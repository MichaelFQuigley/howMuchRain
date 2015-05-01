#linearRegression classifier
#author Michael Quigley
from dataModel import *
from math import *

#right now, assumes that each value for a column is a one element list
class linearRegressor:
    def __init__(self, dim_num):
        self.dim_num = dim_num
        self.w = [0.0] * dim_num
        self.learnRate = 0.005
        self.t = 0.0
        self.C = 2.0
        
    def predictOnExample(self, example):
        sortedExampleCols = example.getSortedColsArr()
        return sum([self.w[i] * sortedExampleCols[i] for i in range(self.dim_num)])
        
    #expects WeatherData object
    def trainOnExample(self, example):
        prediction = self.predictOnExample(example)
        sortedExampleCols = example.getSortedColsArr()
        self.w = [(self.w[j] - self.learnRate * (prediction - example.expected) * sortedExampleCols[j]) for j in range(self.dim_num)]
        self.learnRate /= (1.0 + self.learnRate * float(self.t) / self.C)
        self.t += 1.0