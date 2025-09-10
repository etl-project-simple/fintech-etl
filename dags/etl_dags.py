# dags/etl_dags.py
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"owner": "airflow", "retries": 0}

with DAG(
    dag_id="etl_fintech",
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    schedule="@daily",
    catchup=False,
    tags=["fintech", "pyspark", "redshift"],
):
    run_etl = BashOperator(
        task_id="run_pyspark_etl",
        bash_command="python -m etl.main",
        env={
            "ENV_FILE": "/opt/airflow/.env",
            "PYTHONPATH": "/opt/airflow", 
        },
    )
    run_etl