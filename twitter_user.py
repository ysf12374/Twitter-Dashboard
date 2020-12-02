#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 17:03:42 2020

@author: yousuf
"""
"""
CREATE TABLE `followers` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`created_at`	TEXT,
	`inserted_at`	TEXT,
	`description`	TEXT,
	`favourites_count`	TEXT,
	`followers_count`	TEXT,
	`friends_count`	TEXT,
	`id_str`	TEXT,
	`lang`	TEXT,
	`location`	TEXT,
	`name`	TEXT,
	`profile_image_url_https`	TEXT,
	`protected`	TEXT,
	`screen_name`	TEXT,
	`status_text`	TEXT,
	`statuses_count`	TEXT,
	`verified`	TEXT,
	`time_zone`	TEXT,
	`url`	TEXT
);
"""

import sqlite3
from sqlite3 import Error
from twython import Twython
from time import sleep,time
from datetime import datetime
from tqdm import tqdm

DB_PATH='/home/yousuf/Downloads/twitter_api/twitter_api/'
DB_NAME='twitter_tweets'

ACCESS_TOKEN="407011412-54PkRF8mmKa7tpheK5nGBBgML6iy5t1FapNnZra3"
ACCESS_TOKEN_SECRET="Sq2BYln4kFCDask9NQhUues29Pq9mwUi6JrIuX3O5j3eA"
API_KEY="raAdamXVlnxMd9JW4hiRFvu66"
API_SECRET_KEY="BjJsbrz1YpT0fp1r1Zwp27k1FUbkDD8cd9Fs7jnXzIsReYdtVR"
page=0
SEARCH_FOR='UChicago'
start=time()
twitter = Twython(
API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
conn=sqlite3.connect(DB_PATH+DB_NAME)
#user=twitter.lookup_user(screen_name='_KSU')

while True:
    print(f"[SEARCHING]: {SEARCH_FOR}")
    followers=twitter.lookup_user(screen_name=f'{SEARCH_FOR}')
    if len(followers)>0:
        print(f"[FOUND]: {SEARCH_FOR}")
        i=followers[0]
        inserted_at=str(datetime.now())
        created_at=i.get('created_at','None')
        listed_count=i.get('listed_count','None')        
        description=i.get('description','None').replace('"','')
        favourites_count=i.get('favourites_count','None')
        followers_count=i.get('followers_count','None')
        friends_count=i.get('friends_count','None')
        id_str=i.get('id_str','None')
        lang=i.get('lang','None')
        location=i.get('location','None').replace('"','')
        name=i.get('name','None').replace('"','')
        profile_image_url_https=i.get('profile_image_url_https','None')
        protected=i.get('protected','None')
        screen_name=i.get('screen_name','None')
        status_text=i.get('status',None)
        if status_text:
            status_text=i['status']['text'].replace('"','')
        else:
            status_text='None'
        statuses_count=i.get('statuses_count','None')
        verified=i.get('verified','None')
        time_zone=i.get('time_zone','None')
        url=i.get('url','None')
        sql=f"INSERT INTO `users_`(created_at,inserted_at,description"\
        ",favourites_count,followers_count,friends_count"\
        ",id_str,lang,location,name,profile_image_url_https,protected,screen_name,status_text,"\
        "statuses_count,verified,time_zone,url,listed_count) "\
        f""" VALUES('{created_at}','{inserted_at}',"{description}",'{favourites_count}','{followers_count}' """\
        f""",'{friends_count}','{id_str}','{lang}',"{location}","{name}",'{profile_image_url_https}' """\
        f""" ,'{protected}','{screen_name}',"{status_text}",'{statuses_count}','{verified}','{time_zone}','{url}','{listed_count}')  """
        conn.execute(sql)
        conn.commit()
        break
    break
#    print("[SLEEPING]: 15 Minutes")
#    sleep(920)

    


conn.close()




































