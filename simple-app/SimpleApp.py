"""SimpleApp.py"""
import os
from pyspark.sql import SparkSession

s3_endpoint = os.environ["S3_ENDPOINT"]
s3_access_key = os.environ["S3_ACCESS_KEY"]
s3_secret_key = os.environ["S3_SECRET_KEY"]
s3_bucket = os.environ["S3_BUCKET"]
s3_file_path = os.environ["S3_FILE_PATH"] 

spark = SparkSession.builder \
    .appName("SimpleApp") \
    .config("spark.hadoop.fs.s3a.endpoint", s3_endpoint) \
    .config("spark.hadoop.fs.s3a.access.key", s3_access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", s3_secret_key) \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

s3_uri = f"s3a://{s3_bucket}/{s3_file_path}"
df = spark.read.option("header", "true").json(s3_uri)

df.show()
# numAs = logData.filter(logData.value.contains('a')).count()
# numBs = logData.filter(logData.value.contains('b')).count()

# print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

spark.stop()