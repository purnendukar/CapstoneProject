import http.client
import json
import urllib

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
    "startup",
    "india",
    "covid",
    "pandemic",
]

for query in query_list:
    end_point = f"/v1/search?q={urllib.parse.quote(query)}&lang=en"
    # print("end_point", end_point)
    conn.request("GET", end_point, headers=headers)

    res = conn.getresponse()
    data = res.read()

    response_json = json.loads(data.decode("utf-8"))
    print(query, "done")
