import argparse
import sys
import numpy as np

sys.path.insert(0, "lib")

from mydataset import save_dataset, load_dataset
from cascade import Cascade
from scanning_mixed_cascade import ScanningMixedCascade
from scanning_sequential_cascade import ScanningSequentialCascade
from sklearn.ensemble import RandomForestClassifier
from logs import print_log

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", dest="model", type=str, default=None, help="Config File")
    args = parser.parse_args()
    return args
    
def load_json(path):
    import simplejson
    
    lines = []
    with open(path) as f:
        for row in f.readlines():
            if row.strip().startswith("//"):
                continue
            lines.append(row)
    return simplejson.loads("\n".join(lines))

def prepare_data(config, make_validation_set=True): 
    train_path = config["Data"]["TrainDataPath"]
    (X_train, y_train) = load_dataset(train_path)
    #print("y_train[1]={}".format(len(y_train[y_train == 1])))
    
    test_path = config["Data"]["TestDataPath"]
    (X_test, y_test) = load_dataset(test_path)
    #print("y_test[1]={}".format(len(y_test[y_test == 1])))
        
    return X_train, y_train, X_test, y_test
    
def calc_accuracy(y_true, y_pred, name, classes_count, prefix=""):        
    print("   ")
    for x in range(1, classes_count+1):
        print(" {0:4d}".format(x)),
    print(" ")
        
    for i in range(1, classes_count+1):
        str = "{0:2d}".format(i)
        for j in range(1, classes_count+1):
            ind = np.in1d(np.where(y_true == i), np.where(y_pred == j))
            tp = len(np.where(ind == True)[0])
            str = str + "{0:5d}".format(tp)
        print("{}".format(str))
    
    acc = 100. * np.sum(np.asarray(y_true) == y_pred) / len(y_true)
    print_log('{} Accuracy({})={:.2f}%'.format(prefix, name, acc))
    return acc

def train_and_test_cascade(config, title, make_validation_set=False):

    X_train, y_train, X_test, y_test = prepare_data(config, make_validation_set)
    classes_count = config["ClassesCount"]
    zero_based_classes = config["ZeroBasedClasses"]
    
    cascade = Cascade(config["Cascade"], classes_count, zero_based_classes)
    optimal_level_count, _ = cascade.train(X_train, y_train)
    
    y_predicted = cascade.predict(X_test)
    return calc_accuracy(y_test, y_predicted, "Cascade test", classes_count, title), optimal_level_count    
    
def train_and_test_scanning_cascade(config, title, make_validation_set=False):

    X_train, y_train, X_test, y_test = prepare_data(config, make_validation_set)
    classes_count = config["ClassesCount"]
    cascade_type = config["CascadeType"]
    
    if cascade_type == "SequentialCascade":
        cascade = ScanningSequentialCascade(config)
    else:    
        cascade = ScanningMixedCascade(config)
        
    optimal_level_count = cascade.train(X_train, y_train)
    
    y_predicted = cascade.predict(X_test)
    return calc_accuracy(y_test, y_predicted, "Scanning test", classes_count, title), optimal_level_count    
    
if __name__ == "__main__":
    args = parse_args()
    if args.model is None:
        print("Missing model parameter. Quit")
        sys.exit()
    else:
        config = load_json(args.model)
        
    result = []
    result_levels = []
    
    for i in range(1):
        print("--------------- {} -------------------".format(i))
        
        if 'Scanning' not in config:
            acc, count = train_and_test_cascade(config, "Adverb")
        else:
            acc, count = train_and_test_scanning_cascade(config, "Adverb")
        result.append(acc)
        result_levels.append(count)
        
    for i in range(1):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
       
        print("Result {} = {} / level_count = {}".format(i, result[i], result_levels[i]))