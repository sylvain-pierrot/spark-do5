from pyspark.sql import SparkSession
import os

url = os.getenv("NEO4J_URL", "neo4j://neo4j.neo4j.svc.cluster.local:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "gNi2hv5rzQtq1r")
dbname = os.getenv("NEO4J_DATABASE", "neo4j")

spark = (
    SparkSession.builder.config("neo4j.url", url)
    .config("neo4j.authentication.basic.username", username)
    .config("neo4j.authentication.basic.password", password)
    .config("neo4j.database", dbname)
    .getOrCreate()
)

(spark.read.format("org.neo4j.spark.DataSource").option("labels", "User").load().show())

spark.stop()
