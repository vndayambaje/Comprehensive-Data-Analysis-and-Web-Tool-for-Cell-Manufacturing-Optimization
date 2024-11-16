# scripts/data_generation.py
from kafka import KafkaProducer
import pandas as pd
import json
import time

def produce_data():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    df = pd.read_csv("../data/generated_data.csv")
    for index, row in df.iterrows():
        message = row.to_dict()
        producer.send('cell_data', value=message)
        time.sleep(0.001)  # Simulating 1000Hz data stream
    producer.close()

if __name__ == "__main__":
    produce_data()
