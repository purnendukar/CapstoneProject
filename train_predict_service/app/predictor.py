from flask import Flask, request, render_template, jsonify
from numpy.core.numeric import True_
import pandas as pd
#from kafka import KafkaProducer
import json
from threading import Thread
from werkzeug.utils import redirect
from random import randint
# from pyhive import hive
from pyspark.sql import SparkSession
from sqlalchemy import select

import requests
from bs4 import BeautifulSoup

from utils import text_preprocessor,predictor,retrain_model
from models import News
from kafka import KafkaProducer

import mysql.connector as mysql


db = mysql.connect(
    host = "mysqldb",
    user = "root",
    passwd = "password",
    database = "capstone",
)
connn = db.cursor()

sparksession=SparkSession.builder.appName('preprocessor').master("spark://spark-master:7077").getOrCreate()

producer = KafkaProducer(bootstrap_servers='kafka:9092')

import os
path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():
    if request.method == "GET":
        return render_template(
            "index.html",
        )


@app.route("/news_classify", methods=["POST"])
def news_classfier():
    request_data = dict(request.form)
    print("request_data",request_data)

    url = request_data.get('url')
        
    if request.method == "POST":
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('head').find_all('title')[0].contents[0]
        description = ""
        for tag in soup.find_all("meta"):
            if tag.get("name", None) == "description":
                description = tag.get("content", "")
                break
        data = {
            "title": title,
            "summary": description,
            "source": url
        }
        producer.send('news', json.dumps(data).encode())
        trans_text=text_preprocessor(data["summary"])
        prediction=predictor(trans_text)
    return render_template(
        "index.html",
        url=url,
        category=prediction
    )

@app.route("/retrain", methods=["GET"])
def retrain_model_api():
    if request.method == "GET":
        query='select * from news'
        connn.execute(query)
        records = connn.fetchall()

        train_set = {
            'id': [],
            'title': [],
            'createddate': [],
            'summary': [],
            'topic': [],
            'source_url': []
        }

        for rec in records:
            train_set["id"].append(rec[0])
            train_set["title"].append(rec[1])
            train_set["createddate"].append(str(rec[2]))
            train_set["summary"].append(rec[3])
            train_set["topic"].append(rec[4])
            train_set["source_url"].append(rec[5])

        df = pd.DataFrame(train_set)
        rdd = sparksession.createDataFrame(df.astype(str))

        # thread = Thread(target=retrain_model, args=(rdd,))
        # thread.start()
        retrain_model(rdd)

        return jsonify({
            "message": "Model Retraining Started check spark portal for job process.",
        })


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)