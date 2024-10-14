from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

# Créer une session Spark
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

# Définir le schéma des données
schema = StructType([
    StructField("field1", StringType(), True),
    StructField("field2", StringType(), True),
    # Ajoutez les autres champs selon le schéma de vos données
])

# Lire les données depuis Kafka
topics = ['qualite-rivieres-analyse-pc', 'qualite-rivieres-condition-environnementale-pc', 'qualite-rivieres-operation-pc --bootstrap-server', 'qualite-rivieres-station-pc']

for topic in topics:
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic) \
        .load()

    # Désérialiser les données JSON
    df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Afficher les données
    query = df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()
