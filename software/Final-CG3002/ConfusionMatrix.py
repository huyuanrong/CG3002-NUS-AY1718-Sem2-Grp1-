import sklearn
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix

def confusionMatrixAlgo(y_true, y_pred):
	
	confusionmatrix = confusion_matrix(y_true, y_pred)
	print (confusionmatrix)

	y_actu = pd.Series(y_true, name = 'Actual')
	y_pred = pd.Series(y_pred, name = 'Predicted')
	df_confusion = pd.crosstab(y_actu, y_pred, rownames = ['Actual'], colnames = ['Predicted'], margins = True)
	print (df_confusion)
        # If you look at the output for this ^, sometimes the middle row is missing. lol
