# CapstoneProject

Before setting up docker create a bridge network in docker.

`docker network create api-tier`

This will help to establish conection between multiple app service.

## Docker Setup Data Ingestion Service

First go to the training service folder

`cd path/to/data_ingestion_service`

`docker-compose build`
`docker-compose up`

### Individual Container Spin Up

`docker-compose up zookeeper`
`docker-compose up kafka`
`docker-compose up mysqldb`
`docker-compose up phpmyadmin`
`docker-compose up data_ingestion`

## Docker Setup Predictor/Training Service

First go to the training service folder

`cd path/to/training_service`

`docker-compose build`
`docker-compose up`

### Individual Container Spin Up

`docker-compose up predictor`


