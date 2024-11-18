from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, col, min, max
from clickhouse_driver import Client
import os
import subprocess

def ensure_clickhouse_running():
    """Ensure ClickHouse server is running on port 9000."""
    try:
        # Check if the server is running by attempting to connect
        client = Client(host='localhost', port=9000)
        client.execute("SELECT 1")
    except Exception:
        print("ClickHouse server not running or not reachable. Attempting to start...")
        # Attempt to remove stale PID file if necessary
        pid_path = "/var/run/clickhouse-server/clickhouse-server.pid"
        if os.path.exists(pid_path):
            print(f"Removing stale PID file: {pid_path}")
            subprocess.run(["sudo", "rm", pid_path])

        # Start ClickHouse service
        subprocess.run(["sudo", "service", "clickhouse-server", "start"])

def create_processed_data_table_if_not_exists(client, table_name):
    # Create the processed_data_table in ClickHouse if it does not exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        stage String,
        avg_temperature Float32,
        avg_pressure Float32,
        avg_material_usage Float32,
        avg_process_time Float32,
        avg_defect_rate Float32,
        min_temperature Float32,
        max_temperature Float32,
        min_pressure Float32,
        max_pressure Float32,
        record_count UInt32
    ) ENGINE = MergeTree()
    ORDER BY stage
    """
    client.execute(create_table_query)
    print(f"Table '{table_name}' ensured in ClickHouse.")

def main():
    # Ensure ClickHouse is running before starting
    ensure_clickhouse_running()

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("Cell Manufacturing Analysis using ClickHouse Data") \
        .config("spark.jars", "/home/vic3/spark/clickhouse-jdbc-0.6.3-all.jar") \
        .getOrCreate()

    # ClickHouse connection parameters
    clickhouse_host = os.getenv('CLICKHOUSE_HOST', 'localhost')
    clickhouse_port = os.getenv('CLICKHOUSE_PORT', 9000)  # Native port for clickhouse_driver
    clickhouse_user = os.getenv('CLICKHOUSE_USER', 'default')
    clickhouse_database = os.getenv('CLICKHOUSE_DATABASE', 'default')

    # Create ClickHouse client for native connections
    client = Client(
        host=clickhouse_host,
        port=int(clickhouse_port),
        user=clickhouse_user,
        password='',
        database=clickhouse_database
    )

    # Ensure the processed_data_table exists
    table_name = 'processed_data_table'
    create_processed_data_table_if_not_exists(client, table_name)

    # Define the JDBC URL for Spark connection to ClickHouse on HTTP port
    jdbc_url = f"jdbc:clickhouse://{clickhouse_host}:8123/{clickhouse_database}"

    # Read data from the ClickHouse `raw_data_table` using `dbtable`
    try:
        raw_df = spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", "raw_data_table") \
            .option("driver", "com.clickhouse.jdbc.ClickHouseDriver") \
            .load()

        # Perform data processing and aggregation
        processed_df = raw_df.groupBy("stage").agg(
            avg("temperature").alias("avg_temperature"),
            avg("pressure").alias("avg_pressure"),
            avg("material_usage").alias("avg_material_usage"),
            avg("process_time").alias("avg_process_time"),
            avg("defect_rate").alias("avg_defect_rate"),
            min("temperature").alias("min_temperature"),
            max("temperature").alias("max_temperature"),
            min("pressure").alias("min_pressure"),
            max("pressure").alias("max_pressure"),
            count("*").alias("record_count")
        )

        # Write the processed data back to ClickHouse `processed_data_table`
        processed_df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("driver", "com.clickhouse.jdbc.ClickHouseDriver") \
            .mode("append") \
            .save()

        print("Data processed and saved successfully.")

    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    main()
