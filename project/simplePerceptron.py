import random
from math import *

class perceptron:

	def __init__(self, r = 0.5, mu = 0, examples):
		self.examples            = examples   #list of example types
		self.mistakeCount        = 0
		self.initialRandW        = (random.random() + 0.1) * 2.0 - 1.0
		self.w                   = {} 	#w has format {<index>: <weight>, ...}
		self.r                   = r  # learning rate
		self.b                   = (random.random() + 0.1) * 2.0 - 1.0
		self.mu                  = mu
		self.av                  = {}
		
	def getWVecElement(self, index):
		if index in self.w:
			return self.w[index]
		else:
			return self.initialRandW

	def getXVecElement(self, ex, index):
		if index in ex:
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
		for index in ex:
			sum += self.getAvVecElement(index) * self.getXVecElement(ex, index)
		return sum
			
	def wTx(self, ex):
		sum = 0.0
		for index in ex:
			sum += self.getWVecElement(index) * self.getXVecElement(ex, index)
		return sum

	def updateParams(self, ex):
		for index in ex:
			self.w[index] = self.getWVecElement(index) + self.r * ex[index]
			self.av[index] = self.getAvVecElement(index) + self.w[index]
		self.b   = self.b + self.r * ex["label"]

	def train(self):
		for ex in self.examples:
			if ex["label"] * (self.avTx(ex) + self.b) <= self.mu:
				self.updateParams(ex)
				self.mistakeCount += 1
				
	def test(self):
		self.mistakeCount = 0
		for ex in self.examples:
			if ex["label"] * (self.avTx(ex) + self.b) <= 0.0:
				self.mistakeCount += 1

	def shuffleExamples(self):
		for i in range(len(self.examples)):
			temp = self.examples[i].copy()
			randInd = int(random.random() * len(self.examples))
			self.examples[i] = self.examples[randInd].copy()
			self.examples[randInd] = temp 
	
	def getPredictionFromVec(self, ex):
		return (self.avTx(ex) + self.b)

#print per.w