import random
from math import *

class perceptron:

    def __init__(self, r = 0.5, mu = 0, updateLambda = None):
        self.mistakeCount        = 0
        self.initialRandW        = (random.random() + 0.1) * 2.0 - 1.0
        self.w                   = {}   #w has format {<columnName>: <list>, ...}
        self.r                   = r  # learning rate
        self.b                   = 1.0
        self.mu                  = mu
        self.av                  = {}   #av has format {<columnName>: <list>, ...}
        
    def updateParams(self, ex, increaseW):
        if increaseW:
            for key in ex:
                updateTerm = [self.r * element for element in ex[key]]
                for i in range(0, len(ex[key])):
                    self.w[key][i] += abs(updateTerm[i])
            self.b = self.b + self.r
        else:
            for key in ex:
                updateTerm = [self.r * element for element in ex[key]]
                for i in range(0, len(ex[key])):
                    self.w[key][i] -= abs(updateTerm[i])
            self.b = self.b - self.r
        if len(self.av) == 0:
            self.av = self.w
            return
        else:
            for key in self.av:
                self.av[key] = [self.w[key][i] + self.av[key][i] for i in range(0, len(self.av[key]))]

    #ex = dictionary
    def trainOnExample(self, ex, expected):
        firstTerm = self.matTransposeX(self.w, ex) + self.b
        if firstTerm > expected:
            self.updateParams(ex, False)
        else:
            self.updateParams(ex, True)
        self.mistakeCount += 1

    def getPredictionFromVec(self, ex):
        return (self.matTransposeX(self.w, ex) + self.b)

    #pads a list (vector) up to 'length' with a given 'value' and return the result 
    def padListIfNeeded(self, vector, length, value):
        result = vector
        if len(result) < length:
            result.extend([value]*(length - len(result)))
        return result
       
    #same as dictionaryDotProduct, except pads left mat if necessary
    #used for a transpose x, and w transpose x
    def matTransposeX(self, mat, ex):
        sum = 0.0
        for key in ex:
            if key not in mat:
                mat[key] = []
            mat[key] = self.padListIfNeeded(mat[key], len(ex[key]), self.initialRandW)
            sum += self.dotProduct(mat[key], ex[key])
        return sum
   
    def dictionaryDotProduct(self, map1, map2):
        sum = 0
        for key in map1.keys():
            sum += self.dotProduct(map1[key], map2[key])
        return sum
       
    def dotProduct(self, x, y):
        return sum([a * b for a, b in zip(x, y)])
           
#print per.w