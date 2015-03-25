import random
from math import *

class perceptron:

	def __init__(self, r = 0.5, mu = 0):
		self.maxExampleDimension = 0
		self.examples     = []   #list of example types
		self.mistakeCount = 0
		self.initialRandW = (random.random() + 0.1) * 2.0 - 1.0
		self.w            = {} 	#w has format {<index>: <weight>, ...}
		self.r            = r  # learning rate
		self.b            = (random.random() + 0.1) * 2.0 - 1.0
		self.mu           = mu
		self.av           = {}
		
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
			if index != "label":
				sum += self.getAvVecElement(index) * self.getXVecElement(ex, index)
		return sum
			
	def wTx(self, ex):
		sum = 0.0
		for index in ex:
			if index != "label":
				sum += self.getWVecElement(index) * self.getXVecElement(ex, index)
		return sum

	def updateParams(self, ex):
		for index in ex:
			if index != "label":
				self.w[index] = self.getWVecElement(index) + self.r * ex["label"] * ex[index]
				self.av[index] = self.getAvVecElement(index) + self.w[index]
		self.b   = self.b + self.r * ex["label"]

		
	def examplesFromFile(self, filename):
		file = open(filename)
		self.elements = []
		for line in file:
			ex       = {} #format {"label": <label>, ind1: val1, ...}
			elements = line.split()
			ex["label"] = int(elements[0])
			for i in range(1, len(elements)):
				index, value = map(lambda x : int(x),elements[i].split(":"))
				ex[index]    = value
			self.examples.append(ex)
	
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
	

'''
per.examples = [
{"label":-1, 1:1,2:0,3:0,4:0},
{"label":-1, 1:1,2:1,3:0,4:0},
{"label":1, 1:1,2:0,3:1,4:1},
{"label":-1, 1:0,2:1,3:0,4:0},
{"label":-1, 1:0,2:1,3:1,4:0},
{"label":-1, 1:1,2:1,3:1,4:0},
{"label":1, 1:0,2:1,3:1,4:1}
]
'''

def runTest(name, shuffles, mu):
	per = perceptron(0.5, mu)
	
	print "\n" + name + " test."
	
	per.examplesFromFile("adult/a1a.train")
	if shuffles == 0:
		print "One pass."
		per.train()
	else:
		print str(shuffles) + " passes."
		for i in range(shuffles):
			per.train()
			per.shuffleExamples()

	pos = 0
	neg = 0
	for ex in per.examples:
		if ex["label"]*(per.avTx(ex) + per.b) <= 0.0:
			neg += 1
		else:
			pos += 1
	print "Train accuracy: " + str(float(pos) / float(pos + neg))
	print "Train mistake count:" + str(per.mistakeCount)

	per.examplesFromFile("adult/a1a.test")
	per.test()

	pos = 0
	neg = 0
	for ex in per.examples:
		if ex["label"]*(per.avTx(ex) + per.b) <= 0.0:
			neg += 1
		else:
			pos += 1
	print "Test accuracy: " + str(float(pos) / float(pos + neg))
	print "Test mistake count:" + str(per.mistakeCount)
	
runTest("Margin Perceptron (Averaging)", 0, 3.0)
runTest("Simple Perceptron (Averaging)", 0, 0.0)
runTest("Margin Perceptron (Averaging)", 3, 3.0)
runTest("Simple Perceptron (Averaging)", 3, 0.0)
runTest("Margin Perceptron (Averaging)", 5, 3.0)
runTest("Simple Perceptron (Averaging)", 5, 0.0)
#print per.w