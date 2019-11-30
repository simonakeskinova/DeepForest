#SequentialCascade
import os, os.path as osp
import numpy as np
import pickle 

from scanner import Scanner
from cascade import Cascade
from metrics import calc_accuracy
from logs import print_log

def check_dir(path):
    d = osp.abspath(osp.join(path, osp.pardir))
    if not osp.exists(d):
        os.makedirs(d)
        
class ScanningSequentialCascade(object):
    
    def __init__(self, config):
        
        self.cascade_config = config["Cascade"]
        self.scanning_config = config["Scanning"]
        
        self.name = self.scanning_config["Name"]
        self.classes_count = config["ClassesCount"]
        self.save_directory = self.scanning_config["TempDirectory"]
        self.keep_model_in_mem = self.scanning_config["KeepModelInMemory"]
        self.zero_based_classes = config["ZeroBasedClasses"]
        
        #self.scanners_config = config["scanners"]
        
        self.cascades = []
        self.X_wins1d = []
        self.scanners1d = []     
        self.optimal_level_count = 0        
        self.scanners_count = len(self.scanning_config["Scanners"])
        
        """self.scanner1 = None
        self.scanner2 = None
        self.scanner3 = None
        self.X_win1 = None
        self.X_win2 = None
        self.X_win3 = None"""
    
    def train_scanners(self, X, y):
        for i in range(self.scanners_count):
            print_log("Start scanner_{}".format(i))
            scanner = Scanner(self.scanning_config["Scanners"][i], self.classes_count, self.zero_based_classes, self.scanning_config["ContextSize"], self.scanning_config["WordSize"], self.scanning_config["ContextPOSSize"])
            scanner.train(X, y)
            
            print_log("Start scanner_{}.get_scanned_data".format(i))
            X_win = scanner.get_scanned_data(X)
            print_log("X_win_{}[{}].shape={}".format(i, self.scanning_config["Scanners"][i]["WindowSize"], X_win.shape))
            
            self.scanners1d.append(scanner)
            self.X_wins1d.append(X_win)
        
        """print("{} Start scaner1".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))))
        self.scanner1 = Scanner(self.n_folds, self.classes_count, 10, 3, 1, 10)
        self.scanner1.train(X, y)  
        print("{} Start scaner1.get_scanned_data".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))))
        self.X_win1 = self.scanner1.get_scanned_data(X)
        print("{} X_win1[3].shape={}".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time())), self.X_win1.shape))
        
        print("{} Start scaner2".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))))
        self.scanner2 = Scanner(self.n_folds, self.classes_count, 10, 5, 1, 10)
        self.scanner2.train(X, y)
        print("{} Start scaner2.get_scanned_data".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))))
        self.X_win2 = self.scanner2.get_scanned_data(X)
        print("{} X_win2[5].shape={}".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time())), self.X_win2.shape))
        
        print("{} Start scaner3".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))))
        self.scanner3 = Scanner(self.n_folds, self.classes_count, 10, 7, 1, 10)
        self.scanner3.train(X, y)
        print("{} Start scaner3.get_scanned_data".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))))
        self.X_win3 = self.scanner3.get_scanned_data(X)
        print("{} X_win3[7].shape={}".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time())), self.X_win3.shape))"""
    
    def train(self, X, y): 
        self.train_scanners(X, y)
        
        #level_count = 0 
        levels = []
        y_proba = None
               
        """if level_count > self.max_levels_count:
            self.optimal_level_count = level_count
            print_log("-----!!!!!! Optimal level count {}".format(self.optimal_level_count))
            break"""
        
        print_log("-----!!!!!! Start train cascade")
                    
        for i in range(len(self.X_wins1d)):
            cascade = Cascade(self.cascade_config, self.classes_count, self.zero_based_classes, i)
            
            """if i > 0:
                X_win = np.concatenate((self.X_wins1d[i], y_proba), axis=1)
            else:"""
            X_win = self.X_wins1d[i]
                
            count, y_proba = cascade.train(X_win, y, None, None, y_proba) #(X_win, y, None, None)
            levels.append(count)
            
            if self.keep_model_in_mem:
                self.cascades.append(cascade)
            else:
                self.save_estimator(i, cascade)
                    
        accuracy = calc_accuracy(y, y_proba, self.name, self.classes_count, "train_window_cascade2", show_matrix=False)
        
        """if level_count > 1 and last_accuracy >= accuracy:
            self.optimal_level_count = level_count
            print_log("-----!!!!!! Optimal level count {}".format(self.optimal_level_count))
            break               """
            
        """last_accuracy = accuracy """
        
        """if level_count == 0:
            if self.keep_model_in_mem:
                self.levels.append(ansamble)
            else:
                self.save_estimator(level_count, ansamble)
        else:
            if self.keep_model_in_mem:
                self.levels.append(window_level)
            else:
                self.save_estimator(level_count, window_level)
                
        level_count += 1"""
            
        return levels

    def predict_proba(self, X):
        X_test_wins = []
        
        for i in range(self.scanners_count):
            X_test_win = self.scanners1d[i].get_scanned_data(X)
            X_test_wins.append(X_test_win)
            
        """X_test_win1 = self.scanner1.get_scanned_data(X)
        X_test_win2 = self.scanner2.get_scanned_data(X)
        X_test_win3 = self.scanner3.get_scanned_data(X)"""
        
        for i in range(len(X_test_wins)):
            if self.keep_model_in_mem:
                classifier = self.cascades[i]
            else:
                classifier = self.load_estimator(i) 

            if i > 0:
                X_win = np.concatenate((X_test_wins[i], y_curr_proba), axis=1)
            else:
                X_win = X_test_wins[i]              
            
            y_curr_proba = classifier.predict_proba(X_win)
        
        #y_proba /= self.optimal_level_count
        return y_curr_proba
        
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
        print_log("save model as {}_layer_{}.pkl".format(self.name, layer_id))
        data_path = osp.join(self.save_directory, "{}_layer_{}.pkl".format(self.name, layer_id))
        check_dir(data_path)
       
        with open(data_path, "wb") as f:
            pickle.dump(classifier, f, pickle.HIGHEST_PROTOCOL)
                
    def load_estimator(self, layer_id):
        data_path = osp.join(self.save_directory, "{}_layer_{}.pkl".format(self.name, layer_id))
        check_dir(data_path)
        
        # load
        with open(data_path, "rb") as f:
            classifier = pickle.load(f)
        return classifier