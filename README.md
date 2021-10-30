# CapstoneProject

Before setting up docker create a bridge network in docker.

`docker network create api-tier`

This will help to establish conection between multiple app service.

## Docker Setup Data Ingestion Service

First go to the training service folder

`cd path/to/data_ingestion_service`

Now run the following command:

* `docker-compose build`
* `docker-compose up`

### Individual Container Spin Up

Incase any container fails to start.

* `docker-compose up zookeeper`
* `docker-compose up kafka`
* `docker-compose up mysqldb`
* `docker-compose up phpmyadmin`
* `docker-compose up data_ingestion`


## Data Analysis and Preprocessing

This is part of Capstone - week 2 Milestone - Data Preprocessing

## Prerequisites
Data Ingestion to be completed and data should present in the news_data table in mysql db container.

## Setup Docker
`sudo docker up --build`

## Preprocess Engineer
`python preprocess.py`

To Simulate the data ingestion pipeline, plese follow below.

`sudo docker up --build`

`sudo docker exec -it model-training-service_db_1 bash`

Run below with in model-training-service_db_1 container.

`mysql -uroot -proot < dump.sql`

`Note: dump.sql containes schema construction which was resulted from data ingestion pipeline`

Once both containers are up, run below commands to check the preproccessed file.

`sudo docker exec -it model-training-service_preprocessor_1 bash`

`cd data`

`ls preprocessed*`

`You should see a file starting with preprocesseddata_{}.csv`

`Note : To reduce the computatio time, the preprocess enginer is setup for 5000 records however we can change no of records by doing below modifications`

`- add {noofrecords argument in preprocessor/Dockerfile}`

`ENTRYPOINT python preprocess.py {noofrecords} && sleep 1800`


## Docker Setup Predictor/Training Service

This is part of Capstone - week 3 Milestone - New Predictor 

First go to the training service folder

`cd path/to/train_predict_service`

Now run the following command:

* `docker-compose build`
* `docker-compose up`

### Individual Container Spin Up

Incase any container fails to start.

* `docker-compose up predictor`

### Retrain Model

`curl --location --request GET 'http://localhost:7000/retrain'`


