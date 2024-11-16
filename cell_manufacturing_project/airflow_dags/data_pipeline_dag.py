# airflow_dags/data_pipeline_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from scripts.data_processing import insert_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

with DAG('cell_data_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    ingest_task = PythonOperator(task_id='ingest_data', python_callable=insert_data)
