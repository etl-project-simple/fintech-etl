from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

def extract_data(spark: SparkSession,input_path: str):
        # read data from a CSV file using Spark  
    schema = StructType([
            StructField("transaction_id", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("amount", DoubleType(), True),
            StructField("payment_method", StringType(), True),
            StructField("timestamp", TimestampType(), True)
            ])
    return spark.read.option("header", "true").schema(schema).csv(input_path)
        
