from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/data', methods=['GET'])
def get_data():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.abspath(os.path.join(base_dir, '../../data/processed_data/processed_data.csv'))
        if not os.path.exists(data_file_path):
            return jsonify({"error": f"Processed data file not found at {data_file_path}"}), 404
        df = pd.read_csv(data_file_path)
        if df.empty:
            return jsonify({"message": "The data file is empty"}), 200
        data = df.head(100).to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Welcome to the Data API. Access /data to retrieve data."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
