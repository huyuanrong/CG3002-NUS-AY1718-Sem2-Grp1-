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

##Feature Selection
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from nb_author_id import preprocesses

X_list, y_list = preprocesses()
clf = RandomForestClassifier(random_state = 1)
#fit the model
clf.fit(X_list,y_list)

importance = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],
             axis=0)
indices = np.argsort(importance)[::-1]
# Print the feature ranking
print("Feature ranking:")

for f in range(X_list.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importance[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importance")
plt.bar(range(X_list.shape[1]), importance[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X_list.shape[1]), indices)
plt.xlim([-1, X_list.shape[1]])
plt.show()
