# model-training-service
###  This is part of Capstone - week 2 Milestone - Data Preprocessing

## Prerequisites.
1. data Ingestion to be completed and data should present in the news_data table in mysql db container.

## Setup Docker
`sudo docker up --build`

## preprocess enginer
`python preprocess.py`

## To Simulate the data ingestion pipeline, plese follow below.
`sudo docker up --build`

`sudo docker exec -it model-training-service_db_1 bash`

### run below with in model-training-service_db_1 container
`mysql -uroot -proot < dump.sql`

`Note ; dump.sql containes schema construction which was resulted from data ingestion pipeline`

### once both containers are up, run below commands to check the preproccessed file.
`sudo docker exec -it model-training-service_preprocessor_1 bash`

`cd data`

`ls preprocessed*`

`You should see a file starting with preprocesseddata_{}.csv`

`Note : To reduce the computatio time, the preprocess enginer is setup for 5000 records however we can change no of records by doing below modifications`

`- add {noofrecords argument in preprocessor/Dockerfile}`

`ENTRYPOINT python preprocess.py {noofrecords} && sleep 1800`

### milestone report has been added under ./milestonereport

