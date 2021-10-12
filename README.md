# CapstoneProject

## Setup Data Ingestion System
### Install Cronjob
`apt-get install cron`

### Install MySQL
`apt install mysql-server`

### Create MySQL DB
`CREATE DATABASE capstone;`

### Install virtual machine and requirements
* `pip install virtualenv`
* `python3 -m venv /path/to/new/virtual/environment`
* `source /path/to/new/virtual/environment/bin/activate`
* `pip3 install requirements.txt`

### Setup cron job
Open cron tab: `contab -e`. <br/>
Cronjob script to run cron job daily at 22:00.
```
0 22 * * * /path/to/new/virtual/environment/bin/python path/to/project/news_collector.py
```

### Start Kafka News Consumer
`python kafka_news_consumer.py`



