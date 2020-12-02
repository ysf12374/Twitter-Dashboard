#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 14:32:26 2020

@author: yousuf
"""
"""
Access token :407011412-54PkRF8mmKa7tpheK5nGBBgML6iy5t1FapNnZra3
Access token secret :Sq2BYln4kFCDask9NQhUues29Pq9mwUi6JrIuX3O5j3eA
API key:raAdamXVlnxMd9JW4hiRFvu66
API secret key:BjJsbrz1YpT0fp1r1Zwp27k1FUbkDD8cd9Fs7jnXzIsReYdtVR
"""
import sqlite3
from sqlite3 import Error
DB_PATH='/home/yousuf/Downloads/twitter_api/twitter_api/'
DB_NAME='twitter'

conn = sqlite3.connect(DB_PATH+DB_NAME)
#conn.execute('''CREATE TABLE COMPANY
#         (ID INT PRIMARY KEY     NOT NULL,
#         NAME           TEXT    NOT NULL,
#         AGE            INT     NOT NULL,
#         ADDRESS        CHAR(50),
#         SALARY         REAL);''')
#conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");


ACCESS_TOKEN="407011412-54PkRF8mmKa7tpheK5nGBBgML6iy5t1FapNnZra3"
ACCESS_TOKEN_SECRET="Sq2BYln4kFCDask9NQhUues29Pq9mwUi6JrIuX3O5j3eA"
API_KEY="raAdamXVlnxMd9JW4hiRFvu66"
API_SECRET_KEY="BjJsbrz1YpT0fp1r1Zwp27k1FUbkDD8cd9Fs7jnXzIsReYdtVR"

#from TwitterAPI import TwitterAPI
#api = TwitterAPI(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
#for item in r:
#        print(item)


from twython import Twython
from time import sleep,time
APP_KEY = API_KEY
APP_SECRET = API_SECRET_KEY

#twitter = Twython(API_KEY, API_SECRET_KEY)
#
#auth = twitter.get_authentication_tokens(callback_url='https://dev.deepcheck.one:8080/twitter')



oauth_verifier="xT7m69LEEqaNOi5qCAs2IcEbs07ZpkHD"

#
#OAUTH_TOKEN = auth['oauth_token']
#OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
start=time()
twitter = Twython(
API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)


user=twitter.lookup_user(screen_name='_KSU')
remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
remaining_calls=int(remaining_calls)
print(remaining_calls)
if remaining_calls<2:
    rem_time=time.time()-start
    if rem_time<1050:
        sleep(920-int(rem_time))
    else:
        sleep(20)
    start=time()
#final_step = twitter.get_authorized_tokens(oauth_verifier)

ksu=twitter.search(q='(from:_KSU)',f="user",count=100)

remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
remaining_calls=int(remaining_calls)
print(remaining_calls)
if remaining_calls<2:
    rem_time=time.time()-start
    if rem_time<1050:
        sleep(920-int(rem_time))
    else:
        sleep(20)
    start=time()
#ksu_=twitter.show_user(user_id='@_KSU')
#ksu_=twitter.search_users(q='@_KSU')
#results = twitter.cursor(twitter.show_user, q='@_KSU')
#get_retweets
#lookup_user

retweets=twitter.get_retweets(id='1276115476054188032')#tweet id
remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
print(remaining_calls)
remaining_calls=int(remaining_calls)
if remaining_calls<2:
    rem_time=time.time()-start
    if rem_time<1050:
        sleep(920-int(rem_time))
    else:
        sleep(20)
    start=time()
tweets=twitter.get_user_timeline(user_id='18916965',count=200)#user id
remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
remaining_calls=int(remaining_calls)
print(remaining_calls)
if remaining_calls<2:
    rem_time=time.time()-start
    if rem_time<1050:
        sleep(920-int(rem_time))
    else:
        sleep(20)
    start=time()
tweets=twitter.get_user_timeline(user_id='18916965',count=200,include_rts=1)
remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
print(remaining_calls)
remaining_calls=int(remaining_calls)
if remaining_calls<2:
    rem_time=time.time()-start
    if rem_time<1050:
        sleep(920-int(rem_time))
    else:
        sleep(20)
    start=time()
txtx=[x['id'] for x in tweets]
max(txtx)
min(txtx)
tweets1=twitter.get_user_timeline(user_id='18916965',count=200,include_rts=1,max_id=str(min(txtx)))
remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
print(remaining_calls)
remaining_calls=int(remaining_calls)
if remaining_calls<2:
    rem_time=time.time()-start
    if rem_time<1050:
        print("Sleeping for [920] seconds")
        sleep(920-int(rem_time))
    else:
        print("Sleeping for [20] seconds")
        sleep(20)
    start=time()
txtx=[x['id'] for x in tweets]
min(txtx)
txtx=[x['id'] for x in tweets1]
min(txtx)


#
#OAUTH_TOKEN=
#OAUTH_TOKEN_SECRET=
#
#twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)







#import os
#import tweepy as tw
#import pandas as pd
#
#
#
#auth = tw.OAuthHandler(API_KEY, API_SECRET_KEY)
#auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#api = tw.API(auth, wait_on_rate_limit=True)
#search_words = "(from:_KSU)"
#date_since = "2020-05-01"
#until="2020-06-02"
#tweets = tw.Cursor(api.search,
#              q=search_words,
#              lang="en",
#              since_id=date_since).items(5)











