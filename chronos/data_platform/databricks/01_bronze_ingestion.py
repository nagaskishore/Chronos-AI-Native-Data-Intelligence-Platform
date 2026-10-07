# Databricks notebook source
dbutils.fs.mkdirs("/Volumes/workspace/default/chronos/input/vendor_a")
dbutils.fs.mkdirs("/Volumes/workspace/default/chronos/input/vendor_b")
dbutils.fs.mkdirs("/Volumes/workspace/default/chronos/input/vendor_c")
dbutils.fs.mkdirs("/Volumes/workspace/default/chronos/bronze")


# COMMAND ----------

# ============================================================
# Chronos - Bronze Ingestion
# ============================================================

from pyspark.sql import functions as F
from pyspark.sql.types import *
from datetime import datetime
import uuid

PROJECT_NAME = "chronos"

#INPUT_BASE = "/FileStore/chronos/input"
#BRONZE_BASE = "/FileStore/chronos/bronze"

INPUT_BASE = "/Volumes/workspace/default/chronos/input"
BRONZE_BASE = "/Volumes/workspace/default/chronos/bronze"


BATCH_ID = str(uuid.uuid4())

print(f"Project : {PROJECT_NAME}")
print(f"Batch ID: {BATCH_ID}")

# COMMAND ----------

vendor_a_v1_path = f"{INPUT_BASE}/vendor_a/vendor_a_v1.json"
vendor_a_v2_path = f"{INPUT_BASE}/vendor_a/vendor_a_v2.json"

vendor_b_path = f"{INPUT_BASE}/vendor_b/vendor_b.csv"

vendor_c_path = f"{INPUT_BASE}/vendor_c/vendor_c.json"

print(vendor_a_v1_path)
print(vendor_a_v2_path)
print(vendor_b_path)
print(vendor_c_path)

# COMMAND ----------

display(dbutils.fs.ls(INPUT_BASE))

# COMMAND ----------

display(dbutils.fs.ls(f"{INPUT_BASE}/vendor_a"))

# COMMAND ----------

vendor_a_v1_raw = (
    spark.read
    .option("multiLine", "true")
    .json(vendor_a_v1_path)
)

display(vendor_a_v1_raw)

# COMMAND ----------

vendor_a_v2_raw = (
    spark.read
    .option("multiLine", "true")
    .json(vendor_a_v2_path)
)

display(vendor_a_v2_raw)

# COMMAND ----------

vendor_b_raw = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(vendor_b_path)
)

display(vendor_b_raw)

# COMMAND ----------

vendor_c_raw = (
    spark.read
    .option("multiLine", "true")
    .json(vendor_c_path)
)

display(vendor_c_raw)

# COMMAND ----------

def add_bronze_metadata(df, vendor, source_file):

    return (
        df
        .withColumn("_vendor", F.lit(vendor))
        .withColumn("_source_file", F.lit(source_file))
        .withColumn("_batch_id", F.lit(BATCH_ID))
        .withColumn("_ingestion_timestamp", F.current_timestamp())
    )

# COMMAND ----------

vendor_a_v1_bronze = add_bronze_metadata(
    vendor_a_v1_raw,
    "vendor_a",
    "vendor_a_v1.json"
)

display(vendor_a_v1_bronze)

# COMMAND ----------

vendor_a_v2_bronze = add_bronze_metadata(
    vendor_a_v2_raw,
    "vendor_a",
    "vendor_a_v2.json"
)

display(vendor_a_v2_bronze)

# COMMAND ----------

vendor_a_v2_bronze = add_bronze_metadata(
    vendor_a_v2_raw,
    "vendor_a",
    "vendor_a_v2.json"
)

display(vendor_a_v2_bronze)

# COMMAND ----------

vendor_b_bronze = add_bronze_metadata(
    vendor_b_raw,
    "vendor_b",
    "vendor_b.csv"
)

display(vendor_b_bronze)

# COMMAND ----------

vendor_c_bronze = add_bronze_metadata(
    vendor_c_raw,
    "vendor_c",
    "vendor_c.json"
)

display(vendor_c_bronze)

# COMMAND ----------

(
    vendor_a_v1_bronze
    .write
    .format("delta")
    .mode("append")
    .save(f"{BRONZE_BASE}/vendor_a_v1")
)

# COMMAND ----------

(
    vendor_a_v2_bronze
    .write
    .format("delta")
    .mode("append")
    .save(f"{BRONZE_BASE}/vendor_a_v2")
)

# COMMAND ----------

(
    vendor_b_bronze
    .write
    .format("delta")
    .mode("append")
    .save(f"{BRONZE_BASE}/vendor_b")
)

# COMMAND ----------

(
    vendor_c_bronze
    .write
    .format("delta")
    .mode("append")
    .save(f"{BRONZE_BASE}/vendor_c")
)

# COMMAND ----------

display(dbutils.fs.ls(BRONZE_BASE))

# COMMAND ----------

bronze_vendor_b = (
    spark.read
    .format("delta")
    .load(f"{BRONZE_BASE}/vendor_b")
)

display(bronze_vendor_b)

# COMMAND ----------

print("Vendor A v1:", vendor_a_v1_bronze.count())
print("Vendor A v2:", vendor_a_v2_bronze.count())
print("Vendor B   :", vendor_b_bronze.count())
print("Vendor C   :", vendor_c_bronze.count())

# COMMAND ----------

display(
    vendor_b_bronze
    .groupBy("record_id")
    .count()
    .filter(F.col("count") > 1)
)

# COMMAND ----------

bronze_summary = spark.createDataFrame(
    [
        ("vendor_a", "vendor_a_v1.json", vendor_a_v1_bronze.count()),
        ("vendor_a", "vendor_a_v2.json", vendor_a_v2_bronze.count()),
        ("vendor_b", "vendor_b.csv", vendor_b_bronze.count()),
        ("vendor_c", "vendor_c.json", vendor_c_bronze.count())
    ],
    ["vendor", "source_file", "record_count"]
)

display(bronze_summary)

# COMMAND ----------

