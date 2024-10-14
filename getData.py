import requests
from kafka import KafkaProducer
import json

# Configuration Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# URLs des API
api_urls = [
    'https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc',
    'https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/condition_environnementale_pc',
    'https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/operation_pc',
    'https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc'
]

# Topics Kafka correspondants
topics = [
    'qualite-rivieres-analyse-pc',
    'qualite-rivieres-condition-environnementale-pc',
    'qualite-rivieres-operation-pc --bootstrap-server',
    'qualite-rivieres-station-pc'
]

# Récupérer et envoyer les données à Kafka
for api_url, topic in zip(api_urls, topics):
    response = requests.get(api_url)
    data = response.json()

    # Si les données sont une liste, limiter à 10 éléments
    if isinstance(data, list):
        data = data[:10]

    # Envoyer les données à Kafka
    for item in data:
        producer.send(topic, value=item)
        producer.flush()

# Fermer le producteur Kafka
producer.close()