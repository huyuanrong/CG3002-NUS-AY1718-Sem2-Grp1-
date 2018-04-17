###imports
import sklearn

from SVM import SVMprocess
from KNN import KNNprocess
from NaiveBayes import NBprocess
from RandomForest import RFprocess

#SVMtime,SVM_kfold_acc, SVM_loo_acc = SVMprocess()
#KNNtime, KNN_kfold_acc, KNN_loo_acc = KNNprocess()
#NBtime, NB_kfold_acc, NB_loo_acc = NBprocess()
RFtime, RF_kfold_acc, NB_loo_acc = RFprocess()
