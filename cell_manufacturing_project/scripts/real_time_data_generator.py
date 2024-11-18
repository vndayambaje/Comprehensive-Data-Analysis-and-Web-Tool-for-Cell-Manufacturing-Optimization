import random
import time
import json
import datetime
import os
from kafka import KafkaProducer  # Import Kafka producer (if you want to use Kafka)

def generate_data():
    # Create data lake directory if it doesn't exist
    data_lake_dir = os.path.join(os.path.dirname(__file__), '../data/data_lake')
    if not os.path.exists(data_lake_dir):
        os.makedirs(data_lake_dir)

    # Initialize Kafka producer (optional, requires Kafka setup)
    kafka_enabled = True  # Set to False if not using Kafka
    kafka_topic = 'manufacturing_data'
    producer = None
    if kafka_enabled:
        try:
            producer = KafkaProducer(
                bootstrap_servers='localhost:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except Exception as e:
            print(f"Error initializing Kafka producer: {e}")
            kafka_enabled = False

    while True:
        # Current timestamp
        timestamp = datetime.datetime.now().isoformat()

        # Simulated data for different stages
        data = {
            "timestamp": timestamp,
            "stage": random.choice(["Electrode Production", "Cell Assembly", "Cell Finishing"]),
            "temperature": round(random.uniform(20.0, 80.0), 2),
            "pressure": round(random.uniform(1.0, 10.0), 2),
            "material_usage": round(random.uniform(0.1, 5.0), 2),
            "process_time": round(random.uniform(0.5, 5.0), 2),
            "defect_rate": round(random.uniform(0, 1), 2)
        }

        # Write data to a file in data/data_lake
        file_path = os.path.join(data_lake_dir, 'real_time_data.json')
        with open(file_path, 'a') as file:
            file.write(json.dumps(data) + '\n')

        # Send data to Kafka topic (optional)
        if kafka_enabled and producer:
            try:
                producer.send(kafka_topic, data)
            except Exception as e:
                print(f"Error sending data to Kafka: {e}")

        # Print to console for debugging
        print(json.dumps(data))

        # Sleep for 30 seconds to simulate reduced data generation rate
        time.sleep(30)

if __name__ == "__main__":
    generate_data()
