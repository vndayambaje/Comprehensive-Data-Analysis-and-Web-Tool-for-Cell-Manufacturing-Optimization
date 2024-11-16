# scripts/data_processing.py
import pandas as pd

def process_data(input_file="data/generated_data.csv", output_file="data/processed_data/processed_data.csv"):
    df = pd.read_csv(input_file)
    # Basic processing example: Filter out rows with high defect rates
    processed_df = df[df["defect_rate"] == 0]
    processed_df.to_csv(output_file, index=False)
    print(f"Processed data saved at {output_file}")

if __name__ == "__main__":
    process_data()
