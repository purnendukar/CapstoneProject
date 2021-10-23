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

producer = KafkaProducer(bootstrap_servers='kafka:9092')

import os
path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder="templates")

"""
producer = KafkaProducer(
    bootstrap_servers = app.config["KAFKA_SERVER"],
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)
"""
@app.route("/")
def home():
    if request.method == "GET":
        return render_template(
            "index.html",
        )

"""
def df_send_kafka(df, test_id=None):
    print('send thread started')
    for data in json.loads(df.to_json(orient="records")):
        if test_id:
            data["test_id"] = test_id
        producer.send(topic=app.config["TOPIC"], value=data)
"""


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
        category=prediction
    )

@app.route("/retrain", methods=["GET"])
def test_model():
    # if request.method == "GET":
    #     return render_template(
    #         "retrain.html",
    #     )
    # elif request.method == "POST":
    if request.method == "GET":
        train_set = select(News)
        sparksession=SparkSession.builder.appName('preprocessor').getOrCreate()
        rdd=sparksession.createDataFrame(train_set)

        #thread = Thread(target=df_send_kafka, args=(test_set,test_id))
        #thread.start()
        retrain_model(rdd)

        return jsonify({
            "message": "Retrain Successful"
        })


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)