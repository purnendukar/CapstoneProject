import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
import nltk
import json
import mysql.connector as mysql
import pickle
from nltk.stem import PorterStemmer
from nltk import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
import sys
import re

class Connector:
    def __init__(self):
        self.config=json.load(open('./db_config.json','r'))[0]

        self.db_user = self.config.get('user')
        self.db_pwd = self.config.get('password')
        self.db_host = self.config.get('host')
        # self.db_port = self.config.get('port')
        self.db_name = self.config.get('database')# specify connection string
        self.db_table=self.config.get('test_table')
        self.db=None
        self.cur=self.connect_to_db()
        self.data=dict()
    def connect_to_db(self):
        self.db = mysql.connect(host = self.db_host,user = self.db_user,passwd = self.db_pwd,database = self.db_name,port= self.db_port)
        print('connected to db')
        return self.db.cursor()
    
    def fetch_data(self,table_name='news_data'):
        #conn=self.connect_to_db()
        query_str=f'select * from {table_name}'
        self.cur.execute(query_str)
        result=self.cur.fetchall()
        print('data has been fetched')
        return result
    def convert_to_rdd(self,records):
        ids=[]
        title=[]
        createddate=[]
        summary=[]
        topic=[]
        urls=[]
        for rec in records:
            ids.append(rec[0])
            title.append(rec[1])
            createddate.append(str(rec[2]))
            summary.append(rec[3])
            topic.append(rec[4])
            urls.append(rec[5])
        self.data={'id':ids,\
            'title':title,\
            'createddate':createddate,\
            'summary':summary,\
            'topic':topic,\
            'source_url':urls}
        df=pd.DataFrame(self.data)
        sparksession=SparkSession.builder.appName('preprocessor').getOrCreate()
        rdd=sparksession.createDataFrame(df)
        print('data has been converted into rdd')
        return rdd
    
    def preprocess(self,rdd,length=5000):
        rdd=rdd.dropna(how='any')
        rdd=rdd.collect()
        if length is None:
            length=len(rdd)
        corpus=[]
        topic=[]
        for row in rdd[:length]:
            text=row['title']+' '+row['summary']
            corpus.append(text)
            topic.append(row['topic'])
        updated_corpus=[]
        stemmer=PorterStemmer()
        for row in corpus:
            sents=' '.join([sent for sent in sent_tokenize(row)])
            words=[word for word in word_tokenize(sents) if not word in stopwords.words('english')]
            words=[word for word in words if len(word)>1]
            #words=[word for word in words if not word in punctuation]
            words=[re.sub('[^a-zA-Z0-9.]+', '',word) for word in words]
            #tagged_words=[nltk.pos_tag(word) for word in words]
            words=' '.join([stemmer.stem(word) for word in words])
            updated_corpus.append(words)
        print('preprocessing is completed')
        self.cur.close()
        self.db.close()

        return updated_corpus,topic
    """
    def __del__(self):
        self.cur.close()
        #self.db.close()
    """
    

if __name__=='__main__':
    if len(sys.argv)>1:
        given_length=int(sys.argv[1])
    else:
        given_length=5000 #this is just to reduce the computation
    
    connector=Connector()
    records=connector.fetch_data()
    spark_df=connector.convert_to_rdd(records)
    corpus,topic=connector.preprocess(spark_df,given_length)
    #below just to store the preprocessed data
    pandas_df=pd.DataFrame({'text':corpus,'topic':topic})
    pandas_df.to_csv(f'./data/preprocesseddata_{given_length}.csv',sep='|',index=False)
    

