from pyspark.sql import SparkSession

url = "neo4j://neo4j.neo4j.svc.cluster.local:7687"
username = "neo4j"
password = "gNi2hv5rzQtq1r"
dbname = "neo4j"

spark = (
    SparkSession.builder.config("neo4j.url", url)
    .config("neo4j.authentication.basic.username", username)
    .config("neo4j.authentication.basic.password", password)
    .config("neo4j.database", dbname)
    .getOrCreate()
)

(
    spark.read.format("org.neo4j.spark.DataSource")
    .option("labels", "User")
    .load()
    .show()
)

spark.stop()