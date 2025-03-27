import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StringType
import sys

kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
kafka_topic = "my-topic-1"

schema = StructType().add("message", StringType())

spark = SparkSession.builder \
    .appName("KafkaConsumerApp") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "latest") \
    .load()

value_df = raw_df.selectExpr("CAST(value AS STRING) as value")
parsed_df = value_df.select(col("value").alias("message"))

def print_batch(batch_df, _):
    messages = [row.message for row in batch_df.collect() if row.message]
    for msg in messages:
        print(f">>> {msg}", file=sys.stdout, flush=True)

query = parsed_df.writeStream \
    .outputMode("append") \
    .foreachBatch(print_batch) \
    .start()

query.awaitTermination()

spark.stop()