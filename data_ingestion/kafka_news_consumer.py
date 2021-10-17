from kafka import KafkaConsumer
from sqlalchemy.orm import sessionmaker
import json

from models import News, engine

Session = sessionmaker(bind = engine)
session = Session()

consumer = KafkaConsumer(
    'news',
    bootstrap_servers='kafka:9092'
)
for data in consumer:
    print(data.value.decode())
    try:
        news = json.loads(data.value.decode())
        new_obj = News(
            title=news.get("title"),
            date_time=news.get("published_date"),
            summary=news.get("summary"),
            topic=news.get("topic"),
            source=news.get("clean_url")
        )
        session.add(new_obj)
        session.commit()
    except Exception as error:
        print("error", str(error))
        session.rollback()

