from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, sum as _sum, avg as _avg, max as _max, to_date

def transform_data(df: DataFrame) -> dict:
      # dim_user
    dim_user = (
        df.groupBy("user_id")
        .agg(
            count("*").cast("int").alias("total_transactions"),
            _sum("amount").cast("double").alias("total_amount"),
            _avg("amount").cast("double").alias("average_amount"),
            _max("timestamp").alias("last_transaction")
        )
    )
    
    # dim_payment_method
    dim_payment_method = (
        df.groupBy("payment_method")
        .agg(
            count("*").cast("int").alias("total_transactions"),
            _sum("amount").cast("double").alias("total_amount"),
            _avg("amount").cast("double").alias("average_amount")
        )
    )

    # fact_transactions
    fact_transactions = (
        df.withColumn("transaction_date", to_date(col("timestamp")))
        .groupBy("transaction_date", "payment_method")
        .agg(
            count("*").cast("int").alias("total_transactions"),
            _sum("amount").cast("double").alias("total_amount"),
            _avg("amount").cast("double").alias("average_amount")
        )
    )
    return {
        "dim_user": dim_user,
        "dim_payment_method": dim_payment_method,
        "fact_transactions": fact_transactions
    }
   