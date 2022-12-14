# -*- coding: utf-8 -*-
"""Copy of Music classification and Recommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F9mgUoXdoLqpHaEwrak43SoNJewdo97E
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
import sklearn

# Librosa (the mother of audio files)
import librosa
import librosa.display
import IPython.display as ipd
import warnings
warnings.filterwarnings('ignore')

from google.colab import drive
drive.mount('/content/drive')

!unzip '/content/drive/MyDrive/Music GTZAN/GTZAN Music Dataset.zip' -d "/content/drive/MyDrive/Music GTZAN/ Music GTZAN"

import os
general_path = '/content/drive/MyDrive/music data/Data'
print(list(os.listdir(f'/content/drive/MyDrive/Music GTZAN/ Music GTZAN/genres_original')))

pd.read_csv("/content/drive/MyDrive/Music GTZAN/ Music GTZAN/features_30_sec.csv")

y, sr = librosa.load(f'/content/drive/MyDrive/Music GTZAN/ Music GTZAN/genres_original/rock/rock.00025.wav')

print('y:', y, '\n') # different audio files stored in y
print('y shape:', np.shape(y), '\n')
print('Sample Rate (KHz):', sr, '\n')

# Verify length of the audio
print('Check Len of Audio:', 661794/22050)

# Trim leading and trailing silence from an audio signal (silence before and after the actual audio)
audio_file, _ = librosa.effects.trim(y)
# the result is an numpy ndarray
print('Audio File:', audio_file, '\n')
print('Audio File shape:', np.shape(audio_file))

from xgboost import XGBClassifier, XGBRFClassifier
from xgboost import plot_tree, plot_importance
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report

from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, roc_curve
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE

#Reading in the Data

#Now let's try to predict the Genre of the audio using Machine Learning techniques.

data = pd.read_csv(r"/content/drive/MyDrive/Music GTZAN/ Music GTZAN/features_3_sec.csv")
data.head()

data.shape

data = pd.read_csv(f'/content/drive/MyDrive/Music GTZAN/ Music GTZAN/features_3_sec.csv')
data = data.iloc[0:, 1:] 
data.head()

y = data['label'] # genre variable.
X = data.loc[:, data.columns != 'label'] #select all columns but not the labels

#### NORMALIZE X ####

# Normalize so everything is on the same scale. 

cols = X.columns
min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(X)

# new data frame with the new scaled data. 
X = pd.DataFrame(np_scaled, columns = cols)

#Splitting the data into training and testing

#70% - 30% split

from sklearn.preprocessing import StandardScaler
fit = StandardScaler()
X = fit.fit_transform(np.array(data.iloc[:, :-1],dtype =float))

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

len(X_train),len(X_test),len(y_train),len(y_test)

#*XGBoost CLASSIFIER - 90% accuracy eXtreme gradient boosting

#create the final model

#compute confusion matrix

#from sklearn.metrics import roc_auc_score, accuracy_score,roc_curve, precision_recall_curve, auc, confusion_matrix
#from xgboost import XGBClassifier, XGBRFClassifier
#estimators=[300, 500, 1000]
#for x in estimators:    
   # for i in range (3,7):
        #xgb = XGBClassifier(n_estimators=x, max_depth=i, n_jobs=-1)
        #xgb.fit(X_train, y_train)
        #preds = xgb.predict(X_test)
       # print('Accuracy', ':', round(accuracy_score(y_test, preds), 5), '\n','estimators: ',x,'\n','maxdepth: ', i)

xgbc = XGBClassifier()
xgbc.fit(X_train, y_train)

score = xgbc.score(X_train, y_train)
print("Train score: ",score)

cv_score = cross_val_score(xgbc, X_train, y_train, cv=10)
print("CV mean score:", cv_score.mean()) #cross validation is used to determine the skill of the data

xgb = XGBClassifier(n_estimators=1000, max_depth=6, n_jobs=-1)
xgb = XGBClassifier()
xgb.fit(X_train,y_train)
preds = xgb.predict(X_test)
print('Accuracy', ':', round(accuracy_score(y_test, preds), 5))

ypred = xgbc.predict(X_test)

cm = confusion_matrix(y_test, ypred)#a confusion matrix is an n*n matrix used for evaluating the performance of the classsfication model
#the matrix compares the actual traget values with those predicted by the machine learning model
print(cm)

cr = classification_report(y_test, ypred) # it gives precision,recall,f1-score,support
#precision-what percent of your predictions were correct?
#recall-what percent of the positive cases did you catch?
#f1 score- what percent of positive predictions were correct?
#support-whether training data is imbalanced or not?
print(cr)

import seaborn as sns
import matplotlib.pyplot as plt

confusion_matr = confusion_matrix(y_test, preds) 
fig1=plt.figure(figsize = (16, 9))
plt.title("Not Normalized Confusion Matrix")
xticklabels = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
yticklabels=["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
sns.heatmap(confusion_matr, cmap="Blues", annot=True, xticklabels=xticklabels,yticklabels=yticklabels);
p1=plt.savefig("confusion matrix")
fig2=plt.figure(figsize=(16,9))
plt.title("Normalized Confusion Matrix")
sns.heatmap(confusion_matr/confusion_matr.sum(axis=1), annot=True,xticklabels=xticklabels,yticklabels=yticklabels)
p2=plt.savefig("normalized confusion matrix")