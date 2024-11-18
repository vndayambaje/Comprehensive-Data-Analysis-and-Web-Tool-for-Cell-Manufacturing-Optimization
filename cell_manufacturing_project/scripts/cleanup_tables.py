from clickhouse_driver import Client

def cleanup_tables():
    """
    Connects to ClickHouse and empties the specified tables.
    """
    try:
        # Initialize ClickHouse client without a password
        client = Client(
            host='localhost',
            port=9000,
            user='default',
            database='default'
        )

        # Specify the tables to clean up
        tables_to_cleanup = ['raw_data_table', 'processed_data_table', 'cell_manufacturing_data', 'cell_data']

        for table in tables_to_cleanup:
            try:
                query = f"TRUNCATE TABLE IF EXISTS {table}"
                client.execute(query)
                print(f"Successfully cleaned up table '{table}'.")
            except Exception as e:
                print(f"Error cleaning up table '{table}': {e}")

    except Exception as main_e:
        print(f"Failed to connect to ClickHouse: {main_e}")

if __name__ == "__main__":
    cleanup_tables()
