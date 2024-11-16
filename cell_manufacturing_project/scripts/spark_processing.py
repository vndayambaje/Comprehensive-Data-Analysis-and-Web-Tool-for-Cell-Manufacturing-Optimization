# scripts/spark_processing.py
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Cell Manufacturing Analysis") \
    .getOrCreate()

df = spark.read.format("jdbc").options(
    url="jdbc:clickhouse://localhost:8123/default",
    driver="ru.yandex.clickhouse.ClickHouseDriver",
    dbtable="cell_data",
    user="default",
    password=""
).load()

# Example Transformation
df.createOrReplaceTempView("cell_data")
defect_analysis = spark.sql("SELECT * FROM cell_data WHERE defect_rate = 1")
defect_analysis.show()
