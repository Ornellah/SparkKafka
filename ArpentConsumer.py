import os
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, ArrayType

output_csv_path = "./output/arpentResultatsDiplomes.csv"
checkpoint_path = "./checkpoint/arpentResultatsDiplomes"

# if folders exist, any folder is created
os.makedirs(output_csv_path, exist_ok=True)
os.makedirs(checkpoint_path, exist_ok=True)

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0") \
    .getOrCreate()

file_path = './schémas/arpent_resultats_diplomes.json'

def load_schema(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    schema = StructType()
    for field_name, field_type in data["properties"].items():
        if field_type['type'] == "string":
            schema.add(StructField(field_name, StringType(), True))
        elif field_type['type'] == "integer":
            schema.add(StructField(field_name, IntegerType(), True))
        elif field_type['type'] == "double":
            schema.add(StructField(field_name, DoubleType(), True))
    schema = ArrayType(schema)
    return schema

schema_arpent_resultats_diplomes = load_schema('./schémas/arpent_resultats_diplomes.json')

# Read Kafka stream
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "arpent-resultats-diplomes") \
    .load()

# Deserialize JSON data
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema_arpent_resultats_diplomes).alias("data")) \
    .select(explode(col("data")).alias("data")) \
    .select("data.*")

# Save data into CSV file
query = df.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path", output_csv_path) \
    .option("checkpointLocation", checkpoint_path) \
    .start()

query.awaitTermination()
