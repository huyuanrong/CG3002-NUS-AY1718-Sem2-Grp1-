import sklearn
from sklearn.model_selection import LeaveOneOut
from sklearn import metrics
# import metrics we'll need
from sklearn.metrics import accuracy_score 
import numpy as np
import timeit

def looalgo(X_list, y_list, trainer):
    start_time = timeit.default_timer()
    loo = LeaveOneOut()
    loo.get_n_splits(X_list)
    count = 0
    final_accuracy = 0
    # y_true_array = []
    # y_pred_array = []
    for train_index, test_index in loo.split(X_list):
        X_train, X_test = X_list[train_index], X_list[test_index]
        y_list = np.asarray(y_list)
        y_train, y_test = y_list[train_index], y_list[test_index]
        trainer.fit(X_train, y_train)
        y_pred = trainer.predict(X_test)
        # y_pred_array.append(y_pred)
        # y_true_array.append(y_test)
        pred_val = metrics.accuracy_score(y_test, y_pred)
        final_accuracy = final_accuracy + pred_val
        count = count +1
    total_time = (timeit.default_timer() - start_time)*1000
    # confusion_matrix = confusionMatrixAlgo(y_true_array, y_pred_array)   
    trainer.fit(X_list, y_list)
    sample_data = X_list[0:1, 0:]
    pred_one = trainer.predict(sample_data)
  
    print ("Time taken for Leave One Out Cross Validation: in ms: [{}]".format(total_time))
    return final_accuracy/ count
