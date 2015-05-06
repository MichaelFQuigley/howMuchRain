'''
Created on May 3, 2015

@author: Ziggy
'''
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn import svm
from sklearn.grid_search import GridSearchCV
import numpy as np
from sklearn.metrics import classification_report

def validateLinearSvm(xTrain, xTest, yTrain, yTest):
     
    params = {'kernel': ['linear'], 'C': [1e0, 1e1, 1e2, 1e3, 1e4, 1e5]}
    print 'validating linear svm'
    crossValidateSVM(params, xTrain, xTest, yTrain, yTest)
    
    
def validatePolySvm(xTrain, xTest, yTrain, yTest): 

    params = {'kernel': ['poly'],
                  'C': [1e0, 1e1, 1e2, 1e3],
                  'degree': [2, 3, 4],
                  'coef0': [1e0, 1e1, 1e2],
                  'gamma': [1e-3, 1e-2, 1e-1]}
    print 'validating poly svm'
    
    crossValidateSVM(params, xTrain, xTest, yTrain, yTest)
    
def validateRBFSvm(xTrain, xTest, yTrain, yTest, c, gamma): 

    params = {'kernel': ['rbf'],
              'C': [c],
              'gamma': [gamma]}
    
    print 'validating RBF svm'
    
    return crossValidateSVM(params, xTrain, xTest, yTrain, yTest)


def crossValidateSVM(params, xTrain, xTest, yTrain, yTest):
    
    tenFold = StratifiedKFold(yTrain, n_folds =10)
    svc = svm.SVC(class_weight='auto')
    
    gridSearch = GridSearchCV(svc, params, n_jobs= 4, cv=tenFold)
    gridSearch.fit(xTrain, yTrain)

    print "Best Params:", gridSearch.best_params_
    print "Best Score:", gridSearch.best_score_
    
    predictions = gridSearch.predict(xTest)
    accuracy = len(np.where(predictions == yTest)[0]) / float(len(predictions))
    print "Accuracy:", accuracy
    print classification_report(yTest, predictions)
    
    return predictions    

