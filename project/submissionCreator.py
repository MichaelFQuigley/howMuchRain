#submissionCreator
from math import exp
import csv

class submissionCreator:
    def __init__(self, filename):
        self.col_num = 70
        self.outFile = open(filename, 'w')
        self.writer = csv.writer(self.outFile, delimiter=',')
        solution_header = ['Id']
        solution_header.extend(['Predicted{0}'.format(t) for t in xrange(0, 70)])
        self.writer.writerow(solution_header)
    
    def sigmoidArr(self, center, length):
        return [1. / (1 + exp(-(i - center))) for i in range(length)]

    def addRow(self, id, prediction):
        sigArr = self.sigmoidArr(prediction, self.col_num)
        row = [id]
        row.extend(sigArr)
        self.writer.writerow(row)
        
    def close(self):
        self.outFile.close()
        
        