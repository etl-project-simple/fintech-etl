# etl/etl.py
import os, time
from pyspark.sql import SparkSession
from dotenv import load_dotenv

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_to_s3_and_redshift

if __name__ == "__main__":
    load_dotenv(os.getenv("ENV_FILE", "/opt/airflow/.env"))

    spark = SparkSession.builder \
    .appName("Fintech_ETL_Local_to_S3_Redshift") \
    .config("spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,"
            "com.amazonaws:aws-java-sdk-bundle:1.12.262") \
    .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID")) \
    .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY")) \
    .config("spark.hadoop.fs.s3a.endpoint", f"s3.{os.getenv('AWS_REGION')}.amazonaws.com") \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
    .config("spark.hadoop.mapreduce.outputcommitter.factory.scheme.s3a",
        "org.apache.hadoop.mapreduce.lib.output.FileOutputCommitterFactory") \
    .config("spark.hadoop.fs.s3a.committer.name", "directory") \
    .config("spark.hadoop.fs.s3a.committer.magic.enabled", "false") \
    .getOrCreate()

    start = time.time()
    input_path = os.getenv("INPUT_PATH", "/opt/airflow/data/transactions_1M.csv")

    print(f"[INFO] Reading data from {input_path}")
    df_raw = extract_data(spark, input_path).repartition(8).cache()
    print("INPUT rows total:", df_raw.count())

    df_transformed = transform_data(df_raw)
    for table_name, df in df_transformed.items():
        print(f"\n===== Table: {table_name} =====")
        df.show(5, truncate=False)

    print("✅ Transformed data successfully!")
    df_processed = load_to_s3_and_redshift(df_transformed, coalesce_n=8)

    print(f"[INFO] ETL finished in {time.time() - start:.2f}s")
    spark.stop()
