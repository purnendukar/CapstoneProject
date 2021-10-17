import http.client
import json
import urllib
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka:9092')

conn = http.client.HTTPSConnection("free-news.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "free-news.p.rapidapi.com",
    'x-rapidapi-key': "4fad5a1a3amshd180764702d3661p148960jsn97aaca3817a6"
}

query_list = [
    "football",
    "cricket",
    "tennis",
    "Business",
    # "startup",
    # "india",
    # "covid",
    # "pandemic",
    # "technology",
    # "bitcoin",
    # "usa",
    # "facebook",
    # "crypto",
    # "cryptocurrency",
    # "Elon Musk",
    # "Bill Gates",
    # "Microsoft",
    # "Tesla",
    # "Government",
    # "Oil",
    # "Tax",
    # "market",
    # "stocks",
    # "Lockdown",
    # "Android",
    # "Apple",
    # "Electric Car",
    # "Electric Bike",
    # "Phone",
    # "Medicine",
    # "Vaccine",
    # "Petrol",
    # "Startup",
    # "Reliance",
    # "Ambani",
    # "Sports",
    # "Olympic",
    # "TCS",
    # "Wipro",
    # "Nifty",
    # "Army",
    # "Post",
    # "finance",
    # "Ratan Tata",
    # "Tata Steel",
    # "Birla",
    # "Aditya Birla",
    # "School",
    # "Accident",
    # "Disaster",
    # "Farmer",
    # "Mobo Industry",
    # "Android",
    # "iPhone",
    # "iPad",
    # "Appolo",
    # "Fortis",
    # "Air Force",
    # "Prime Minister",
    # "Home",
    # "Loan",
    # "Scam",
    # "UK",
    # "Crisis",
    # "West Bengal",
    # "Delhi",
    # "Bangalore",
    # "Mumbai",
    # "Flood",
    # "SpaceX",
    # "ISRO",
    # "Mangalyan",
    # "Data Science",
    # "ICICI",
    # "Yes Bank",
    # "Hyderabad",
    # 'finance',
    # 'news',
    # 'economics',
    # 'business',
    # 'sport',
    # 'energy',
    # 'tech',
    # 'music',
    # 'science',
    # 'entertainment',
    # 'gaming',
    # 'world',
    # 'politics',
    # 'travel',
    # 'beauty',
    # 'food',
    # 'opinion'
]

import time

for query in query_list:
    arr = []
    try:
        end_point = f"/v1/search?q={urllib.parse.quote(query)}&lang=en&page_size=25"
        conn.request("GET", end_point, headers=headers)
        res = conn.getresponse()
        data = res.read()
        response_json = json.loads(data.decode("utf-8"))
        print("end_point", end_point)
        for news in response_json['articles']:
            producer.send('news', json.dumps(news).encode())
        time.sleep(2)
    except Exception as error:
        print(error)
    print(query, "done")
