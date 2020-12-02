# coding: utf-8

"""
asa.py is a simple (Arabic) Sentiment Analysis using Word Embeddings.
Author: Aziz Alto
Date: Aug. 2016
"""

import argparse
from logging import info, basicConfig, INFO
# -- 3rd party -- #
import pandas as pd
from gensim.models import KeyedVectors
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import wordpunct_tokenize
# -- classifiers -- #
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegressionCV
from sklearn.svm import LinearSVC, NuSVC
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
import joblib
LOG_HEAD = '[%(asctime)s] %(levelname)s: %(message)s'
basicConfig(format=LOG_HEAD, level=INFO)


class ArSentiment(object):
    def __init__(self, embeddings_file=None, dataset_file=None, plot_roc=False, split=0.9, detailed=False):
        """
        :param embeddings_file: path to the embeddings file.
        :param dataset_file: path to a labeled dataset file.
        :param plot_roc: boolean, plot ROC figure.
        :param split: float, data split fraction i.e. train | test split (default: 90% | 10%)
        :param detailed: boolean, output classifiers' parameters info i.e. name, parameters' value, .. etc.
        """

        self.dataset_file = dataset_file
        self.split = split

        self.embeddings, self.dimension = self.load_vectors(embeddings_file)

        # read dataset
        train, test = self.read_data(self.dataset_file)
        train_txt, test_txt = train['txt'], test['txt']
        self.y_train = train['sentiment']
        self.y_test = test['sentiment']

        # -- dataset preprocessing -- #
        train_tokens = self.tokenize_data(train_txt, 'training')
        test_tokens = self.tokenize_data(test_txt, 'testing')

        # -- vectorize training/testing data -- #
        train_vectors = self.average_feature_vectors(train_tokens, 'training')
        test_vectors = self.average_feature_vectors(test_tokens, 'testing')

        # vectorized features
        self.X_train = self.remove_nan(train_vectors)
        self.X_test = self.remove_nan(test_vectors)

        info('Done loading and vectorizing data.')
        info("--- Sentiment CLASSIFIERS ---")
        info("fitting ... ")

        # classifiers to use
        classifiers = [
#            RandomForestClassifier(n_estimators=100),
#            SGDClassifier(loss='log', penalty='l1'),
            LinearSVC(C=1e1),
#            NuSVC(),
#            LogisticRegressionCV(solver='liblinear'),
#            GaussianNB(),
        ]

        self.accuracies = {}

        # RUN classifiers
        for c in classifiers:
            self.classify(c, detailed, plot_roc)

        avg_f1 = 0
        info('results ...')
        for k, v in self.accuracies.items():
            string = '\tMacAvg. {:.2f}% F1. {:.2f}% P. {:.2f} R. {:.2f} : {}'
            print(string.format(v[0] * 100, v[1] * 100, v[2] * 100, v[3] * 100, k))
            avg_f1 += float(v[1])

        #print('OVERALL avg F1 test {:.2f}%'.format((avg_f1 / len(self.accuracies)) * 100))
        info("DONE!")

    @staticmethod
    def load_vectors(model_name, binary=True):
        """load the pre-trained embedding model"""
        if binary:
            w2v_model = KeyedVectors.load_word2vec_format(model_name, binary=True)
        else:
            w2v_model = KeyedVectors.load(model_name)

        w2v_model.init_sims(replace=True)  # to save memory
        vocab, vector_dim = w2v_model.syn0.shape
        return w2v_model, vector_dim

    def read_data(self, dataset_in):

        dataset = pd.read_csv(dataset_in,index_col=[0])
        # shuffle df
        dataset = dataset.iloc[np.random.permutation(len(dataset))]
        # split train/test
        train_df, test_df = train_test_split(dataset, train_size=self.split)

        string_ = 'dataset {} {}. Split: {} training and {} testing.'
        info(string_.format(dataset_in, dataset.shape, len(train_df), len(test_df)))

        return train_df, test_df

    @staticmethod
    def tokenize(text):
        """
        :param text: a paragraph string
        :return: a list of words
        """

        try:
            try:
                txt = unicode(text, 'utf-8')  # py2
            except NameError:
                txt = text  # py3
            words = wordpunct_tokenize(txt)
            length = len(words)
        except TypeError:
            words, length = ['NA'], 0

        return words, length

    def tokenize_data(self, examples_txt, type_='NaN'):
        tokens = []
        info('Tokenizing the {} dataset ..'.format(type_))
        total_tokens = []
        for txt in examples_txt:
            words, num = self.tokenize(txt)
            tokens.append(words)
            total_tokens.append(num)
        info(' ... total {} {} tokens.'.format(sum(total_tokens), type_))
        return tokens

    def feature(self, words):
        """average words' vectors"""

        feature_vec = np.zeros((self.dimension,), dtype="float32")
        retrieved_words = 0
        for token in words:
            try:
                feature_vec = np.add(feature_vec, self.embeddings[token])
                retrieved_words += 1
            except KeyError:
                pass  # if a word is not in the embeddings' vocabulary discard it

        np.seterr(divide='ignore', invalid='ignore')
        feature_vec = np.divide(feature_vec, retrieved_words)

        return feature_vec

    def average_feature_vectors(self, examples, type_='NaN'):
        """
        :param examples: a list of lists (each list contains words) e.g. [['hi','do'], ['you','see'], ... ]
        :param type_: (optional) type of examples text e.g. train / test
        :return: the average word vector of each list
        """

        feature_vectors = np.zeros((len(examples), self.dimension), dtype="float32")
        info("Vectorizing {} tokens ..".format(type_))
        for i, example in enumerate(examples):
            feature_vectors[i] = self.feature(example)

        info(" ... total {} {}".format(len(feature_vectors), type_))

        return feature_vectors

    def classify(self, classifier=None, info_=False, plot_roc=False):

        classifier_name = classifier.__class__.__name__

        if info_:
            info('fitting data ...')
            info('\n\ncreated \n\n{}'.format(classifier))

        classifier.fit(self.X_train, self.y_train)
        pscore = classifier.score(self.X_test, self.y_test)

        if info_:
            info('\n\n\t{}() ACCURACY: {}\n'.format(classifier_name, pscore))

        # F1 score
        y_pred = classifier.predict(self.X_test)
        f1_score = metrics.f1_score(self.y_test, y_pred)

        # macro accuracy (macro average)
        macc = metrics.f1_score(self.y_test, y_pred, pos_label=None, average='macro')

        # precision and recall
        recall = metrics.recall_score(self.y_test, y_pred)
        precision = metrics.precision_score(self.y_test, y_pred)

        results = [macc, f1_score, precision, recall]
        self.accuracies[classifier_name] = results
        
        # prediction
        negative = len(classifier.predict(self.X_test)[classifier.predict(self.X_test) == 0])
        positive = len(classifier.predict(self.X_test)[classifier.predict(self.X_test) == 1])
        
        
        filename = 'finalized_model.sav'
        joblib.dump(classifier, filename)
 
        ## some time later...
 
        ## load the model from disk
