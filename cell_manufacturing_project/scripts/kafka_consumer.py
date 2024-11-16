# scripts/kafka_consumer.py
from kafka import KafkaConsumer
import json
import pandas as pd
from clickhouse_driver import Client
import os

def consume_data():
    consumer = KafkaConsumer(
        'cell_data',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    client = Client('localhost')

    # Create ClickHouse table if not exists
    client.execute('''
        CREATE TABLE IF NOT EXISTS cell_data (
            timestamp String,
            temperature Float32,
            pressure Float32,
            material_usage Float32,
            process_time Int32,
            defect_rate Int8
        ) ENGINE = MergeTree() ORDER BY timestamp
    ''')

    data_lake_path = "../data/data_lake/"
    os.makedirs(data_lake_path, exist_ok=True)

    for message in consumer:
        data = message.value
        # Save raw data to the data lake
        raw_file = os.path.join(data_lake_path, f"{data['timestamp']}.json")
        with open(raw_file, 'w') as f:
            json.dump(data, f)

        # Insert processed data into ClickHouse
        client.execute(
            'INSERT INTO cell_data VALUES',
            [(data['timestamp'], data['temperature'], data['pressure'],
              data['material_usage'], data['process_time'], data['defect_rate'])]
        )

if __name__ == "__main__":
    consume_data()
