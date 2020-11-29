# Generate primary first level features
# (+ve word count) (-ve word count) (overall polarity) (times change in pol) (largest + cont) (largest - cont) (capital letters) (punctuation)
import re,csv
import codecs
f3 = codecs.open('/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/data/sarcasm_tweets.txt', encoding='utf-8')
csvfile = open('/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/data/sarcasm_gen_features.csv','wb')
csvwriter =csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
# print('(+ve word count) (-ve word count) (overall polarity) (times change in pol) (largest + cont) (largest - cont) (capital letters) (punctuation)')
csvwriter.writerow(['(+ve word count) ','(-ve word count)' ,'(overall polarity)' ,'(times change in pol)' ,'(largest + cont)' ,'(largest - cont)' ,'(capital letters)' ,'(punctuation)'])
f2 = open('/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/data/sarcasm_tweets_clean.txt')

pattern=re.compile(r'\[(\-?[0-9])\]')
capital_count=[]
punctuation_count=[]
q=0
for l in f3 :

    punctuation_count.append(l.count('!')+l.count('?'))
    for x in range(len(l)-2):
        if l[x]=='.' and l[x+2]=='.':
            punctuation_count[-1]=punctuation_count[-1]+1

# print len(punctuation_count)
for l,inde in zip(f2,range(len(punctuation_count))):
    t= l.split(' ')
    ls=[]
    for x in t :
        try:
            ls.append(int(pattern.findall(x)[0]))
        except:
            continue
    pc,nc=0,0
    lsp,lsn=[],[]

    lsp = list(filter(lambda(x):x>0 , ls ))
    lsn= list(filter(lambda(x):x<0 , ls ))

    change_pol,prev=0,0
    for x in ls :
        if(x==0):
            continue
        if(prev==0 and x>0):prev=1
        elif(prev==0 and x<0):prev=-1
        elif(x>0 and prev<0 or x<0 and prev>0):
            change_pol=change_pol+1
            prev=-1*prev


    neg_max,pos_max=0,0
    cur=0
    prev=0
    for x in ls :
        if(x==0):
            continue
        if(prev==0 and x>0):
            prev=1
            cur=1
        elif(prev == 0 and x<0):
            prev = -1
            cur = 1
        elif(x>0 and prev>0 or x<0 and prev<0):cur=cur+1
        elif(x>0 and prev<0 or x<0 and prev>0):
            if(prev<0):neg_max=max(neg_max,cur)
            else:pos_max=max(pos_max,cur)
            prev= -1*prev
            cur=1
    else:
        if(prev<0):neg_max=max(neg_max,cur)
        elif(prev>0):pos_max=max(pos_max,cur)


    capital_count.append(sum(list(map(lambda x : x.isupper(),list(l))))-l.count('NAME')*4 - l.count('HYPERLINK')*9)

    
    try:
        q+=1
        csvwriter.writerow([len(lsp),len(lsn),sum(lsp)+sum(lsn),change_pol,pos_max,neg_max,capital_count[-1],punctuation_count[inde]])
    except Exception as e:
        pass
    
csvfile.close()
#sentences = Text8Corpus('text8')
#model = gensim.models.Word2Vec(sentences, size=200)
from gensim.models import Word2Vec as w2v
import gensim
import nltk
import numpy as np
from nltk.corpus import stopwords
import logging
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#input_sentences = list()
model = gensim.models.KeyedVectors.load_word2vec_format('/home/nam/Downloads/GoogleNews-vectors-negative300.bin', binary=True)

features_file = open("sarcasm_word_embedding_features.csv", 'w')
csvwriter = csv.writer(features_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
csvwriter.writerow(['(max_similar) ','(min_similar)' ,'(max_dissimilar)' ,'(min_dissimilar)','(wmax_similar) ','(wmin_similar)' ,'(wmax_dissimilar)' ,'(wmin_dissimilar)'])

# Cleaning the tweets and appending in the corpus list
corpus = []
tweets = codecs.open('/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/data/sarcasm_tweets.txt', encoding='UTF-8')
# Counting total number of distinct words (including stop words)
for tweet in tweets:
    # Converting everything to lower case
    tweet = tweet.lower()
    # Removing hyperlinks and name
    tweet = re.sub('hyperlink', ' ', tweet)
    tweet = re.sub('name', ' ', tweet)
    # Removing special characters etc
    tweet = re.sub('[^a-zA-Z]',' ',tweet)
    
    tweet = tweet.split() # Splits the string into list of words separated by space
    tweet = [word for word in tweet if not word in set(stopwords.words('english'))]
#        print str(tweet)
    # Stemming 
    ps = PorterStemmer()
    tweet = [ps.stem(word) for word in tweet]
    tweet = ' '.join(tweet)
    corpus.append(tweet)
    

# Calculating the features
for sen_index, sentence in enumerate(corpus):
    sentence = sentence.split()
    if len(sentence)==0 or len(sentence)==1:
        csvwriter.writerow([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        continue
    scores = np.zeros(shape=(len(sentence), len(sentence)), dtype='float32')
    wscores = np.zeros(shape=(len(sentence), len(sentence)), dtype='float32')
#    print sentence
    for i, word1 in enumerate(sentence):
#        
        if word1 not in model:
            continue
        for j, word2 in enumerate(sentence):
#            
            if word2 not in model:
                continue
#            word2 = re.sub('[^a-zA-Z]',' ',word2)
            if word1 == word2:
                scores[i][j] = np.NaN
            else:
#                print str(word1) + " " + str(word2)
                scores[i][j] = model.similarity(word1, word2)
                wscores[i][j] = model.similarity(word1, word2)/((j-i)*(j-i))
#                print scores[i][j] 
#                print model.similarity(word1, word2)

    print "sentence done: " + str(sen_index)       
    max_similar = max(np.nanmax(scores, axis=1))
    min_similar = min(np.nanmax(scores, axis=1))
    max_dissimilar = min(np.nanmin(scores, axis=1))
    min_dissimilar = max(np.nanmin(scores, axis=1))
    wmax_similar = max(np.nanmax(wscores, axis=1))
    wmin_similar = min(np.nanmax(wscores, axis=1))
    wmax_dissimilar = min(np.nanmin(wscores, axis=1))
    wmin_dissimilar = max(np.nanmin(wscores, axis=1))
    
    csvwriter.writerow([max_similar,min_similar,max_dissimilar,min_dissimilar,wmax_similar,wmin_similar,wmax_dissimilar,wmin_dissimilar])
features_file.close()

csvfile.close()