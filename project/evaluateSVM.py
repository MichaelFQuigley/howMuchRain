'''
Created on May 3, 2015

@author: Ziggy
'''
from sklearn import svm
from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn.metrics import classification_report
from datamodelUtil import crossValidate

def validateLinearSvm(x, y):
    xTrain, xTest, yTrain, yTest = train_test_split(x, y)
    params = {'kernel': ['linear'], 'C': [1e0, 1e1, 1e2, 1e3, 1e4, 1e5]}
    print 'validating linear svm'
    svc = svm.SVC(class_weight='auto')
    crossValidate(svc, params, xTrain, xTest, yTrain, yTest)
    
    
def validatePolySvm(x, y): 
    xTrain, xTest, yTrain, yTest = train_test_split(x, y)

    params = {'kernel': ['poly'],
                  'C': [1e0, 1e1, 1e2, 1e3],
                  'degree': [2, 3, 4],
                  'coef0': [1e0, 1e1, 1e2],
                  'gamma': [1e-3, 1e-2, 1e-1]}
    print 'validating poly svm'
    svc = svm.SVC(class_weight='auto')
    crossValidate(svc, params, xTrain, xTest, yTrain, yTest)
    
def validateRBFSvm(x, y): 
    xTrain, xTest, yTrain, yTest = train_test_split(x, y)
    params = {'kernel': ['rbf'],
              'C': [1e0, 1e1, 1e2, 1e3, 1e4, 1e5],
              'gamma': [1e-4, 1e-3, 1e-2, 1e-1]}
    
    print 'validating RBF svm'
    svc = svm.SVC(class_weight='auto')
    crossValidate(svc, params, xTrain, xTest, yTrain, yTest)
