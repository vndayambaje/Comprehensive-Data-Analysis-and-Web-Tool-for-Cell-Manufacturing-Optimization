# scripts/data_generation.py
import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_records=100000):
    np.random.seed(42)
    timestamps = pd.date_range(start="2024-01-01", periods=num_records, freq="S")
    data = {
        "timestamp": timestamps,
        "temperature": np.random.uniform(20, 100, size=num_records),
        "pressure": np.random.uniform(1, 10, size=num_records),
        "material_usage": np.random.uniform(0, 1, size=num_records),
        "process_time": np.random.randint(5, 500, size=num_records),
        "defect_rate": np.random.choice([0, 1], size=num_records, p=[0.95, 0.05])  # 5% defect rate
    }
    df = pd.DataFrame(data)
    output_path = os.path.join("..", "data", "generated_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Data generated at {output_path}")

if __name__ == "__main__":
    generate_synthetic_data()
