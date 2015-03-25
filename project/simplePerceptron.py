import random
from math import *

class perceptron:

    def __init__(self, r = 0.5, mu = 0, examples = []):
        self.examples            = examples   #list of example types
        self.mistakeCount        = 0
        self.initialRandW        = (random.random() + 0.1) * 2.0 - 1.0
        self.w                   = {}   #w has format {<index>: <weight>, ...}
        self.r                   = r  # learning rate
        self.b                   = 1.0
        self.mu                  = mu
        self.av                  = {}
        
    def getWVecElement(self, index):
        if index in self.w:
            return self.w[index]
        else:
            return self.initialRandW

    def getXVecElement(self, ex, index):
        if index in range(0, len(ex)):
            return ex[index]
        else:
            return 0

    def getAvVecElement(self, index):
        if index in self.av:
            return self.av[index]
        else:
            return 0.0

    def avTx(self, ex):
        sum = 0.0
        for index in range(0, len(ex)):
            sum += self.getAvVecElement(index) * self.getXVecElement(ex, index)
        return sum
            
    def wTx(self, ex):
        sum = 0.0
        for index in range(0, len(ex)):
            sum += self.getWVecElement(index) * self.getXVecElement(ex, index)
        return sum

    def updateParams(self, ex, increaseW):
        if increaseW:
            for index in range(0, len(ex)):
                self.w[index] = self.getWVecElement(index) + self.r * ex[index]
                self.av[index] = self.getAvVecElement(index) + self.w[index]
            self.b   = self.b + self.r
        else:
            for index in range(0, len(ex)):
                self.w[index] = self.getWVecElement(index) - self.r * ex[index]
                self.av[index] = self.getAvVecElement(index) + self.w[index]
            self.b   = self.b - self.r

    def train(self):
        for ex in self.examples:
            trainOnExample(ex)

    def trainOnExample(self, ex, expected):
        difference = self.wTx(ex) + self.b - expected
        if abs(difference) > self.mu:
            if difference < 0.0:
                self.updateParams(ex, True)
            else:
                self.updateParams(ex, False)
            self.mistakeCount += 1
                
    def shuffleExamples(self):
        for i in range(len(self.examples)):
            temp = self.examples[i].copy()
            randInd = int(random.random() * len(self.examples))
            self.examples[i] = self.examples[randInd].copy()
            self.examples[randInd] = temp 
    
    def getPredictionFromVec(self, ex):
        return (self.wTx(ex) + self.b)

#print per.w