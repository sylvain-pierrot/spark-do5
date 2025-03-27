import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import input_file_name, current_timestamp

s3_endpoint = os.environ["S3_ENDPOINT"]
s3_access_key = os.environ["S3_ACCESS_KEY"]
s3_secret_key = os.environ["S3_SECRET_KEY"]
s3_bucket = os.environ["S3_BUCKET"]
s3_prefix = os.environ.get("S3_PREFIX", "")
s3_uri = f"s3a://{s3_bucket}/{s3_prefix}"

# Create Spark session
spark = (
    SparkSession.builder.appName("BucketMonitorStreamApp")
    .config("spark.hadoop.fs.s3a.endpoint", s3_endpoint)
    .config("spark.hadoop.fs.s3a.access.key", s3_access_key)
    .config("spark.hadoop.fs.s3a.secret.key", s3_secret_key)
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Monitor raw text files in MinIO (new arrivals only)
df = (
    spark.readStream.format("text")
    .option("path", s3_uri)
    .option("maxFilesPerTrigger", 1)
    .load()
    .withColumn("filename", input_file_name())
    .withColumn("detected_at", current_timestamp())
)

# Log new file arrivals
query = (
    df.writeStream.outputMode("append")
    .format("console")
    .option("truncate", False)
    .start()
)

query.awaitTermination()

spark.stop()
