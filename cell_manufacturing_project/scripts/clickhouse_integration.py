import os
from clickhouse_driver import Client

class ClickHouseIntegration:
    def __init__(self, host='localhost', port=9000, user=None, password=None, database='default'):
        """
        Initializes the ClickHouse client. Default credentials can be overridden with environment variables.
        """
        self.client = Client(
            host=host, 
            port=port, 
            user=user or os.getenv('CLICKHOUSE_USER', 'default'), 
            password='', 
            database=database
        )

    def create_table(self, table_name):
        """
        Creates a table in ClickHouse for storing manufacturing data.
        """
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            timestamp DateTime,
            stage String,
            temperature Float32,
            pressure Float32,
            material_usage Float32,
            process_time Float32,
            defect_rate Float32
        ) ENGINE = MergeTree()
        ORDER BY timestamp;
        """
        self.client.execute(create_query)
        print(f"Table '{table_name}' created or already exists.")

    def insert_data(self, table_name, data):
        """
        Inserts data into the specified ClickHouse table.
        """
        if data:
            insert_query = f"INSERT INTO {table_name} (timestamp, stage, temperature, pressure, material_usage, process_time, defect_rate) VALUES"
            try:
                self.client.execute(insert_query, data)
                print(f"Inserted {len(data)} rows into '{table_name}'.")
            except Exception as e:
                print(f"Failed to insert data into '{table_name}': {e}")

    def query_data(self, query):
        """
        Executes a query and returns results.
        """
        try:
            result = self.client.execute(query)
            return result
        except Exception as e:
            print(f"Failed to execute query: {e}")
            return None

if __name__ == "__main__":
    # Example usage (for testing purposes)
    clickhouse = ClickHouseIntegration(
        host='localhost', 
        port=9000, 
        user=os.getenv('CLICKHOUSE_USER', 'default'), 
        password=os.getenv('CLICKHOUSE_PASSWORD', ''), 
        database='default'
    )
    table_name = 'cell_manufacturing_data'
    clickhouse.create_table(table_name)
