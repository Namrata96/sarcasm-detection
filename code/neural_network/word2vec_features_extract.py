#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 23:08:17 2017

@author: nam
"""

from gensim.models import Word2Vec as w2v
import gensim
import nltk
import numpy as np
from nltk.corpus import stopwords
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from nltk.corpus import brown
nltk.download('brown')
nltk.download('stopwords')
sentences = brown.sents()
#print sentences
model = gensim.models.KeyedVectors.load_word2vec_format('/home/nam/Downloads/GoogleNews-vectors-negative300.bin', binary=True)
#sentences = Text8Corpus('text8')
#model = gensim.models.Word2Vec(sentences, size=200)

#input_sentences = list()
import re
features_file = open("word_embedding_features.csv", 'w')
for sentence in sentences:
    scores = np.zeros(shape=(len(sentence), len(sentence)), dtype='float32')
    for i, word1 in enumerate(sentence):
#        print word1
        word1 = word1.encode("ascii")
        word1 = re.sub('[^a-zA-Z]',' ',word1)
        word_temp = word1.split()
        if len(word_temp) > 1:
            word1 = word_temp[0]
            
        flag = 0
        for c in word1:
            if c == ' ':
                flag = 1
                break
        if(flag):
            continue
        
        if word1.lower() in set(stopwords.words('english')) or word1 not in model:
            continue
        
        for j, word2 in enumerate(sentence):
            word2 = word2.encode("ascii")
            word2 = re.sub('[^a-zA-Z]',' ',word2)
            word_temp = word2.split()
            if len(word_temp) > 1: 
                word2 = word_temp[0]
            
            flag = 0
            for c in word2:
                if c == ' ':
                    flag = 1
                    break
            if(flag):
                continue
            
            if word2.lower() in set(stopwords.words('english')) or word2 not in model:
                continue
            word2 = re.sub('[^a-zA-Z]',' ',word2)
            if word1 == word2:
                scores[i][j] = np.NaN
            else:
                print str(word1) + " " + str(word2)
                scores[i][j] = model.similarity(word1, word2)
#                print scores[i][j] 
#                print model.similarity(word1, word2)
    print "129393939"           
    max_similar = max(np.nanmax(scores, axis=1))
    print str(max_similar)
    min_similar = min(np.nanmax(scores, axis=1))
    max_dissimilar = min(np.nanmin(scores, axis=1))
    min_dissimilar = max(np.nanmin(scores, axis=1))
    
    features_file.write(str(max_similar) + " " + str(min_similar) + " " + str(max_dissimilar) + " " + str(min_dissimilar) + "\n")
features_file.close()
    
# print model.similarity("dad", "mom")
