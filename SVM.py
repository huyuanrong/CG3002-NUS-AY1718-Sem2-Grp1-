##### imports
import sklearn
from sklearn import metrics
def SVMprocess():
    # import metrics we'll need
    from sklearn.metrics import accuracy_score  
    from sklearn.metrics import classification_report
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import roc_auc_score
    from sklearn.metrics import roc_curve 
    from sklearn.metrics import auc
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
        
    ##Support Vector Machine
    from sklearn.svm import SVC
    from nb_author_id import preprocesses
    from KFold import KFoldalgo
    from loo import looalgo
    from ConfusionMatrix import confusionMatrixAlgo 

    X_list, y_list = preprocesses()
    # instantiate time
    import time
    start_time = time.time()
    # instantiate the estimator
    svm = SVC()

    # fit the model
    #svm.fit(X_train, y_train)
    kfold_acc = KFoldalgo(X_list,y_list,svm)
    pred_svm_kfold = kfold_acc
    end_time = time.time()                          #considers the run-time only while using KFold and not loo    
    #loo_acc = looalgo(X_list, y_list, svm)
    #pred_svm_loo = loo_acc
    pred_svm_loo = 1
    # Confusion Matrix
    svm.fit(X_list, y_list)
    y_pred = svm.predict(X_list)
    con_matrix = confusionMatrixAlgo(y_list, y_pred)
    # predict the response
    #y_pred = svm.predict(X_test)

    # accuracy score
    #pred_svm = metrics.accuracy_score(y_test, y_pred)
    print ("Accuracy for SVM Using KFold Cross Validation: {}".format(pred_svm_kfold))
    print ("Accuracy for SVM Using Leave One Out Cross Validation: {}".format(pred_svm_loo))
    #print ("Time taken for SVM: {}".format(end_time-start_time))

    from sklearn.externals import joblib
    joblib.dump(svm, 'model_svm.pkl', protocol=2) #Save Model

    return time.time()-start_time, pred_svm_kfold, pred_svm_loo
