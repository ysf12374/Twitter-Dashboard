from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from ip2geotools.databases.noncommercial import DbIpCity
from django.db import connections
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import base64
import io
import sys
import json 
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import json
from pandas import read_sql,DataFrame,to_numeric
from django.utils.encoding import smart_str
import os,sys
import secrets
import wave
import sqlite3
from sqlite3 import Error
from twython import Twython
from time import sleep,time
from datetime import datetime
from pandas.api.types import CategoricalDtype
sorter = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
sorterIndex = dict(zip(sorter,range(len(sorter))))
# Create your views here.


@csrf_exempt
def twitter(request,oauth_token='',oauth_verifier='',*args,**kwargs):
      context={
                'oauth_token':request.GET.get('oauth_token',None),
                'oauth_verifier':request.GET.get('oauth_verifier',None),
              }
      return render(request,'extra/twitter.html',{'data':context})  


def dashboard(request,*args,**kwargs):
  conn=sqlite3.connect(settings.DB_PATH+settings.DB_NAME2)
  tweets=read_sql('select * from tweets',con=conn,index_col=['id'])
  influencers=read_sql('select * from influencers',con=conn,index_col=['id'])
  users=read_sql('select * from users_ where screen_name="_KSU" order by inserted_at desc',con=conn,index_col=['id'])
  mentions=influencers[influencers['to_id_str']!='{SEACH_OR_ID}']
  retweets=influencers[influencers['to_id_str']=='{SEACH_OR_ID}']
  influencers.index=list(range(1,len(influencers)+1))


  tweets['retweet_count'] =to_numeric(tweets['retweet_count'], errors ='coerce').fillna(0).astype('int')
  tweets_=users['statuses_count'][0]
  mentions_=len(mentions)
  avg_retweets_=int(tweets['retweet_count'].mean())
  followers_=users['followers_count'][0]
  following_=users['friends_count'][0]
  favourites_=users['favourites_count'][0]
  retweets_mentions_by_user_=users['listed_count'][0]
  location_=users['location'][0]
  age_user_=int(((datetime.now()-datetime.strptime(users['created_at'][0], '%a %b %d %H:%M:%S +0000 %Y')).days)/365)

  retweets['created_at']=retweets['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
  retweets['inserted_at']=retweets['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
  tweets['created_at']=tweets['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
  tweets['inserted_at']=tweets['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
  tweets['created_date_md']=tweets['created_at'].apply(lambda x:  str(x.strftime('%A')))
  tweets_df = (tweets.groupby('created_date_md', as_index=False)
         .agg({'id_str':'count', 'retweet_count':'mean'})).reset_index(drop=True)
  tweets_df['Day_id'] = tweets_df['created_date_md'].map(sorterIndex)
  tweets_df=tweets_df.sort_values('Day_id')
  
  tweets_df['retweet_count']=tweets_df['retweet_count'].astype(int)
  influencers['created_at']=influencers['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
  influencers['inserted_at']=influencers['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
  influencers['created_date_md']=influencers['created_at'].apply(lambda x: str(x.day)+'/'+str(x.month)+'/'+str(x.year))
  influencers_df = (influencers.groupby('created_date_md', as_index=False)
       .agg({'id_str':'count'})).reset_index(drop=True)
  influencers_df['create_date']=influencers_df['created_date_md'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
  influencers_df=influencers_df.sort_values('create_date')
  m_values2=list(tweets_df['retweet_count'].values)
  m_values=list(tweets_df['id_str'].values)
  month=list(tweets_df['created_date_md'].values)
  influencer=list(influencers_df['created_date_md'].values)
  influencer_values=list(influencers_df['id_str'].values)

  # conn.close()
  # conn=sqlite3.connect(settings.DB_PATH+settings.DB_NAME1)

  # followers=read_sql('select * from followers',con=conn,index_col=['id'])
  # followers['followers_count']=followers['followers_count'].astype(int)
  # followers['created_at']=followers['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
  # followers['inserted_at']=followers['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
  # conn.close()
  followers=read_sql('select * from followers_followers where screen_name="_KSU"',con=conn)
  a0_250=followers['a0_250'][0]
  a250_500=followers['a250_500'][0]
  a500_1k=followers['a500_1k'][0]
  a1k_2_5k=followers['a1k_2_5k'][0]
  a2_5k_5k=followers['a2_5k_5k'][0]
  # a5k_10k=followers['a5k_10k'][0]
  # a10k_25k=followers['a10k_25k'][0]
  # a25k_50k=followers['a25k_50k'][0]
  # a50k_100k=followers['a50k_100k'][0]
  # a_g_100k=followers['a_g_100k'][0]
  fllws_rng=['0-250','250-500','500-1K',
            '1K-2.5K','2.5K-5K']
            # ,'5K-10K','10K-25K','25K-50K',
            # '50K-100K','>100K']

  fllws_values=[a0_250,a250_500,a500_1k,a1k_2_5k,a2_5k_5k]
            # ,a5k_10k,a10k_25k,a25k_50k,
            # a50k_100k,a_g_100k]


  followers_age=read_sql('select * from followers_age where screen_name="_KSU"',con=conn)
  years=list(followers_age['years'].values)
  years=[x+' Yr' for x in years]
  count=list(followers_age['count'].values)

  sentiment=read_sql('select * from tweets where name is null',con=conn,index_col=['id'])

  pos=len(sentiment[sentiment['sentiment']=='Positive'])
  neg=len(sentiment[sentiment['sentiment']=='Negative'])
  neu=len(sentiment[sentiment['sentiment']=='Neutral'])





  SEARCH_FOR="_KSU"
  SEARCH_FOR_ID='18916965'

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

  ksu_rt_val=[int(x) for x in ksu_rt_val]
  kauweb_rt_vals=[int(x) for x in kauweb_rt_vals]
  IMSIU_edu_sa_rt_val=[int(x) for x in IMSIU_edu_sa_rt_val]
  kkueduksa_rt_val=[int(x) for x in kkueduksa_rt_val]
  EdinburghUni_rt_val=[int(x) for x in EdinburghUni_rt_val]
  OfficialUoM_rt_val=[int(x) for x in OfficialUoM_rt_val]
  Harvard_rt_val=[int(x) for x in Harvard_rt_val]
  UChicago_rt_val=[int(x) for x in UChicago_rt_val]

  users_unique = users.drop_duplicates('id_str')
  context={'months_values':",".join([str(x) for x in m_values]),
            'months':",".join(["'"+x+"'" for x in month]),
            'months_values2':",".join([str(x) for x in m_values2]),
            'influencer':influencer,
            'influencer_values':",".join([str(x) for x in influencer_values]),
            'follwers_range':fllws_rng,
            'follwers_range_values':fllws_values,
            'age_values':",".join([str(x) for x in count]),
            'age':years,
            'tweets':tweets_,
            'mentions':mentions_,
            'retweets':avg_retweets_,
            'followers':followers_,
            'following_':following_,
            'favourites':favourites_,
            'retweets_mentions_by_user':retweets_mentions_by_user_,
            'location':location_,
            'user_age':age_user_,
            'results':['Neutral','Positive','Negative'],
            'results_values':[neu,pos,neg],
            'tweets_month':sorter,
            'tweets_values_ksu':ksu_val,
            'tweets_values_kauweb':kauweb_vals,
            'tweets_values_IMSIU_edu_sa':IMSIU_edu_sa_val,
            'tweets_values_kkueduksa':kkueduksa_val,
            'tweets_values_EdinburghUni':EdinburghUni_val,
            'tweets_values_OfficialUoM':OfficialUoM_val,
            'tweets_values_Harvard':Harvard_val,
            'tweets_values_UChicago':UChicago_val,
            'tweets_values_rt_ksu':ksu_rt_val,
            'tweets_values_rt_kauweb':kauweb_rt_vals,
            'tweets_values_rt_IMSIU_edu_sa':IMSIU_edu_sa_rt_val,
            'tweets_values_rt_kkueduksa':kkueduksa_rt_val,
            'tweets_values_rt_EdinburghUni':EdinburghUni_rt_val,
            'tweets_values_rt_OfficialUoM':OfficialUoM_rt_val,
            'tweets_values_rt_Harvard':Harvard_rt_val,
            'tweets_values_rt_UChicago':UChicago_rt_val,
            }

  return render(request,'extra/dashboard_new.html',{'compare':users_unique.to_dict(orient="records"),'data':context,})










def customer_list(request,p_num=1,*args,**kwargs):
      conn=sqlite3.connect(settings.DB_PATH+settings.DB_NAME1)
      customers_count=read_sql("select count(*) as count from followers " ,
              con=conn)
      length_cust=customers_count['count'][0] # len(customers_count.T.to_dict().values())
      length_cust=int(length_cust)
      if length_cust%2>0:
        last_page=(length_cust//2)+1
      else:
        last_page=(length_cust//2)
      if p_num=='' or not p_num:
        p_num=1
      if not p_num:
        per_page=1
      p_num=int(p_num)
      if p_num<=0:
        p_num=1
      elif int(p_num)>last_page:
        p_num=last_page
      if p_num==0:
        previous_page=0
      else:
        previous_page=p_num-1
      if p_num==last_page:
        next_page=p_num
      else:
        next_page=p_num+1 
      p_num=int(p_num)-1
      per_page=10*int(p_num) 
      if per_page<0:
        per_page=0
      customers_=read_sql("SELECT * FROM followers " \
        f" order by created_at desc LIMIT 10 OFFSET {per_page}",
        con=conn)
      conn.close()
      context={
          'length':length_cust,
          'last_page':last_page,
          'current_page':p_num,
          'previous_page':previous_page,
          'next_page':next_page,
          'range':range(1,4),
        }
      return render(request,'extra/follower_list.html',{'data':customers_.T.to_dict().values(),'context':context})  





















































