"""SimpleApp.py"""

import os
from pyspark.sql import SparkSession

s3_endpoint = os.environ["S3_ENDPOINT"]
s3_access_key = os.environ["S3_ACCESS_KEY"]
s3_secret_key = os.environ["S3_SECRET_KEY"]
s3_bucket = os.environ["S3_BUCKET"]
s3_file_path = os.environ["S3_FILE_PATH"]

spark = (
    SparkSession.builder.config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    )
    .appName("SimpleApp")
    .getOrCreate()
)
sc = spark.sparkContext

sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", s3_endpoint)
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", s3_access_key)
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", s3_secret_key)
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "true")
sc._jsc.hadoopConfiguration().set(
    "fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
)
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "true")

s3_uri = f"s3a://{s3_bucket}/{s3_file_path}"
df = spark.read.text(s3_uri)

df.show()

spark.stop()
