#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:45:46 2020

@author: yousuf
"""
import sqlite3
from sqlite3 import Error
from twython import Twython
from time import sleep,time
from datetime import datetime
from tqdm import tqdm
import pandas as pd
from pandas import read_sql
import re
import pycountry
DB_PATH='/home/yousuf/Downloads/twitter_api/twitter_api/'
DB_NAME='twitter'

ACCESS_TOKEN="407011412-54PkRF8mmKa7tpheK5nGBBgML6iy5t1FapNnZra3"
ACCESS_TOKEN_SECRET="Sq2BYln4kFCDask9NQhUues29Pq9mwUi6JrIuX3O5j3eA"
API_KEY="raAdamXVlnxMd9JW4hiRFvu66"
API_SECRET_KEY="BjJsbrz1YpT0fp1r1Zwp27k1FUbkDD8cd9Fs7jnXzIsReYdtVR"
page=0

start=time()
#twitter = Twython(
#API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
#)
conn=sqlite3.connect(DB_PATH+DB_NAME)

followers=read_sql('select * from followers',con=conn,index_col=['id'])
followers['followers_count']=followers['followers_count'].astype(int)
followers['created_at']=followers['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
followers['inserted_at']=followers['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
followers['created_date_md']=followers['created_at'].apply(lambda x: int(((datetime.now()-x).days)/365))
followers_df = (followers.groupby('created_date_md', as_index=False)
       .agg({'id_str':'count'})).reset_index(drop=True)

conn.close()

locations=list(followers['location'].unique())

locations_eng=[re.sub(r'[^a-zA-Z0-9 ]',r'',x) for x in locations]
loc=[]
country_df=pd.DataFrame(columns=['country','count'])
locations_eng=[x.strip() for x in locations_eng]
locations_eng=list(set(locations_eng))
for i in tqdm(locations_eng,total=len(locations_eng)):
    for j in i.strip().split(" "):
        loc.append(j.lower())
countries=[]
for i in tqdm(loc[0:50],total=len(loc[0:50])):
        try:
            s=pycountry.countries.search_fuzzy(j.lower()).name
#            country_df=country_df.append({"country":s, 
#                        "count":0},ignore_index=True)
            countries.append(s)
        except:
            continue

#locations_ind=[]
#for i in enumerate(locations_eng):
#    if i[1]=='':
#        locations_ind.append(i[0])
#a_series = pd.Series(locations)
#locations_arabic = a_series[locations_ind]
#locations_arabic = list(locations_arabic)
#locations_arabic_translated=[]
#
#from googletrans import Translator
#translator = Translator()
#
#for i in tqdm(locations_arabic,total=len(locations_arabic)):
#    try:
#        s=translator.translate(i)
#        if s.text!='':
#            locations_arabic_translated.append(s.text)
#        else:
#            locations_arabic_translated.append(i)
#    except:
#        locations_arabic_translated.append(i)
















