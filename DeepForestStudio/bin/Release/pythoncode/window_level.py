import os, os.path as osp
import numpy as np
from ansamble import Ansamble
from scanner import Scanner

class WindowLevel(object):
    
    def __init__(self, config, windows_count, classes_count, zero_based_classes):
        
        self.config = config
        
        self.ansambles1d = []
        self.windows_count = windows_count
        self.classes_count = classes_count
        self.zero_based_classes = zero_based_classes
        
        """self.ansamble0 = None
        self.ansamble1 = None
        self.ansamble2 = None
        self.ansamble3 = None
        #self.scanner1 = None
        #self.scanner2 = None
        #self.scanner3 = None"""
        
    def train(self, X_wins, y, y_proba):
        if y_proba is None:
            X_win = X_wins[0]
            ansamble = Ansamble(self.config, self.classes_count, self.zero_based_classes)
            y_proba = ansamble.train(X_win, y, None, None) 

            self.ansambles1d.append(ansamble)           
        else:    
            for i in range(self.windows_count):
                X_win = np.concatenate((X_wins[i], y_proba), axis=1)
                
                ansamble = Ansamble(self.config, self.classes_count, self.zero_based_classes)
                y_proba = ansamble.train(X_win, y, None, None)
            
                self.ansambles1d.append(ansamble)
    
        """#self.scanner1 = Scanner(self.n_folds, self.classes_count, 10, 3, 1)
        #self.scanner1.train(X, y)
        #X_win1 = self.scanner1.get_scanned_data(X)
        
        #self.ansamble0 =  Ansamble(self.name, self.n_folds, self.classes_count)
        #y_proba0 = self.ansamble0.train(X_win1, y)
        
        X_win1 = np.concatenate((X_win1, y_proba), axis=1)
        self.ansamble1 = Ansamble("ansamble_window_1", self.n_folds, self.classes_count)
        y_proba1 = self.ansamble1.train(X_win1, y)
        
        #self.scanner2 = Scanner(self.n_folds, self.classes_count, 10, 5, 1)
        #self.scanner2.train(X, y)
        #X_win2 = self.scanner2.get_scanned_data(X)
        X_win2 = np.concatenate((X_win2, y_proba1), axis=1)
        self.ansamble2 =  Ansamble("ansamble_window_2", self.n_folds, self.classes_count)
        y_proba2 = self.ansamble2.train(X_win2, y)
        
        #self.scanner3 = Scanner(self.n_folds, self.classes_count, 10, 7, 1)
        #self.scanner3.train(X, y)
        #X_win3 = self.scanner3.get_scanned_data(X)
        X_win3 = np.concatenate((X_win3, y_proba2), axis=1)
        self.ansamble3 =  Ansamble("ansamble_window_3", self.n_folds, self.classes_count)
        y_proba3 = self.ansamble3.train(X_win3, y)  """      
        
        return y_proba
        
    def predict_proba(self, X_wins, y_proba):
    
        for i in range(len(self.ansambles1d)):
            if y_proba is None:
                X_win = X_wins[i]
            else:
                X_win = np.concatenate((X_wins[i], y_proba), axis=1)
                
            y_proba = self.ansambles1d[i].predict_proba(X_win)
    
        """X_win1 = np.concatenate((X_win1, y_proba), axis=1)
        y_proba1 = self.ansamble1.predict_proba(X_win1)
        
        X_win2 = np.concatenate((X_win2, y_proba1), axis=1)
        y_proba2 = self.ansamble2.predict_proba(X_win2)
        
        X_win3 = np.concatenate((X_win3, y_proba2), axis=1)
        y_proba3 = self.ansamble3.predict_proba(X_win3)"""
        
        return y_proba
        
    def predict(self, X):
        y_proba = self.predict_proba(X)
        y_pred = np.argmax(y_proba, axis=1)
        
        if self.zero_based_classes:
            return y_pred
        else:
            return y_pred + 1