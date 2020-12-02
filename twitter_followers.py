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
from pandas import read_sql
# Twitter Database class for reading and executing queries onto the db
class DB_Twitter:
    def __init__(self,db_name,db_path):
        self.db_name=db_name
        self.db_path=db_path
    def open_con(self):
        try:
            self.conn=sqlite3.connect(self.db_path+self.db_name)
        except Error as e:
            print(e)
    def command(self,text):
        self.conn.execute(text)
    def command_w_commit(self,text):
        self.conn.execute(text)
        self.conn.commit()
    def close_w_commit(self):
        self.conn.commit()
        self.conn.close()
    def close(self):
        self.conn.close()

#change the path to the db
DB_PATH='/home/yousuf/Downloads/twitter_api/twitter_api/'
DB_NAME='twitter'
#change the twitter api details
ACCESS_TOKEN="407011412-54PkRF8mmKa7tpheK5nGBBgML6iy5t1FapNnZra3"
ACCESS_TOKEN_SECRET="Sq2BYln4kFCDask9NQhUues29Pq9mwUi6JrIuX3O5j3eA"
API_KEY="raAdamXVlnxMd9JW4hiRFvu66"
API_SECRET_KEY="BjJsbrz1YpT0fp1r1Zwp27k1FUbkDD8cd9Fs7jnXzIsReYdtVR"
page=0

start=time()
# Initiating a Tython twitter api class
twitter = Twython(
API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
# Searching for followers 
followers=twitter.get_followers_list(screen_name='_KSU',count=200)
page+=1
length_followers=len(followers['users'])

# Check remaining calls and sleep if the api is exhausted
remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
remaining_calls=int(remaining_calls)

if remaining_calls<2:
    print(remaining_calls)
    rem_time=time()-start
    if rem_time<1050:
        print(f"Sleeping for [{920-int(rem_time)}] seconds")
        sleep(920-int(rem_time))
    else:
        print("Sleeping for [20] seconds")
        sleep(20)
    start=time()

cursor_followers=followers['next_cursor_str']
#twt=DB_Twitter(DB_NAME,DB_PATH)
#twt.open_con()
# Insert query for all the followers
conn=sqlite3.connect(DB_PATH+DB_NAME)
for i in tqdm(followers['users'],total=len(followers['users'])):
    inserted_at=str(datetime.now())
    created_at=i.get('created_at','None')
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
    
#    check_sql=f"""select id_str from followers where id_str='{id_str}' """
#    check_df=read_sql(check_sql,con=conn)
#    if len(check_df)>0:
#        sql=f""" UPDATE followers SET followers_count = '{followers_count}', """\
#        f""" friends_count='{friends_count}', statuses_count='{statuses_count}', """\
#        f""" favourites_count='{favourites_count}', description="{description}"; """
    sql=f"INSERT INTO `followers`(created_at,inserted_at,description"\
    ",favourites_count,followers_count,friends_count"\
    ",id_str,lang,location,name,profile_image_url_https,protected,screen_name,status_text,"\
    "statuses_count,verified,time_zone,url) "\
    f""" VALUES('{created_at}','{inserted_at}',"{description}",'{favourites_count}','{followers_count}' """\
    f""",'{friends_count}','{id_str}','{lang}',"{location}","{name}",'{profile_image_url_https}' """\
    f""" ,'{protected}','{screen_name}',"{status_text}",'{statuses_count}','{verified}','{time_zone}','{url}')  """
    conn.execute(sql)
    conn.commit()


# Loop for getting all the followers in series
while True:
    followers=twitter.get_followers_list(screen_name='_KSU',count=200,cursor=cursor_followers)
    page+=1
    length_followers=len(followers['users'])
    if length_followers<1:
        break
    remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
    remaining_calls=int(remaining_calls)
    
    if remaining_calls<2:
        print(remaining_calls)
        rem_time=time()-start
        if rem_time<1050:
            print(f"Sleeping for [{920-int(rem_time)}] seconds")
            sleep(920-int(rem_time))
        else:
            print(f"Sleeping for [20] seconds")
            sleep(20)
        start=time()
    
    cursor_followers=followers['next_cursor_str']
    
    for i in tqdm(followers['users'],total=len(followers['users'])):
        inserted_at=str(datetime.now())
        created_at=i.get('created_at','None')
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
        sql=f"INSERT INTO `followers`(created_at,inserted_at,description"\
        ",favourites_count,followers_count,friends_count"\
        ",id_str,lang,location,name,profile_image_url_https,protected,screen_name,status_text,"\
        "statuses_count,verified,time_zone,url) "\
        f""" VALUES('{created_at}','{inserted_at}',"{description}",'{favourites_count}','{followers_count}' """\
        f""",'{friends_count}','{id_str}','{lang}',"{location}","{name}",'{profile_image_url_https}' """\
        f""" ,'{protected}','{screen_name}',"{status_text}",'{statuses_count}','{verified}','{time_zone}','{url}')  """
        conn.execute(sql)
        conn.commit()

# close connection
conn.close()




































