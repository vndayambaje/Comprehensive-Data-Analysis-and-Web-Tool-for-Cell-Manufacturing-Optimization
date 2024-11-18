from flask import Flask, jsonify
from flask_cors import CORS
from clickhouse_driver import Client
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Environment variables for ClickHouse credentials
clickhouse_host = os.getenv('CLICKHOUSE_HOST', 'localhost')
clickhouse_port = int(os.getenv('CLICKHOUSE_PORT', 9000))
clickhouse_user = os.getenv('CLICKHOUSE_USER', 'default')
clickhouse_database = os.getenv('CLICKHOUSE_DATABASE', 'default')

def get_clickhouse_client():
    """Create and return a new ClickHouse client instance without a password."""
    try:
        client = Client(
            host=clickhouse_host,
            port=clickhouse_port,
            user=clickhouse_user,
            database=clickhouse_database
        )
        return client
    except Exception as e:
        print(f"Failed to connect to ClickHouse: {e}")
        return None

@app.route('/api/raw_data', methods=['GET'])
def get_raw_data():
    clickhouse_client = get_clickhouse_client()
    if not clickhouse_client:
        return jsonify({"error": "ClickHouse connection not established"}), 500
    try:
        query = "SELECT * FROM raw_data_table ORDER BY timestamp DESC LIMIT 100"
        rows = clickhouse_client.execute(query)
        if not rows:
            return jsonify({"message": "No raw data available"}), 200
        column_names = ["timestamp", "stage", "temperature", "pressure", "material_usage", "process_time", "defect_rate"]
        data = [dict(zip(column_names, row)) for row in rows]
        return jsonify(data), 200
    except Exception as e:
        print(f"Error fetching raw data: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        clickhouse_client.disconnect()

@app.route('/api/processed_data', methods=['GET'])
def get_processed_data():
    clickhouse_client = get_clickhouse_client()
    if not clickhouse_client:
        return jsonify({"error": "ClickHouse connection not established"}), 500
    try:
        query = "SELECT * FROM processed_data_table ORDER BY stage ASC LIMIT 100"
        rows = clickhouse_client.execute(query)
        if not rows:
            return jsonify({"message": "No processed data available"}), 200
        column_names = ["stage", "avg_temperature", "avg_pressure", "avg_material_usage", "avg_process_time", 
                        "avg_defect_rate", "min_temperature", "max_temperature", "min_pressure", "max_pressure", "record_count"]
        data = [dict(zip(column_names, row)) for row in rows]
        return jsonify(data), 200
    except Exception as e:
        print(f"Error fetching processed data: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        clickhouse_client.disconnect()

@app.route('/')
def home():
    return "Welcome to the Data API. Access /api/raw_data and /api/processed_data to retrieve data."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
