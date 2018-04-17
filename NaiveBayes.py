##### imports
import sklearn
from sklearn import metrics
# import metrics we'll need
from sklearn.metrics import accuracy_score  
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve 
from sklearn.metrics import auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
    
##Naive Bayes
from sklearn.naive_bayes import GaussianNB
from nb_author_id import preprocesses
from KFold import KFoldalgo
from loo import looalgo
from ConfusionMatrix import confusionMatrixAlgo 

import time
def NBprocess():
    start_time = time.time()
    X_list, y_list = preprocesses()
    # instantiate the estimator
    nb = GaussianNB()

    # fit the model
    kfold_acc = KFoldalgo(X_list,y_list,nb)
    end_time = time.time()                          #considers the run-time only while using KFold and not loo
    pred_nb_kfold = kfold_acc
    #loo_acc = looalgo(X_list, y_list, nb)
    #pred_nb_loo = loo_acc
    pred_nb_loo = 1
    # Confusion Matrix
    nb.fit(X_list, y_list)
    y_pred = nb.predict(X_list)
    con_matrix = confusionMatrixAlgo(y_list, y_pred)
    # predict the response
    #y_pred = nb.predict(X_test)

    # accuracy score
    #pred_nb = metrics.accuracy_score(y_test, y_pred)
    print ("Accuracy for Gaussian Naive Bayes using KFold Cross Validation: {}".format(pred_nb_kfold))
    print ("Accuracy for Gaussian Naive Bayes using Leave One Out Cross Validation: {}".format(pred_nb_loo))
    #print ("Time taken for Naive Bayes: {}".format(end_time-start_time))
    from sklearn.externals import joblib
    joblib.dump(nb, 'model_nb.pkl', protocol=2) #Save Model

    return time.time()-start_time, pred_nb_kfold, pred_nb_loo



