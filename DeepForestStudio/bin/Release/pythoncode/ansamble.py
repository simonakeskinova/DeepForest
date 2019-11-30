import os, os.path as osp
import numpy as np

from classificator2 import Classificator
from metrics import calc_accuracy

class Ansamble(object):
    
    def __init__(self, config, classes_count, zero_based_classes): #name, n_folds, classes_count):
        
        self.name = config["Name"]
        self.classifiers_config = config["Classifiers"]
        self.classes_count = classes_count #config["classes_count"]
        self.zero_based_classes = zero_based_classes
        
        self.classifier1d = []
        self.classifiers_count = len(self.classifiers_config)
        
        #self.estimator1 = None
        #self.estimator2 = None
        #self.estimator3 = None
        #self.estimator4 = None
        #self.estimator5 = None
        #self.estimator6 = None
        #self.estimator7 = None
        #self.estimator8 = None
        
    def train(self, X, y, X_val, y_val):
        y_proba = np.zeros((y.shape[0], self.classes_count))
        
        for i in range(self.classifiers_count):
            classifier = Classificator(self.classifiers_config[i], self.classes_count, self.zero_based_classes)
            y_pred = classifier.train(X, y, X_val, y_val)
            self.classifier1d.append(classifier)
            
            calc_accuracy(y, y_pred, self.name, self.classes_count, "train_classifier_{}".format(i), show_matrix=False)
            y_proba += y_pred
            
        """self.estimator1 = Classificator(self.name, self.n_folds, self.classes_count)
        y_proba = self.estimator1.train_RF(X, y, X_val, y_val)
        
        self.estimator2 = Classificator(self.name, self.n_folds, self.classes_count)
        y_proba += self.estimator2.train_RF(X, y, X_val, y_val)
        
        self.estimator3 = Classificator(self.name, self.n_folds, self.classes_count)
        y_proba += self.estimator3.train_ET(X, y, X_val, y_val)
        
        self.estimator4 = Classificator(self.name, self.n_folds, self.classes_count)
        y_proba += self.estimator4.train_ET(X, y, X_val, y_val)
        
        self.estimator5 = Classificator(self.name, self.n_folds, self.classes_count)
        y_proba = self.estimator5.train_RF(X, y, X_val, y_val)
        
        self.estimator6 = Classificator(self.name, self.n_folds, self.classes_count)
        y_proba += self.estimator6.train_RF(X, y, X_val, y_val)
        
        self.estimator7 = Classificator(self.name, self.n_folds, self.classes_count)
        y_proba += self.estimator7.train_ET(X, y, X_val, y_val)
        
        self.estimator8 = Classificator(self.name, self.n_folds, self.classes_count)
        y_proba += self.estimator8.train_ET(X, y, X_val, y_val)"""
        
        y_proba /= self.classifiers_count
        
        return y_proba
        
    def predict_proba(self, X):
        y_proba = np.zeros((X.shape[0], self.classes_count))
        
        for i in range(self.classifiers_count):
            y_proba += self.classifier1d[i].predict_proba(X)
            
        """y_proba = self.estimator1.predict_proba(X)
        y_proba += self.estimator2.predict_proba(X)
        #y_proba += self.estimator3.predict_proba(X)
        #y_proba += self.estimator4.predict_proba(X)
        #y_proba += self.estimator5.predict_proba(X)
        #y_proba += self.estimator6.predict_proba(X)
        #y_proba += self.estimator7.predict_proba(X)
        #y_proba += self.estimator8.predict_proba(X)"""
        
        y_proba /= self.classifiers_count
        return y_proba
        
    def predict(self, X):
        y_proba = self.predict_proba(X)
        y_pred = np.argmax(y_proba, axis=1)
        
        if self.zero_based_classes:
            return y_pred
        else:
            return y_pred + 1