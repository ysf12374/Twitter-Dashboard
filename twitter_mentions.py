#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 02:00:20 2020

@author: yousuf
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 19:57:20 2020

@author: yousuf
"""

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

SEARCH_FOR='UChicago'
SEARCH_FOR_ID='131144285'
start=time()
#twitter = Twython(API_KEY, API_SECRET_KEY)
#
#auth = twitter.get_authentication_tokens(callback_url='https://dev.deepcheck.one:8080/twitter')

twitter = Twython(
API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
#user=twitter.lookup_user(screen_name='_KSU')
tweets=twitter.search(q=f'(@{SEARCH_FOR})',count=100)

length_followers=len(tweets['statuses'])

#remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
#remaining_calls=int(remaining_calls)
remaining_calls=175
if remaining_calls<2:
    print(remaining_calls)
    rem_time=time()-start
    if rem_time<925:
        print(f"Sleeping for [{920-int(rem_time)}] seconds")
        sleep(920-int(rem_time))
    else:
        print("Sleeping for [20] seconds")
        sleep(20)
    start=time()
txtx=[x['id'] for x in tweets['statuses']]
max_id=str(min(txtx))
#max_id=tweets['search_metadata']['next_results'].split('&')[0].split('=')[-1]
#twt=DB_Twitter(DB_NAME,DB_PATH)
#twt.open_con()
conn=sqlite3.connect(DB_PATH+DB_NAME)
for i in tqdm(tweets['statuses'],total=len(tweets['statuses'])):
        inserted_at=str(datetime.now())
        created_at=i.get('created_at','None')
        try:
            coordinates=str(i.get('coordinates','None').get("coordinates",'None'))
        except:
            coordinates='NONE'
        entities=i.get('entities','None')
        
        hashtags_all=entities.get('hashtags','None')
        hashtags_count=str(len(hashtags_all))
        hashtags=[x.get('text','None').replace('"','') for x in hashtags_all if x.get('text',None)]
        
        symbols_all=entities.get('symbols','None')
        symbols_count=str(len(symbols_all))
        symbols=[x.get('text','None').replace('"','') for x in symbols_all if x.get('text',None)]
    
        urls_all=entities.get('urls','None')
        urls_count=str(len(urls_all))
        urls=[x.get('expanded_url','None').replace('"','') for x in urls_all if x.get('expanded_url',None)]
        
        user_mentions_all=entities.get('user_mentions','None')
        user_mentions_count=str(len(user_mentions_all))
        user_mentions=[x.get('screen_name','None').replace('"','') for x in urls_all if x.get('screen_name',None)]
          
        favorite_count=i.get('favorite_count','None')
        try:
            geo=str(i.get('geo','None'))
        except:
            geo='None'
        id_str=i.get('id_str','None')
        lang=i.get('lang','None')
        try:
            place=i.get('place','None').replace('"','')
        except:
            place='None'
        retweet_count=i.get('retweet_count','None')
        text=i.get('text','None').replace('"','')
        try:
            text=i.get('text','None').replace('"','')
        except:
            text='None'
        quote_count=i.get('quote_count','None')
        reply_count=i.get('reply_count','None')
    
        from_=i.get('user',None)
        if from_:
            from_id_str=from_.get('id_str','None')
            from_screen_name=from_.get('screen_name','None')
            try:
                from_screen_name=from_screen_name.replace('"','')
            except:
                from_screen_name='None'
        else:
            from_id_str='None'
            from_screen_name='None'
            
#        try:
#            to_id_str=i.get('in_reply_to_user_id','None')
#            to_screen_name=i.get('in_reply_to_screen_name','None')
#            try:
#                to_screen_name=to_screen_name.replace('"','')
#            except:
#                to_screen_name='None'
#        except:
#            to_id_str='None'
#            to_screen_name=f'{SEARCH_FOR}'
        to_id_str='{SEACH_OR_ID}'
        to_screen_name=f'{SEARCH_FOR}'            
        sql=f"INSERT INTO `influencers`(created_at,inserted_at,coordinates"\
        ",hashtags,hashtags_count,symbols,symbols_count,urls,urls_count,user_mentions,user_mentions_count"\
        ",favorite_count,geo,id_str,lang,place,retweet_count,text,quote_count,"\
        "reply_count,'to_id_str','to_screen_name','from_id_str','from_screen_name') "\
        f""" VALUES('{created_at}','{inserted_at}',"{coordinates}","{hashtags}",'{hashtags_count}' """\
        f""","{symbols}",'{symbols_count}',"{urls}","{urls_count}","{user_mentions}",'{user_mentions_count}' """\
        f""" ,'{favorite_count}',"{geo}","{id_str}",'{lang}',"{place}",'{retweet_count}',"{text}",'{quote_count}','{reply_count}','{to_id_str}',"{to_screen_name}",'{from_id_str}',"{from_screen_name}")  """
        conn.execute(sql)
        conn.commit()



while True:
    tweets=twitter.search(q=f'(@{SEARCH_FOR})',count=100,max_id=max_id)
    remaining_calls-=1
    length_followers=len(tweets['statuses'])
    if length_followers<=1:
        break
#    remaining_calls=twitter.get_lastfunction_header('x-rate-limit-remaining')
#    remaining_calls=int(remaining_calls)
    
    if remaining_calls<2:
        print(remaining_calls)
        rem_time=time()-start
        if rem_time<925:
            print(f"Sleeping for [{920-int(rem_time)}] seconds")
            sleep(920-int(rem_time))
        else:
            print(f"Sleeping for [20] seconds")
            sleep(20)
        start=time()
        remaining_calls=175
    
    txtx=[x['id'] for x in tweets['statuses']]
    max_id=str(min(txtx))
    
    for i in tqdm(tweets['statuses'],total=len(tweets['statuses'])):
        inserted_at=str(datetime.now())
        created_at=i.get('created_at','None')
        try:
            coordinates=str(i.get('coordinates','None').get("coordinates",'None'))
        except:
            coordinates='NONE'
        entities=i.get('entities','None')
        
        hashtags_all=entities.get('hashtags','None')
        hashtags_count=str(len(hashtags_all))
        hashtags=[x.get('text','None').replace('"','') for x in hashtags_all if x.get('text',None)]
        
        symbols_all=entities.get('symbols','None')
        symbols_count=str(len(symbols_all))
        symbols=[x.get('text','None').replace('"','') for x in symbols_all if x.get('text',None)]
    
        urls_all=entities.get('urls','None')
        urls_count=str(len(urls_all))
        urls=[x.get('expanded_url','None').replace('"','') for x in urls_all if x.get('expanded_url',None)]
        
        user_mentions_all=entities.get('user_mentions','None')
        user_mentions_count=str(len(user_mentions_all))
        user_mentions=[x.get('screen_name','None').replace('"','') for x in urls_all if x.get('screen_name',None)]
          
        favorite_count=i.get('favorite_count','None')
        try:
            geo=str(i.get('geo','None'))
        except:
            geo='None'
        id_str=i.get('id_str','None')
        lang=i.get('lang','None')
        try:
            place=i.get('place','None').replace('"','')
        except:
            place='None'
        retweet_count=i.get('retweet_count','None')
        text=i.get('text','None').replace('"','')
        try:
            text=i.get('text','None').replace('"','')
        except:
            text='None'
        quote_count=i.get('quote_count','None')
        reply_count=i.get('reply_count','None')
    
        from_=i.get('user',None)
        if from_:
            from_id_str=from_.get('id_str','None')
            from_screen_name=from_.get('screen_name','None')
            try:
                from_screen_name=from_screen_name.replace('"','')
            except:
                from_screen_name='None'
        else:
            from_id_str='None'
            from_screen_name='None'
            
#        try:
#            to_id_str=i.get('in_reply_to_user_id','None')
#            to_screen_name=i.get('in_reply_to_screen_name','None')
#            try:
#                to_screen_name=to_screen_name.replace('"','')
#            except:
#                to_screen_name='None'
#        except:
#            to_id_str='None'
#            to_screen_name=f'{SEARCH_FOR}'
        to_id_str='{SEACH_OR_ID}'
        to_screen_name=f'{SEARCH_FOR}'    
        sql=f"INSERT INTO `influencers`(created_at,inserted_at,coordinates"\
        ",hashtags,hashtags_count,symbols,symbols_count,urls,urls_count,user_mentions,user_mentions_count"\
        ",favorite_count,geo,id_str,lang,place,retweet_count,text,quote_count,"\
        "reply_count,'to_id_str','to_screen_name','from_id_str','from_screen_name') "\
        f""" VALUES('{created_at}','{inserted_at}',"{coordinates}","{hashtags}",'{hashtags_count}' """\
        f""","{symbols}",'{symbols_count}',"{urls}","{urls_count}","{user_mentions}",'{user_mentions_count}' """\
        f""" ,'{favorite_count}',"{geo}","{id_str}",'{lang}',"{place}",'{retweet_count}',"{text}",'{quote_count}','{reply_count}','{to_id_str}',"{to_screen_name}",'{from_id_str}',"{from_screen_name}")  """
        conn.execute(sql)
        conn.commit()

conn.close()




































