#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 00:37:57 2020

@author: yousuf
"""
import json
from gensim.models import Word2Vec
from numpy import dot,asarray
import numpy as np
from gensim.matutils import unitvec
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity
from  numpy import array 
import joblib
import nltk
from gensim.models import KeyedVectors
nltk.download('stopwords')
from nltk.corpus import stopwords   
model_name='./arabic-news.bin'
w2v_model = KeyedVectors.load_word2vec_format(model_name, binary=True)






filename="finalized_model.sav"
loaded_model = joblib.load(filename)

tst="المهم هو الصادق معي الناصح لي"
tst_=tst.split(" ")
v2 = [w2v_model.wv[word] for word in tst_ if word in w2v_model.wv.vocab]
v2=np.asarray(v2)
result=loaded_model.predict(v2)
