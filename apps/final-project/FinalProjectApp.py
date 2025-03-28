import os
from pyspark.sql import SparkSession

url = os.environ["NEO4J_URL"]
username = os.environ["NEO4J_USERNAME"]
password = os.environ["NEO4J_PASSWORD"]
dbname = os.environ["NEO4J_DATABASE"]

spark = (
    SparkSession.builder.config("neo4j.url", url)
    .config("neo4j.authentication.basic.username", username)
    .config("neo4j.authentication.basic.password", password)
    .config("neo4j.database", dbname)
    .getOrCreate()
)

df = (
    spark.read.format("org.neo4j.spark.DataSource")
    .option("query", """
        MATCH (:Client:FirstPartyFraudster)-[]-(txn:Transaction)-[]-(c:Client)
        WHERE NOT c:FirstPartyFraudster
        UNWIND labels(txn) AS transactionType
        RETURN transactionType, count(*) AS frequency
        ORDER BY frequency DESC
    """)
    .load()
)

df.show(truncate=False)

spark.stop()