from clickhouse_driver import Client
import os

def monitor_data():
    client = Client(host='localhost', port=9000)
    # Fetch the latest raw data and processed data
    raw_data_query = "SELECT * FROM raw_data_table ORDER BY timestamp DESC LIMIT 5"
    processed_data_query = "SELECT * FROM processed_data_table"
    
    raw_data = client.execute(raw_data_query)
    processed_data = {row[0]: row for row in client.execute(processed_data_query)}

    alerts = []
    for row in raw_data:
        stage, temp, pressure, *_ = row[1:]  # Adjust according to schema
        avg_data = processed_data.get(stage)
        if avg_data:
            avg_temp, avg_pressure, *_ = avg_data[1:]
            if abs(temp - avg_temp) > 0.05 * avg_temp:
                alerts.append(f"Temperature deviation in stage {stage}: {temp} vs avg {avg_temp}")
            if abs(pressure - avg_pressure) > 0.05 * avg_pressure:
                alerts.append(f"Pressure deviation in stage {stage}: {pressure} vs avg {avg_pressure}")
    
    if alerts:
        for alert in alerts:
            print(alert)

if __name__ == "__main__":
    monitor_data()
