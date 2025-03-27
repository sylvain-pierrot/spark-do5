import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, regexp_extract_all, udf
from pyspark.sql.types import ArrayType, StringType
import re

s3_endpoint = os.environ["S3_ENDPOINT"]
s3_access_key = os.environ["S3_ACCESS_KEY"]
s3_secret_key = os.environ["S3_SECRET_KEY"]
s3_bucket = os.environ["S3_BUCKET"]
s3_file_path = os.environ["S3_FILE_PATH"]

spark = SparkSession.builder \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .appName("WikipediaCategoryCounter") \
    .getOrCreate()
sc = spark.sparkContext

sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", s3_endpoint)
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", s3_access_key)
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", s3_secret_key)
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

s3_uri = f"s3a://{s3_bucket}/{s3_file_path}"
raw_df = spark.read.text(s3_uri)

category_pattern = r"\[\[Category:(.*?)\]\]"

@udf(ArrayType(StringType()))
def extract_categories(text):
    return re.findall(category_pattern, text)

df_with_categories = raw_df.withColumn("categories", extract_categories(col("value")))
exploded = df_with_categories.select(explode(col("categories")).alias("category"))
top_categories = exploded.groupBy("category").count().orderBy(col("count").desc()).limit(50)

top_categories.show(truncate=False)

spark.stop()