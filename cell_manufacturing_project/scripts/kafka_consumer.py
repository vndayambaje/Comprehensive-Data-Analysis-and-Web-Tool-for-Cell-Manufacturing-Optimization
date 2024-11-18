import os
import json
import subprocess
from kafka import KafkaConsumer
from clickhouse_driver import Client

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

def consume_data():
    # Ensure ClickHouse is running before starting
    ensure_clickhouse_running()

    # Configure ClickHouse connection using environment variables
    client = Client(
        host=os.getenv('CLICKHOUSE_HOST', 'localhost'),
        port=int(os.getenv('CLICKHOUSE_PORT', 9000)),
        user=os.getenv('CLICKHOUSE_USER', 'default'),
        password='',
        database=os.getenv('CLICKHOUSE_DATABASE', 'default')
    )

    consumer = KafkaConsumer(
        'manufacturing_data',
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )

    # Create the table if it doesn't exist
    client.execute('''
        CREATE TABLE IF NOT EXISTS raw_data_table (
            timestamp String,
            stage String,
            temperature Float32,
            pressure Float32,
            material_usage Float32,
            process_time Float32,
            defect_rate Float32
        ) ENGINE = MergeTree() ORDER BY timestamp
    ''')

    latest_entry = None  # Variable to hold the latest entry

    for message in consumer:
        data = message.value
        try:
            # Store the latest entry only
            latest_entry = (
                data['timestamp'], data['stage'], data['temperature'],
                data['pressure'], data['material_usage'], data['process_time'], data['defect_rate']
            )

            # Insert only the latest entry into the database
            client.execute('INSERT INTO raw_data_table VALUES', [latest_entry])
            print(f"Inserted latest entry into 'raw_data_table': {latest_entry}")

        except Exception as e:
            print(f"Error processing data: {e}")

if __name__ == "__main__":
    consume_data()
