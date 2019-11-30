import numpy as np

from logs import print_log

def calc_accuracy(y_true, y_pred, name, classes_count, prefix="", show_matrix=True):
    y_proba = np.argmax(y_pred.reshape((-1, y_pred.shape[-1])), 1) + 1 
    classes_count = classes_count + 1
          
    if show_matrix:
        print("   ")
        for x in range(1,classes_count):
            print(" {0:3d}".format(x)),
        print(" ")
            
        for i in range(1,classes_count):
            str = "{0:2d}".format(i)
            for j in range(1,classes_count):
                ind = np.in1d(np.where(y_true == i), np.where(y_proba == j))
                tp = len(np.where(ind == True)[0])
                str = str + "{0:5d}".format(tp)
            print("{}".format(str))
    
    acc = 100. * np.sum(np.asarray(y_true) == y_proba) / len(y_true)
    print_log('{} Accuracy({})={:.2f}%'.format(prefix, name, acc))
    return acc