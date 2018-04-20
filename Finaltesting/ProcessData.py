#!/usr/bin/python
import numpy as np
import pandas as pd
import scipy as sc
import os
##### imports
import sklearn
from sklearn import metrics
from scipy.fftpack import fft
# import metrics we'll need
from sklearn.metrics import accuracy_score  
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve 
from sklearn.metrics import auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from math import ceil
from statistics import mode

def preprocesses(segment):
    segment = np.array(segment)
    stat_list = []
    #extract features
    temp_row = []
    for j in range(0,12):
        temp = segment[0:,j]
        #Mean = sum of everything / no. of data point
        mean = np.mean(temp)
        #Median = middle value of sorted
        median = np.median(temp)
        #Std = Standard Deviation, How individual points differs from the mean
        std = np.std(temp)
        #iqr = Inter-Quartile Range, 75th percentile - 25th percentile
        iqr = np.percentile(temp, [75 ,25])
        q75, q25 = np.percentile(temp, [75 ,25])
        iqr = q75 - q25
        maximum = np.amax(temp)
        temp_row.append(mean)
        temp_row.append(median)
        temp_row.append(std)
        temp_row.append(iqr)
        temp_row.append(maximum)
        Fourier_temp = fft(temp)
        #Fourier = Power Spectral Density, essentially, Summation |Ck|^2
        fourier = np.abs(Fourier_temp)**2
        value = 0
        for x in range (len(fourier)):
            value = value + (fourier[x] * fourier [x])
        value = value / len(fourier)
        temp_row.append(value)
    stat_list.append(temp_row)
    #print stat_list

    #label_list.append(Counter(labels[i]).most_common(1)[0])
    #m = list(labels[i])
    #hash(tuple(m))

#normalizing the features
    stat_list = preprocessing.normalize(stat_list)
#use this code to extract top 5 features only
#stat_list = stat_list[0: ,[5,7,10,11,35]]

#X_train, X_test, y_train, y_test = train_test_split(stat_list, label_list,train_size=0.75,test_size=0.25, random_state=42)
#scaler = StandardScaler()
#scaler.fit(X_train)
#X_train = scaler.transform(X_train)
#X_test = scaler.transform(X_test)
#return stat_list,label_list
    #return stat_list[0: , [65,71,11,41,29,59,35,5,17,23,53,47,58,64,63,57,56,69,70,60,62,40,7,37,61,6,54,4,55,22,25,28,34,3,10,24,66,67,16,36]]
    #return stat_list[0: , [65,29,71,41,59,35,11,17,23,5,53,47,58,63,64,57,7,70,56,37,62,55,60,54,0,69,4,25]]
    #return stat_list[0: , [5,65,11,35,41,17,59,29,23,71,53,47,64,57,58,63,70,3,62,61]]
    return stat_list[0: , [65,41,29,71,5,11,59,17,23,35,53,47,58,64,57,70,63,62,7,37,54,4,24,69,61,55,56,60,25,66,28,6,22,10,67,16,40,9,34,0,12,13,48,27,32,3,18,33,21,49,2,36,20,52,31,1,19,14,46]]
    #return stat_list
    #return stat_list[0: , [65,5,29,35,11,17,23,59,41,71,53,64,70,56,57,63,62,54,58,22,60,3,68,69,61,37,9]]


