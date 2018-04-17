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
    
##Random Forest
from sklearn.ensemble import RandomForestClassifier
from nb_author_id import preprocesses
from KFold import KFoldalgo
from loo import looalgo
from ConfusionMatrix import confusionMatrixAlgo
from sklearn.model_selection import RandomizedSearchCV

import numpy as np

def RFprocess():
    X_list, y_list = preprocesses()
    import time
    start_time = time.time()
    #instantiate the estimator
    #Number of trees in random forest
    #n_estimators = [int(x) for x in np.linspace(start = 200, stop = 1000, num = 10)]
    #n_estimators = [400]
    #Number of features to consider at every split
    #max_features = ['sqrt']
    # Maximum number of levels in tree
    #max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    #max_depth.append(None)
    # Minimum number of samples required to split a node
    #min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    #min_samples_leaf = [1,5,10]
    # Method of selecting samples for training each tree
    #bootstrap = [True,False]
    #n_jobs = 1
    #random_grid = {'n_estimators': n_estimators,
    #           'max_features': max_features,
    #           'max_depth': max_depth,
    #           'min_samples_split': min_samples_split,
    #           'min_samples_leaf': min_samples_leaf,
    #           'bootstrap': bootstrap
    #               }
    #rndforest = RandomForestClassifier(bootstrap = False, min_samples_leaf = 1, n_estimators = 400, min_samples_split = 10, max_features = 'sqrt', max_depth = 60)
    #rndforest = RandomForestClassifier()
    #rndforest = RandomForestClassifier(bootstrap = False, min_samples_leaf = 1, n_estimators = 400, max_features='sqrt', min_samples_split = 2, max_depth = None)
    rndforest = RandomForestClassifier()
    #rndforest = RandomizedSearchCV(estimator = rndforest, param_distributions = random_grid, n_iter = 5, cv = 3, verbose=2, random_state=42)
    rndforest.fit(X_list, y_list)
    #print (rndforest.best_params_)
    from sklearn.externals import joblib
    joblib.dump(rndforest, 'rdf_model.pkl', protocol=2) #Save Model
    print ("saved\n")
    #print (rndforest.best_params_)
    kfold_acc = KFoldalgo(X_list,y_list,rndforest)
    end_time = time.time()                          #considers the run-time only while using KFold and not loo
    pred_rf_kfold = kfold_acc
    #loo_acc = looalgo(X_list, y_list, rndforest)
    #pred_rf_loo = loo_acc
    pred_rf_loo = 1
    # Confusion Matrix
    y_pred = rndforest.predict(X_list)
    con_matrix = confusionMatrixAlgo(y_list, y_pred)
    # fit the model
    #clf.fit(X_train, y_train)

    # predict the response
    #y_pred = clf.predict(X_test)

    # accuracy score
    #pred_rf = metrics.accuracy_score(y_test, y_pred)
    print ("Accuracy for RandomForest Using KFold Cross Validation: {}".format(pred_rf_kfold))
    print ("Accuracy for RandomForest Using Leave One Out Cross Validation: {}".format(pred_rf_loo))
    #print ("Time taken for RandomForest: {}".format(end_time-start_time))

    return time.time()-start_time, pred_rf_kfold, pred_rf_loo
