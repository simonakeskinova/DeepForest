import numpy as np

from classificator2 import Classificator
from logs import print_log

class Scanner(object):
    
    def __init__(self, config, classes_count, zero_based_classes, context_size, context_word_size, context_pos_size):
        
        self.classes_count = classes_count
        self.zero_based_classes = zero_based_classes
        self.context_size = context_size
        self.window_size = config["WindowSize"]
        self.context_word_size = context_word_size
        self.context_pos_size = context_pos_size
        self.classifiers_config = config["Classifiers"]
        
        self.name = "scanner"
        self.classifier1d = []
        self.classifiers_count = len(self.classifiers_config)
        #self.classifier2 = None
        
    def scan_data(self, X, y):
        X_new = []
        y_new = []
        
        for i in xrange(X.shape[0]):
            x_array = X[i]
            y_array = y[i]
            
            word = x_array[0:1*self.context_word_size]
            context = x_array[1*self.context_word_size:1*self.context_word_size+self.context_size*self.context_word_size]
            context_pos = x_array[1*self.context_word_size+self.context_size*self.context_word_size:]
                    
            #context_size = len(context)
            groups = self.context_size - self.window_size + 1
            
            for j in range(0, groups):
                X_new.append(np.concatenate([word, context[j*self.context_word_size:self.window_size*self.context_word_size+j*self.context_word_size], context_pos[j*self.context_pos_size:self.window_size*self.context_pos_size+j*self.context_pos_size]]))
                y_new.append(y_array)
        
        X_new = np.asarray(X_new)
        y_new = np.asarray(y_new)
            
        return X_new, y_new     
        
    def train(self, X, y):
        print_log("Before scanning X.shape={}".format(X.shape))
        print_log("Start scanning data")
        X_window, y_window = self.scan_data(X, y)
        print_log("After scanning X_window.shape={}".format(X_window.shape))
    
        for i in range(self.classifiers_count):
            print_log("Train scanning classifier {}".format(i))
            classifier = Classificator(self.classifiers_config[i], self.classes_count, self.zero_based_classes)
            classifier.train(X_window, y_window, None, None)
            self.classifier1d.append(classifier)
        
        """print("{} Train first scanning classifier".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))))
        self.classifier1 = Classificator(self.name, self.n_folds, self.classes_count)
        self.classifier1.train_RF(X_window, y_window)
        
        print("{} Train second scanning classifier".format(time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))))
        self.classifier2 = Classificator(self.name, self.n_folds, self.classes_count)
        self.classifier2.train_ET(X_window, y_window)"""
        
    def get_scanned_data_(self, X):
        X_win = []
        
        groups = self.context_size - self.window_size + 1
        
        for i in xrange(X.shape[0]):
            X_new = []
            x_array = X[i]
            
            word = x_array[0:1*self.context_word_size]
            context = x_array[1*self.context_word_size:1*self.context_word_size+self.context_size*self.context_word_size]
            context_pos = x_array[1*self.context_word_size+self.context_size*self.context_word_size:]
                    
            #context_size = len(context)
            
            for j in range(0, groups):
                X_new.append(np.concatenate([word, context[j*self.context_word_size:self.window_size*self.context_word_size+j*self.context_word_size], context_pos[j*self.context_pos_size:self.window_size*self.context_pos_size+j*self.context_pos_size]]))
                                
            X_new = np.asarray(X_new)
            
            y_probas = []
            
            for i in range(self.classifiers_count):
                y_proba = self.classifier1d[i].predict_proba(X_new)
                
                y_probas = np.concatenate((y_probas, y_proba), axis=None)
            
            #y_1 = self.classifier1.predict_proba(X_new)
            #y_2 = self.classifier2.predict_proba(X_new)
            
            X_win.append(y_probas)
            
        X_win = np.asarray(X_win)
        return X_win
        
    def get_scanned_data(self, X):
        X_win = []
        y_probas = None
        
        groups = self.context_size - self.window_size + 1
        
        X_new = [item for sublist in [[np.concatenate((X[i][0:self.context_word_size],X[i][j*self.context_word_size+self.context_word_size:self.context_word_size*j+self.context_word_size+self.window_size*self.context_word_size],X[i][self.context_word_size+self.context_size*self.context_word_size+j*self.context_pos_size:self.context_word_size+self.context_size*self.context_word_size+j*self.context_pos_size+self.window_size*self.context_pos_size])) for j in range(groups)] for i in range(X.shape[0])] for item in sublist]
        X_new = np.asarray(X_new)
        
        #print_log("X_new={}".format(X_new))
        
        for i in range(self.classifiers_count):
            y_proba = self.classifier1d[i].predict_proba(X_new)
            
            y_proba = [np.concatenate([y_proba[groups*i+j] for j in range(groups)]) for i in range(X.shape[0])]
            
            if y_probas is None:
                y_probas = y_proba
            else:
                y_probas = np.hstack((y_probas, y_proba))
            
        #X_win = np.asarray(X_win)
        return np.asarray(y_probas)