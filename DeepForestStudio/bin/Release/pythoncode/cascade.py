import os, os.path as osp
import numpy as np
import pickle 

from ansamble import Ansamble
from metrics import calc_accuracy
from logs import print_log

def check_dir(path):
    d = osp.abspath(osp.join(path, osp.pardir))
    if not osp.exists(d):
        os.makedirs(d)
        
class Cascade(object):
    
    def __init__(self, config, classes_count, zero_based_classes, prefix=""):
        
        self.name = config["Name"]
        self.config = config
        self.classes_count = classes_count #config["ClassesCount"]
        self.max_levels_count = config["MaxLevelCount"]
        self.keep_model_in_mem = config["KeepModelInMemory"]
        self.save_directory = config["TempDirectory"]
        self.prefix = prefix
        self.zero_based_classes = zero_based_classes
        
        self.levels = []
        self.optimal_level_count = 0        
    
    def train(self, X, y, X_val=None, y_val=None, y_proba_for_concat=None): 
        level_count = 0
        X_val_transform = None
        
        while 1:        
            if level_count > self.max_levels_count:
                self.optimal_level_count = level_count
                print_log("-----!!!!!! Optimal level count {}".format(self.optimal_level_count))
                break
            
            print_log("-----!!!!!! Start level {}".format(level_count + 1))
            ansamble = Ansamble(self.config, self.classes_count, self.zero_based_classes)
            
            if level_count == 0:
                if y_proba_for_concat is None:
                    X_win = X
                else:
                    X_win = np.concatenate((X, y_proba_for_concat), axis=1)
                
                y_proba = ansamble.train(X_win, y, X_val, y_val)
            else:
                if y_val is None:
                    X_transform = self.transform(X, y_proba)
                else:
                    X_transform = self.transform(X, y_proba)
                    X_val_transform = self.transform(X_val, y_proba)
                    
                y_proba = ansamble.train(X_transform, y, X_val_transform, y_val)                
                        
            if y_val is None:
                accuracy = calc_accuracy(y, y_proba, self.name, self.classes_count, "train_classifier_average ", show_matrix=False)
            else:   
                accuracy = calc_accuracy(y_val, y_proba, self.name, self.classes_count, "train_classifier_average ", show_matrix=False)
                            
            if level_count > 0 and last_accuracy >= accuracy:
                self.optimal_level_count = level_count
                print_log("-----!!!!!! Optimal level count {}".format(self.optimal_level_count))
                break               
                
            last_accuracy = accuracy  
            
            if self.keep_model_in_mem:
                self.levels.append(ansamble)
            else:
                self.save_estimator(level_count, ansamble)
            level_count += 1
            
        return self.optimal_level_count, y_proba

    def predict_proba(self, X):
        y_proba = np.zeros((X.shape[0], self.classes_count))
        
        for level in range(self.optimal_level_count):
            if self.keep_model_in_mem:
                est = self.levels[level]
            else:
                est = self.load_estimator(level)
            
            if level == 0:
                y_curr_proba = est.predict_proba(X)
                #y_proba = y_curr_proba
            else:
                X_transform = self.transform(X, y_curr_proba)
                y_curr_proba = est.predict_proba(X_transform)
               
            y_proba += y_curr_proba
        
        y_proba /= self.optimal_level_count
        return y_proba
        
    def predict(self, X):
        y_proba = self.predict_proba(X)
        y_pred = np.argmax(y_proba, axis=1)
        
        if self.zero_based_classes:
            return y_pred
        else:
            return y_pred + 1
        
    def transform(self, X, y):
        return np.concatenate((X,y),axis=1)
        
    def save_estimator(self, layer_id, classifier):
        data_path = osp.join(self.save_directory, "{}_layer_{}_{}.pkl".format(self.name, layer_id, self.prefix))
        check_dir(data_path)
       
        with open(data_path, "wb") as f:
            pickle.dump(classifier, f, pickle.HIGHEST_PROTOCOL)
                
    def load_estimator(self, layer_id):
        data_path = osp.join(self.save_directory, "{}_layer_{}_{}.pkl".format(self.name, layer_id, self.prefix))
        check_dir(data_path)
        
        # load
        with open(data_path, "rb") as f:
            classifier = pickle.load(f)
        return classifier