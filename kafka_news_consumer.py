from kafka import KafkaConsumer
consumer = KafkaConsumer('news')
for msg in consumer:
    print (msg)

