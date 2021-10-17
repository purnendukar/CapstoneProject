FROM python:3.9.6
RUN apt-get update

WORKDIR /data_ingestion

# RUN apt-get update 
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /data_ingestion
RUN apt-get install -y cron

COPY cron.txt /data_ingestion/cron.txt
RUN crontab /data_ingestion/cron.txt




