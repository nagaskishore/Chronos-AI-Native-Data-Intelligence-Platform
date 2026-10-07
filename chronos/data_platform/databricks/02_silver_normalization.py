# Databricks notebook source
dbutils.fs.mkdirs("/Volumes/workspace/default/chronos/silver")

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import *
from functools import reduce

PROJECT_NAME = "chronos"

BRONZE_BASE = "/Volumes/workspace/default/chronos/bronze"
SILVER_BASE = "/Volumes/workspace/default/chronos/silver"

print(PROJECT_NAME)

# COMMAND ----------

vendor_a_v1 = (
    spark.read
    .format("delta")
    .load(f"{BRONZE_BASE}/vendor_a_v1")
)

display(vendor_a_v1)

# COMMAND ----------

vendor_a_v2 = (
    spark.read
    .format("delta")
    .load(f"{BRONZE_BASE}/vendor_a_v2")
)

display(vendor_a_v2)

# COMMAND ----------

vendor_b = (
    spark.read
    .format("delta")
    .load(f"{BRONZE_BASE}/vendor_b")
)

display(vendor_b)

# COMMAND ----------

vendor_c = (
    spark.read
    .format("delta")
    .load(f"{BRONZE_BASE}/vendor_c")
)

display(vendor_c)

# COMMAND ----------

vendor_a_v1_silver = (
    vendor_a_v1
    .select(
        F.col("vendor_record_id").alias("record_id"),
        F.lit("vendor_a").alias("vendor"),
        F.col("ticker"),
        F.to_timestamp("event_date", "yyyy-MM-dd").alias("event_time"),
        F.col("revenue").cast("double").alias("revenue"),
        F.col("currency"),
        F.col("status"),
        F.col("_source_file").alias("source_file"),
        F.col("_batch_id").alias("batch_id"),
        F.col("_ingestion_timestamp").alias("ingestion_timestamp")
    )
)

display(vendor_a_v1_silver)

# COMMAND ----------

F.to_timestamp("event_date", "yyyy-MM-dd")

# COMMAND ----------

vendor_a_v2_silver = (
    vendor_a_v2
    .select(
        F.col("vendor_record_id").alias("record_id"),
        F.lit("vendor_a").alias("vendor"),
        F.col("ticker"),
        F.to_timestamp("eventDate", "yyyy/MM/dd").alias("event_time"),
        F.col("revenue_amount").cast("double").alias("revenue"),
        F.col("currency"),
        F.col("status"),
        F.col("_source_file").alias("source_file"),
        F.col("_batch_id").alias("batch_id"),
        F.col("_ingestion_timestamp").alias("ingestion_timestamp")
    )
)

display(vendor_a_v2_silver)

# COMMAND ----------

vendor_b_silver = (
    vendor_b
    .select(
        F.col("record_id"),
        F.lit("vendor_b").alias("vendor"),
        F.col("security").alias("ticker"),
        F.to_timestamp("trade_date", "MM-dd-yyyy").alias("event_time"),
        F.col("amount").cast("double").alias("revenue"),
        F.col("ccy").alias("currency"),
        F.lit("ACTIVE").alias("status"),
        F.col("_source_file").alias("source_file"),
        F.col("_batch_id").alias("batch_id"),
        F.col("_ingestion_timestamp").alias("ingestion_timestamp")
    )
)

display(vendor_b_silver)

# COMMAND ----------

vendor_c_silver = (
    vendor_c
    .select(
        F.col("id").alias("record_id"),
        F.lit("vendor_c").alias("vendor"),
        F.col("symbol").alias("ticker"),
        F.to_timestamp(
            "business_date",
            "yyyy-MM-dd'T'HH:mm:ssX"
        ).alias("event_time"),
        F.col("value").cast("double").alias("revenue"),
        F.col("currency_code").alias("currency"),
        F.lit("ACTIVE").alias("status"),
        F.col("_source_file").alias("source_file"),
        F.col("_batch_id").alias("batch_id"),
        F.col("_ingestion_timestamp").alias("ingestion_timestamp")
    )
)

display(vendor_c_silver)

# COMMAND ----------

silver_df = (
    vendor_a_v1_silver
    .unionByName(vendor_a_v2_silver)
    .unionByName(vendor_b_silver)
    .unionByName(vendor_c_silver)
)

display(silver_df)

# COMMAND ----------

silver_df.printSchema()

# COMMAND ----------

display(
    silver_df
    .groupBy("vendor")
    .count()
    .orderBy("vendor")
)

# COMMAND ----------

display(
    silver_df
    .groupBy("vendor")
    .count()
    .orderBy("vendor")
)

# COMMAND ----------

display(
    silver_df
    .groupBy("ticker")
    .count()
    .orderBy("ticker")
)

# COMMAND ----------

display(
    silver_df
    .select(
        "vendor",
        "record_id",
        "ticker",
        "event_time"
    )
    .orderBy("event_time")
)

# COMMAND ----------

display(
    silver_df.select(
        "record_id",
        "vendor",
        "ticker",
        "revenue",
        "source_file",
        "batch_id",
        "ingestion_timestamp"
    )
)

# COMMAND ----------

(
    silver_df
    .write
    .format("delta")
    .mode("overwrite")
    .save(f"{SILVER_BASE}/vendor_events")
)

# COMMAND ----------

silver_check = (
    spark.read
    .format("delta")
    .load(f"{SILVER_BASE}/vendor_events")
)

display(silver_check)

# COMMAND ----------

print("Silver record count:", silver_check.count())

# COMMAND ----------

