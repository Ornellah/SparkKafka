import requests
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))

api_url = "https://ensagri-pprd.api.agriculture.gouv.fr/arpent-resultats-api/api/arpent-resultats/diplomes"

response = requests.get(api_url)
data = response.json()

for item in data:
    producer.send("arpent-resultats-diplomes", item)
    producer.flush()
    
producer.close()