import math
import numpy as np
import csv
from keras.models import Sequential
from keras.layers import Dense
import random
import math
from sklearn.metrics import precision_recall_curve
from keras.models import model_from_json
import h5py
import os
import glob
def read_input():
    A = [];
    b = [];
    with open('/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/nonsarcasm_final_features.csv', 'rb') as csvfile:
        file = csv.reader(csvfile, delimiter=',', quotechar='|')
        init = 1
        for row in file:
            if(init == 1):
                init = 0
                continue
            print row
            temp = [float(i) for i in row]
            print temp
            A.append(temp[0:18])
            b.append(0)


    with open('/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/sarcasm_final_features.csv', 'rb') as csvfile:
        file = csv.reader(csvfile, delimiter=',', quotechar='|')
        init = 1
        for row in file:
            if(init == 1):
                init = 0
                continue
            print row
            temp = [float(i) for i in row]
            A.append(temp[0:18])
            b.append(1)
    A = np.asarray(A)
    b = np.asarray(b)

    D = np.c_[A, b]
    np.random.shuffle(D)
    X = D[:,0:18]
    y = D[:,18]
    return X,y


n_input = 18

[X_test,Y_test] = read_input()
# print("input read")

json_file = open('/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/data/sarcasm_model.json', 'r') # load json and create model
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/data/sarcasm_model.h5") # load weights into new model
print("Loaded model from disk")
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
scores = loaded_model.evaluate(X_test, Y_test)
test_classes = loaded_model.predict_classes(X_test)


p_label = test_classes
p_actual = Y_test
tp,fp,tn,fn=0.0,0.0,0.0,0.0
for predicted,actual in zip(p_label,p_actual):
    if(predicted==actual and predicted==1): tp+=1
    elif(predicted==actual and predicted==0):tn+=1
    elif(predicted==0):fn+=1
    else:fp+=1

precision = float(tp)/(tp+fp)
recall = float(tp)/(tp+fn)
fscore = 2*precision*recall/(precision+recall)

print "\n"
print "precision: ",precision
print "recall: ",recall
print "f-measure",fscore

print "accuracy",scores[1]


