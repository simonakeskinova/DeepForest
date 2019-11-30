import numpy as np

def find_missing_classes(n_classes, y_train):
    y_unique = np.unique(y_train)
    #print("y_unique={}".format(y_unique))
    classes = np.arange(1, n_classes + 1, 1)
    #print("classes={}".format(classes))
            
    missing = np.isin(classes, y_unique)
    #print("missing={}".format(missing))
    return np.where(missing == False)
        
def fill_missing_classes(y, missing_indexes):
    for i in missing_indexes[0]:
        y = np.insert(y, i, 0, axis=1)
        
    return y