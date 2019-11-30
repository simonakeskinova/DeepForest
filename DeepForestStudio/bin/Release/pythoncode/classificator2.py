import os, os.path as osp
import numpy as np
from sklearn.model_selection import StratifiedKFold

#from metrics import calc_accuracy
from size_utils import find_missing_classes, fill_missing_classes
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

class Classificator(object):
    
    def __init__(self, config, classes_count, zero_based_classes):
        
        #self.name = config["name"]
        self.classifier = config["ClassifierType"] # classifier type 
        self.n_estimators = config["EstimatorsCount"] # number of estimators for classifier
        self.n_folds = config["KFolds"]
        self.classes_count = classes_count
        #self.retrain = config["retrain"]
        self.zero_based_classes = zero_based_classes
        
        self.estimator = None
        self.missing_indexes = None
        self.KFold = True
        
        #self.estimator1d = [None for k in range(self.n_folds)]
        #self.missing_indexes1d = [None for k in range(self.n_folds)]
        
    def get_estimator(self):
        if self.classifier == "RandomForestClassifier":
            #print("RandomForestClassifier")
            return RandomForestClassifier(n_estimators=self.n_estimators, max_depth=None, n_jobs=-1, verbose=False)
        else:
            #print("ExtraTreesClassifier")
            return ExtraTreesClassifier(n_estimators=self.n_estimators, max_depth=None, n_jobs=-1, verbose=False, random_state=0)
        
    def train(self, X, y, X_val, y_val):
        if X_val is None:
            y_proba = self.train_KFold(X, y) # get predicted proba for next level
            self.KFold = True
            
            # train real estimator
            self.estimator = self.get_estimator()               
            self.estimator.fit(X.reshape((-1, X.shape[-1])), y.reshape(-1))
            self.missing_indexes = find_missing_classes(self.classes_count, y)          
        else:
            y_proba = self.train_val(X, y, X_val, y_val)
            self.KFold = False
        
        return y_proba
        
    """def train_RF(self, X, y, X_val, y_val):
        self.classifier = RandomForestClassifier
        #est = RandomForestClassifier(n_estimators=500)
        if X_val is None:
            y_proba = self.train_KFold(X, y)
            self.KFold = True
        else:
            y_proba = self.train_val(X, y, X_val, y_val)
            self.KFold = False
        
        return y_proba

    def train_ET(self, X, y, X_val, y_val):
        self.classifier = ExtraTreesClassifier
        
        if X_val is None:
            y_proba = self.train_KFold(X, y)
        else:
            y_proba = self.train_val(X, y, X_val, y_val)
            self.KFold = False
        
        return y_proba"""
    
    def train_KFold(self, X, y): 
        n_stratify = X.shape[0]
        
        skf = StratifiedKFold(n_splits=self.n_folds, shuffle=True)
        cv = [(t, v) for (t, v) in skf.split(range(n_stratify), y)]
       
        # Fit
        y_probas = [] #np.zeros((y.shape[0], self.classes_count))
        n_dims = X.shape[-1] 
        n_datas = X.size / n_dims 
        
        # fit on k-fold train     
        for k in range(self.n_folds):
            missing_indexes = []

            train_idx, val_idx = cv[k]               
                   
            est = self.get_estimator()            
            est.fit(X[train_idx].reshape((-1, n_dims)), y[train_idx].reshape(-1))
            missing_indexes = find_missing_classes(self.classes_count, y[train_idx])

            # predict on k-fold validation
            y_proba = est.predict_proba(X[val_idx].reshape((-1, n_dims)))
            #calc_accuracy(y[val_idx], y_proba, self.name, self.classes_count, prefix="train_{}".format(k))

            # merging result
            if k == 0:
                y_proba_cv = np.zeros((n_stratify, y_proba.shape[1]), dtype=np.float32)
                
                if len(missing_indexes[0]) > 0:
                    y_proba_cv = fill_missing_classes(y_proba_cv, missing_indexes)  
                                        
                y_probas.append(y_proba_cv)
             
            if len(missing_indexes[0]) > 0: 
                y_proba = fill_missing_classes(y_proba, missing_indexes)     
                
            y_probas[0][val_idx, :] += y_proba
            #if keep_model_in_mem:
            #--self.estimator1d[k] = est

        for y_proba in y_probas[1:]:
            y_proba /= self.n_folds
        # log
        #calc_accuracy(y, y_probas[0], self.name, self.classes_count, "Train classifier ", show_matrix=False)
        
        return y_probas[0]
        
    def train_val(self, X, y, X_val, y_val): 
        n_stratify = X.shape[0]
               
        # Fit
        n_dims = X.shape[-1] 
        n_datas = X.size / n_dims 
        
        self.estimator = self.get_estimator()        
        self.estimator.fit(X.reshape((-1, n_dims)), y.reshape(-1))
        self.missing_indexes = find_missing_classes(self.classes_count, y)
        
        y_proba = self.estimator.predict_proba(X_val.reshape((-1, n_dims)))
        
        if len(self.missing_indexes[0]) > 0: 
            y_proba = fill_missing_classes(y_proba, self.missing_indexes)  
            
        # log
        #calc_accuracy(y_val, y_proba, self.name, self.classes_count, "train_classificator validation set", show_matrix=True)
                
        return y_proba
        
    """def predict_proba_KFold(self, X_test):        
        # K-Fold split
        n_dims = X_test.shape[-1]
        n_datas = X_test.size / n_dims
        
        for k in range(self.n_folds):
            est = self.estimator
            y_proba = est.predict_proba(X_test.reshape((-1, n_dims))) 
            
            if len(self.missing_indexes1d[k][0]) > 0:            
                y_proba = fill_missing_classes(y_proba, self.missing_indexes1d[k]) 
            
            if k == 0:
                y_proba_kfolds = y_proba
            else:
                y_proba_kfolds += y_proba
        y_proba_kfolds /= self.n_folds
        return y_proba_kfolds"""
        
    def predict_proba(self, X_test):
        n_dims = X_test.shape[-1]
        n_datas = X_test.size / n_dims
        
        est = self.estimator
        y_proba = est.predict_proba(X_test.reshape((-1, n_dims))) 
        
        if len(self.missing_indexes[0]) > 0:            
            y_proba = fill_missing_classes(y_proba, self.missing_indexes) 
            
        return y_proba
        
    """def predict_proba_(self, X_test):
        if self.KFold:
            return self.predict_proba_KFold(X_test)
        else:
            return self.predict_proba_(X_test)
        
    def predict_(self, X):
        if self.KFold == False:
            y_proba = self.predict_proba(X)
        else:  
            y_proba = self.predict_proba_KFold(X)
            
        y_pred = np.argmax(y_proba, axis=1)
        return y_pred + 1"""
        
    def predict(self, X):
        y_proba = self.predict_proba(X)            
        y_pred = np.argmax(y_proba, axis=1)
        
        if self.zero_based_classes:
            return y_pred
        else:
            return y_pred + 1