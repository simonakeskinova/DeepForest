import os, os.path as osp
import numpy as np
from sklearn.model_selection import StratifiedKFold

from metrics import calc_accuracy
from size_utils import find_missing_classes, fill_missing_classes
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

class Classificator(object):
    
    def __init__(self, name, n_folds, classes_count, zero_based_classes):
        
        self.name = name
        self.n_folds = n_folds
        self.estimator1d = [None for k in range(self.n_folds)]
        self.classes_count = classes_count
        self.missing_indexes1d = [None for k in range(self.n_folds)]
        self.classifier = None
        self.KFold = True
        self.zero_based_classes = zero_based_classes
        
    def get_estimator(self):
        if self.classifier == RandomForestClassifier:
            #print("RandomForestClassifier")
            return self.classifier(n_estimators=500, max_depth=None, n_jobs=-1, verbose=False)
        else:
            #print("ExtraTreesClassifier")
            return self.classifier(n_estimators=500, max_depth=None, n_jobs=-1, verbose=False, random_state=0)
        
    def train_RF(self, X, y, X_val, y_val, keep_model_in_mem=True):
        self.classifier = RandomForestClassifier
        #est = RandomForestClassifier(n_estimators=500)
        if X_val is None:
            y_proba = self.train_KFold(X, y, keep_model_in_mem)
        else:
            y_proba = self.train_val(X, y, X_val, y_val, keep_model_in_mem)
            self.KFold = False
        
        return y_proba

    def train_ET(self, X, y, X_val, y_val, keep_model_in_mem=True):
        self.classifier = ExtraTreesClassifier
        
        if X_val is None:
            y_proba = self.train_KFold(X, y, keep_model_in_mem)
        else:
            y_proba = self.train_val(X, y, X_val, y_val, keep_model_in_mem)
            self.KFold = False
        
        return y_proba
    
    def train_KFold(self, X, y, keep_model_in_mem): #est
        n_stratify = X.shape[0]
        
        skf = StratifiedKFold(n_splits=self.n_folds, shuffle=True)
        cv = [(t, v) for (t, v) in skf.split(range(n_stratify), y)]
       
        # Fit
        y_probas = []
        n_dims = X.shape[-1] 
        #print("n_dims={}".format(n_dims))
        n_datas = X.size / n_dims 
        inverse = False
        for k in range(self.n_folds):
            if not inverse:
                train_idx, val_idx = cv[k] 
            else:
                val_idx, train_idx = cv[k]
            # fit on k-fold train
            
            est = self.get_estimator()
            
            est.fit(X[train_idx].reshape((-1, n_dims)), y[train_idx].reshape(-1))
            #est.fit(X[train_idx], y[train_idx])
            self.missing_indexes1d[k] = find_missing_classes(self.classes_count, y[train_idx])
            #print("self.missing_indexes1d[{}]={}".format(k, self.missing_indexes1d[k]))

            # predict on k-fold validation
            y_proba = est.predict_proba(X[val_idx].reshape((-1, n_dims)))
            #if len(X.shape) == 3:
            #    y_proba = y_proba.reshape((len(val_idx), -1, y_proba.shape[-1]))
            #calc_accuracy(y[val_idx], y_proba, self.name, self.classes_count, prefix="train_{}".format(k))

            # merging result
            #LOGGER.info('keep_model_in_mem = {}'.format(keep_model_in_mem))
            if k == 0:
                #if len(X.shape) == 2:
                y_proba_cv = np.zeros((n_stratify, y_proba.shape[1]), dtype=np.float32)
                #else:
                #    y_proba_cv = np.zeros((n_stratify, y_proba.shape[1], y_proba.shape[2]), dtype=np.float32)
                
                #print("y_proba.shape={}".format(y_proba.shape))
                if len(self.missing_indexes1d[k][0]) > 0:
                    y_proba_cv = fill_missing_classes(y_proba_cv, self.missing_indexes1d[k])  
                    #print("y_proba.shape={} after filling".format(y_proba.shape))
                    
                y_probas.append(y_proba_cv)
             
            #print("y_proba.shape={}".format(y_proba.shape))
            if len(self.missing_indexes1d[k][0]) > 0: 
                y_proba = fill_missing_classes(y_proba, self.missing_indexes1d[k])     
                #print("y_proba.shape={} after filling".format(y_proba.shape))
                
            y_probas[0][val_idx, :] += y_proba
            #if keep_model_in_mem:
            self.estimator1d[k] = est

        #if inverse and self.n_folds > 1:
        #    y_probas[0] /= (self.n_folds - 1)
        for y_proba in y_probas[1:]:
            y_proba /= self.n_folds
        # log
        calc_accuracy(y, y_probas[0], self.name, self.classes_count, "Train classifier ", show_matrix=False)
        
        return y_probas[0]
        
    def train_val(self, X, y, X_val, y_val, keep_model_in_mem): 
        n_stratify = X.shape[0]
               
        # Fit
        n_dims = X.shape[-1] 
        n_datas = X.size / n_dims 
        
        est = self.get_estimator()
        
        est.fit(X.reshape((-1, n_dims)), y.reshape(-1))
        self.missing_indexes1d[0] = find_missing_classes(self.classes_count, y)
        
        y_proba = est.predict_proba(X_val.reshape((-1, n_dims)))
        
        if len(self.missing_indexes1d[0][0]) > 0: 
            y_proba = fill_missing_classes(y_proba, self.missing_indexes1d[0])  
            
        #if keep_model_in_mem:
        self.estimator1d[0] = est

        # log
        calc_accuracy(y_val, y_proba, self.name, self.classes_count, "train_classificator validation set", show_matrix=True)
                
        return y_proba
        
    def predict_proba_KFold(self, X_test):
        
        # K-Fold split
        n_dims = X_test.shape[-1]
        n_datas = X_test.size / n_dims
        for k in range(self.n_folds):
            est = self.estimator1d[k]
            y_proba = est.predict_proba(X_test.reshape((-1, n_dims))) #, cache_dir=None)
            
            #print("y_proba.shape={}".format(y_proba.shape))
            if len(self.missing_indexes1d[k][0]) > 0:            
                y_proba = fill_missing_classes(y_proba, self.missing_indexes1d[k]) 
                #print("y_proba.shape={} after filling missing indexes".format(y_proba.shape))
            
            #if len(X_test.shape) == 3:
            #    y_proba = y_proba.reshape((X_test.shape[0], X_test.shape[1], y_proba.shape[-1]))
            if k == 0:
                y_proba_kfolds = y_proba
            else:
                y_proba_kfolds += y_proba
        y_proba_kfolds /= self.n_folds
        return y_proba_kfolds
        
    def predict_proba_(self, X_test):
        n_dims = X_test.shape[-1]
        n_datas = X_test.size / n_dims
        est = self.estimator1d[0]
        y_proba = est.predict_proba(X_test.reshape((-1, n_dims))) #, cache_dir=None)
            
        return y_proba
        
    def predict_proba(self, X_test):
        if self.KFold:
            return self.predict_proba_KFold(X_test)
        else:
            return self.predict_proba_(X_test)
        
    def predict(self, X):
        if self.KFold == False:
            y_proba = self.predict_proba(X)
        else:  
            y_proba = self.predict_proba_KFold(X)
            
        y_pred = np.argmax(y_proba, axis=1)
        
        if self.zero_based_classes:
            return y_pred
        else:
            return y_pred + 1