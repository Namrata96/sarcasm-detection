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
    with open('/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/data/nonsarcasm_final_features.csv', 'rb') as csvfile:
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


    with open('/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/data/sarcasm_final_features.csv', 'rb') as csvfile:
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

[A,b] = read_input()
# print("input read")

num_rows, num_cols = A.shape
n_train = int(num_rows*0.95)
X = A[0:n_train,:]
Y = b[0:n_train]

X_valid = A[n_train:num_rows,:]
Y_valid = b[n_train:num_rows]
# print("data processed")


n_input = 18
n1=5
n2=1
from keras.callbacks import ModelCheckpoint
model = Sequential()
model.add(Dense(output_dim = n1, input_dim=n_input, init='uniform', activation='relu'))
model.add(Dense(output_dim = n2, init='uniform', activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, nb_epoch=30, batch_size=20, validation_split=0.1, callbacks=[ModelCheckpoint('sarcasm_model.h5', save_best_only=True)])
# serialize model to JSON
model_json = model.to_json()
with open("sarcasm_model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("sarcasm_model.h5")
print("Saved model to disk")
scores = model.evaluate(X_valid, Y_valid)
test_classes = model.predict_classes(X_valid)


p_label = test_classes
p_actual = Y_valid
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

X_test = []
y_test = []
json_file = open('sarcasm_model.json', 'r') # load json and create model
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("sarcasm_model.h5") # load weights into new model
print("Loaded model from disk")

root_dir = '/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/data/data-sarc-sample(1)/data-sarc-sample/'

all_sarc_paths = glob.glob(os.path.join(root_dir, '*/*.txt'))
for sarc in all_sarc_paths:
    print sarc
    fp = open(sarc, 'r')
    X_test.append(fp.read())
    y_test.append(1) # 1 is for sarcasm

X_test = np.array(X_test)
y_test = np.array(y_test)
y_pred = loaded_model.predict_classes(X_test)
print y_pred
