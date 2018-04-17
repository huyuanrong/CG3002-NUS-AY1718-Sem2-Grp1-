import sklearn
from sklearn.model_selection import KFold
from sklearn import metrics
# import metrics we'll need
from sklearn.metrics import accuracy_score  
import numpy as np
import timeit

def KFoldalgo(X_list, y_list, trainer):
    start_time_kfold = timeit.default_timer()
    print (y_list)
    #num split selected as 50.
    kf = KFold(n_splits = 50)
    kf.get_n_splits(X_list)
    count = 0
    final_accuracy = 0
    for train_index, test_index in kf.split(X_list):
        X_train, X_test = X_list[train_index], X_list[test_index]
        y_list = np.asarray(y_list)
        y_train, y_test = y_list[train_index], y_list[test_index]
        trainer.fit(X_train, y_train)
        y_pred = trainer.predict(X_test)
        #compute the probability of success given (pred, and correct)
        pred_val = metrics.accuracy_score(y_test, y_pred)
        #Sum the prediction up, to find average later.
        final_accuracy = final_accuracy + pred_val
        count = count +1
    trainer.fit(X_list, y_list)
    total_time_kfold = (timeit.default_timer() - start_time_kfold)*1000
    #sample first 1st set of data(50 sampling points)
    sample_data = X_list[0:1, 0:]
    start_time = timeit.default_timer()
    pred_one = trainer.predict(sample_data)
    total_time = (timeit.default_timer() - start_time)*1000
    print ("***************************************************")
    print ("Time taken for one prediction in ms: {0:.50f}".format(total_time))
    print ("Prediction for current algorithm, 1st window(0 = Walk, 1 = Jog, 2 = Run): {}".format(pred_one))
    print ("label for current algorithm, 1st window: [{}]".format(y_list[0]))

    #sample 8500/25 = 340
    sample_data = X_list[339:340, 0:]
    pred_two = trainer.predict(sample_data)
    print ("Prediction for current algorithm, 340th window(0 = Walk, 1 = Jog, 2 = Run): {}".format(pred_two))
    print ("label for current algorithm, 340th window: [{}]".format(y_list[339]))

    #sample 725/25 = 29
    sample_data = X_list[29:30, 0:]
    pred_three = trainer.predict(sample_data)
    print ("Prediction for current algorithm, 30th window(0 = Walk, 1 = Jog, 2 = Run): {}".format(pred_three))
    print ("label for current algorithm, 30th window: [{}]".format(y_list[29]))
    print ("Total time taken for Kfold algo in ms : [{}]".format(total_time_kfold))
    #returns accuracy average
    return final_accuracy/ count
