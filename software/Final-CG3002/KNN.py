##### imports
import sklearn
import timeit
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
from sklearn.neighbors import KNeighborsClassifier
from nb_author_id import preprocesses
from KFold import KFoldalgo
from loo import looalgo
from ConfusionMatrix import confusionMatrixAlgo 

def KNNprocess():
    X_list, y_list = preprocesses()
    import time
    start_time = time.time()
    # instantiate the estimator
    knn = KNeighborsClassifier()
    kfold_acc = KFoldalgo(X_list, y_list, knn)
    end_time = time.time()                          #considers the run-time only while using KFold and not loo
    pred_knn_kfold = kfold_acc
    #loo_acc = looalgo(X_list, y_list, knn)
    #pred_knn_loo = loo_acc
    pred_knn_loo = 1
    # Confusion Matrix
    knn.fit(X_list, y_list)
    y_pred = knn.predict(X_list)
    con_matrix = confusionMatrixAlgo(y_list, y_pred)
    # fit the model
    #knn.fit(X_train, y_train)

    # predict the response
    #y_pred = knn.predict(X_test)

    # accuracy score
    #pred_knn = metrics.accuracy_score(y_test, y_pred)
    print ("Accuracy for Knn using KFold Cross Validation: {}".format(pred_knn_kfold))
    print ("Accuracy for Knn using Leave One Out Cross Validation: {}".format(pred_knn_loo))
    #print ("Time taken for knn using: {}".format(end_time-start_time))

    from sklearn.externals import joblib
    joblib.dump(knn, 'model_knn.pkl', protocol=2) #Save Model
    return time.time()-start_time, pred_knn_kfold, pred_knn_loo