#        loaded_model = joblib.load(filename)
        if plot_roc:
            info('plotting roc of ... {}'.format(classifier_name))
            self.plot_auc(classifier, classifier_name, negative, positive)

    def plot_auc(self, estimator, estimator_name, neg, pos):
        try:
            classifier_probas = estimator.decision_function(self.X_test)
        except AttributeError:
            classifier_probas = estimator.predict_proba(self.X_test)[:, 1]

        false_positive_r, true_positive_r, thresholds = metrics.roc_curve(self.y_test, classifier_probas)
        roc_auc = metrics.auc(false_positive_r, true_positive_r)

        label = '{:.1f}% neg:{} pos:{} {}'.format(roc_auc * 100, neg, pos, estimator_name)
        plt.plot(false_positive_r, true_positive_r, label=label)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([-0.05, 1.0])
        plt.ylim([0.0, 1.05])
        plt.title('ROC score(s)')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.legend(loc='lower right', prop={'size': 10})
        plt.savefig("ROC.png", dpi=300, bbox_inches='tight')
        plt.grid()

    @staticmethod
    def remove_nan(x):
        """remove NaN values from data vectors"""
        imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
        x_clean = imp.fit_transform(x)
        return x_clean


#if __name__ == "__main__":
##    parser = argparse.ArgumentParser()
##    parser.add_argument("--vectors", help="path a pre-trained vectors model.")
##    parser.add_argument("--dataset", help="path a labeled (0/1) sentiment dataset.")
##
##    args = parser.parse_args()
##    vec = args.vectors
#
#    # vectors file
#    embeddings_path = "./arabic-news.bin"#args.vectors if args.vectors else "embeddings/arabic-news.bin"
#    # dataset file
#    dataset_path = "./mpqa-ar.csv"#args.dataset if args.dataset else "datasets/mpqa-ar.csv"
#    import pandas as pd
#    df=pd.read_csv("./mpqa-ar.csv")
#    
#    train_neg=pd.read_csv("./arabic tweets/train_Arabic_tweets_negative_20190413.tsv",sep='\t',header=None)
#    train_pos=pd.read_csv("./arabic tweets/train_Arabic_tweets_positive_20190413.tsv",sep='\t',header=None)
#    train=train_neg.append(train_pos)
#    train.columns=['sentiment','txt']
#    train['sentiment']=train['sentiment'].apply(lambda x: 0 if x=='neg' else 1)
#    train.to_csv('train_arabic_sentiment.csv',index=[0])
#    # run
#    ArSentiment(embeddings_path, './train_arabic_sentiment.csv', plot_roc=False)

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
def sent(tst):
#    tst="المهم هو الصادق معي الناصح لي"
    global w2v_model,loaded_model
    tst_=tst.split(" ")
    v2 = [w2v_model.wv[word] for word in tst_ if word in w2v_model.wv.vocab]
    if len(v2)>0:
        v2=np.asarray(v2)
        result=loaded_model.predict(v2)
        result_len=len(result)
        positive=list(result).count(1)
        negative=list(result).count(0)

        if (negative/result_len)*100 >73.5:
            result='Negative'
        else:
            if (positive/result_len)*100 >60:
                result='Positive'
            else:
                result='Neutral'
    else:
        result='Neutral'
    return result


