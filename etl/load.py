# etl/load.py
import os
import logging
from typing import Dict

from dotenv import load_dotenv
from pyspark.sql import DataFrame
import psycopg2


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Đọc ENV từ biến ENV_FILE (do DAG set), fallback về /opt/airflow/.env
load_dotenv(os.getenv("ENV_FILE", "/opt/airflow/.env"))

# AWS & S3
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
S3_BUCKET  = os.getenv("AWS_S3_BUCKET")          # vd: my-bucket
S3_PREFIX  = os.getenv("AWS_S3_PREFIX", "dwh")   # vd: dwh

# Redshift
REDSHIFT_HOST = os.getenv("REDSHIFT_HOST")
REDSHIFT_PORT = int(os.getenv("REDSHIFT_PORT", "5439"))
REDSHIFT_DB   = os.getenv("REDSHIFT_DB")
REDSHIFT_USER = os.getenv("REDSHIFT_USER")
REDSHIFT_PWD  = os.getenv("REDSHIFT_PASSWORD")
REDSHIFT_IAM_ROLE_ARN = os.getenv("REDSHIFT_IAM_ROLE_ARN")
REDSHIFT_SCHEMA = os.getenv("REDSHIFT_SCHEMA", "public")


def _rs_conn():
    return psycopg2.connect(
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT,
        dbname=REDSHIFT_DB,
        user=REDSHIFT_USER,
        password=REDSHIFT_PWD,
    )


def _copy_sql(table: str, s3_uri: str) -> str:
    # COPY từ S3 (Parquet) vào Redshift qua IAM Role
    return f"""
        COPY {REDSHIFT_SCHEMA}.{table}
        FROM '{s3_uri}'
        IAM_ROLE '{REDSHIFT_IAM_ROLE_ARN}'
        FORMAT AS PARQUET
        REGION '{AWS_REGION}';
    """


def load_to_s3_and_redshift(tables: Dict[str, DataFrame], *, coalesce_n: int = 8) -> None:
    """
    tables: dict tên_bảng -> DataFrame đã transform
    - Ghi Parquet lên S3 (s3a://) để Spark ghi
    - COPY từ S3 (s3://) vào Redshift
    """
    if not S3_BUCKET:
        raise RuntimeError("Missing env AWS_S3_BUCKET")

   
    s3a_base = f"s3a://{S3_BUCKET}/{S3_PREFIX}"  # cho Spark writer
    s3_base  = f"s3://{S3_BUCKET}/{S3_PREFIX}"   # cho Redshift COPY

    # 1) Ghi Parquet lên S3
    for name, df in tables.items():
        path = f"{s3a_base}/{name}"
        df.coalesce(1).write.mode("overwrite").parquet(path)
        log.info("Wrote %s → %s", name, path)

    # 2) COPY vào Redshift
    with _rs_conn() as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            for name in tables.keys():
                cur.execute(f"TRUNCATE TABLE {REDSHIFT_SCHEMA}.{name};")
                cur.execute(_copy_sql(name, f"{s3_base}/{name}"))
                log.info("Loaded %s → %s.%s", name, REDSHIFT_SCHEMA, name)
