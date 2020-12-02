#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 16:30:39 2020

@author: yousuf
"""

import sqlite3
from sqlite3 import Error
from twython import Twython
from time import sleep,time
from datetime import datetime
from tqdm import tqdm
from pandas import read_sql
from pandas.api.types import CategoricalDtype
sorter = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
sorterIndex = dict(zip(sorter,range(len(sorter))))

DB_PATH='/home/yousuf/Downloads/twitter_api/twitter_api/'
DB_NAME='twitter_tweets'

ACCESS_TOKEN="407011412-54PkRF8mmKa7tpheK5nGBBgML6iy5t1FapNnZra3"
ACCESS_TOKEN_SECRET="Sq2BYln4kFCDask9NQhUues29Pq9mwUi6JrIuX3O5j3eA"
API_KEY="raAdamXVlnxMd9JW4hiRFvu66"
API_SECRET_KEY="BjJsbrz1YpT0fp1r1Zwp27k1FUbkDD8cd9Fs7jnXzIsReYdtVR"
page=0

start=time()
#twitter = Twython(
#API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
#)
SEARCH_FOR="_KSU"
SEARCH_FOR_ID='18916965'

conn=sqlite3.connect(DB_PATH+DB_NAME)

users=read_sql('select * from users_',con=conn,index_col=['id'])

ksu_tweets=read_sql('select * from tweets where name is NULL',con=conn,index_col=['id'])
ksu_influencers=read_sql('select * from influencers where to_screen_name="{SEARCH_FOR}"',con=conn,index_col=['id'])
to_id_str='{SEACH_OR_ID}'
ksu_retweets=read_sql(f'select * from influencers where to_id_str="{to_id_str}" and to_screen_name="{SEARCH_FOR}" ',con=conn,index_col=['id'])
ksu_mentions=read_sql(f'select * from influencers where to_id_str!="{to_id_str}" and to_screen_name="{SEARCH_FOR}"',con=conn,index_col=['id'])

comparing_ids=list(users['screen_name'].unique())
comparing_ids=[x for x in comparing_ids if x!='_KSU']

ksu_tweets['retweet_count']=ksu_tweets['retweet_count'].astype(int)
ksu_tweets['created_at']=ksu_tweets['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
ksu_tweets['inserted_at']=ksu_tweets['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
ksu_tweets['created_date_md']=ksu_tweets['created_at'].apply(lambda x:  str(x.strftime('%A')))
ksu_tweets_df = (ksu_tweets.groupby('created_date_md', as_index=False)
         .agg({'id_str':'count', 'retweet_count':'mean'})).reset_index(drop=True)

ksu_tweets_df['Day_id'] = ksu_tweets_df['created_date_md'].map(sorterIndex)
ksu_tweets_df=ksu_tweets_df.sort_values('Day_id')

ksu_val=list(ksu_tweets_df['id_str'].values)
ksu_rt_val=list(ksu_tweets_df['retweet_count'].values)

to_id_str='{SEACH_OR_ID}'
kauweb_vals=[]
IMSIU_edu_sa_val=[]
kkueduksa_val=[]
EdinburghUni_val=[]
OfficialUoM_val=[]
Harvard_val=[]
UChicago_val=[]

kauweb_rt_vals=[]
IMSIU_edu_sa_rt_val=[]
kkueduksa_rt_val=[]
EdinburghUni_rt_val=[]
OfficialUoM_rt_val=[]
Harvard_rt_val=[]
UChicago_rt_val=[]

for i in comparing_ids:
    SEARCH_FOR=str(i)
    tweets=read_sql(f'select * from tweets where name="{SEARCH_FOR}"',con=conn,index_col=['id'])
    influencers=read_sql('select * from influencers where to_screen_name="{SEARCH_FOR}"',con=conn,index_col=['id'])
    retweets=read_sql(f'select * from influencers where to_id_str="{to_id_str}" and to_screen_name="{SEARCH_FOR}" ',con=conn,index_col=['id'])
    mentions=read_sql(f'select * from influencers where to_id_str!="{to_id_str}" and to_screen_name="{SEARCH_FOR}"',con=conn,index_col=['id'])
    tweets['retweet_count']=tweets['retweet_count'].astype(int)
    tweets['created_at']=tweets['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
    tweets['inserted_at']=tweets['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
    tweets['created_date_md']=tweets['created_at'].apply(lambda x:  str(x.strftime('%A')))
    tweets_df = (tweets.groupby('created_date_md', as_index=False)
             .agg({'id_str':'count', 'retweet_count':'mean'})).reset_index(drop=True)
    tweets_df['Day_id'] = tweets_df['created_date_md'].map(sorterIndex)
    tweets_df=tweets_df.sort_values('Day_id')    
    if i=='kauweb':
        kauweb_vals=list(tweets_df['id_str'].values)
        kauweb_rt_vals=list(tweets_df['retweet_count'].values)
    elif i=='IMSIU_edu_sa':
        IMSIU_edu_sa_val=list(tweets_df['id_str'].values)
        IMSIU_edu_sa_rt_val=list(tweets_df['retweet_count'].values)
    elif i=='kkueduksa':
        kkueduksa_val=list(tweets_df['id_str'].values)
        kkueduksa_rt_val=list(tweets_df['retweet_count'].values)
    elif i=='EdinburghUni':
        EdinburghUni_val=list(tweets_df['id_str'].values)
        EdinburghUni_rt_val=list(tweets_df['retweet_count'].values)
    elif i=='OfficialUoM':
        OfficialUoM_val=list(tweets_df['id_str'].values)
        OfficialUoM_rt_val=list(tweets_df['retweet_count'].values)
    elif i=='Harvard':
        Harvard_val=list(tweets_df['id_str'].values)
        Harvard_rt_val=list(tweets_df['retweet_count'].values)
    elif i=='UChicago':
        UChicago_val=list(tweets_df['id_str'].values)
        UChicago_rt_val=list(tweets_df['retweet_count'].values)




sentiment=read_sql('select * from tweets where name is null',con=conn,index_col=['id'])

pos=len(sentiment[sentiment['sentiment']=='Positive'])
neg=len(sentiment[sentiment['sentiment']=='Negative'])
neu=len(sentiment[sentiment['sentiment']=='Neutral'])





users_unique = users.drop_duplicates('id_str')


























conn.close()