import sqlite3
from sqlite3 import Error
from twython import Twython
from time import sleep,time
from datetime import datetime
from tqdm import tqdm
import pandas as pd
from pandas import read_sql
DB_PATH='/home/yousuf/Downloads/twitter_api/twitter_api/'
DB_NAME='twitter_tweets'
ACCESS_TOKEN="407011412-54PkRF8mmKa7tpheK5nGBBgML6iy5t1FapNnZra3"
ACCESS_TOKEN_SECRET="Sq2BYln4kFCDask9NQhUues29Pq9mwUi6JrIuX3O5j3eA"
API_KEY="raAdamXVlnxMd9JW4hiRFvu66"
API_SECRET_KEY="BjJsbrz1YpT0fp1r1Zwp27k1FUbkDD8cd9Fs7jnXzIsReYdtVR"

SEARCH_FOR='_KSU'
SEARCH_FOR_ID='18916965'
conn=sqlite3.connect(DB_PATH+DB_NAME)

tweets=read_sql('select * from tweets',con=conn)
for i in tqdm(tweets[['id','text']].itertuples(),total=len(tweets['id_str'])):
    result=sent(str(i[2]).replace("'","").replace('"',''))
    sql=f"UPDATE tweets SET sentiment = '{result}' WHERE id = {i[1]};"

    conn.execute(sql)
    conn.commit()


conn.close()
