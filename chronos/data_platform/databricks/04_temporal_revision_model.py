# Databricks notebook source


# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable

SILVER_PATH = "/Volumes/workspace/default/chronos/silver/vendor_events"

TEMPORAL_BASE = "/Volumes/workspace/default/chronos/temporal"
TEMPORAL_PATH = f"{TEMPORAL_BASE}/vendor_events_history"

print("Silver:", SILVER_PATH)
print("Temporal:", TEMPORAL_PATH)

# COMMAND ----------

silver_df = spark.read.format("delta").load(SILVER_PATH)

silver_df.select(
    "record_id",
    "vendor",
    "ticker",
    "event_time",
    "revenue",
    "currency",
    "status",
    "source_file",
    "batch_id",
    "ingestion_timestamp"
).show(20, truncate=False)

# COMMAND ----------

DQ_FINAL_PATH = "/Volumes/workspace/default/chronos/dq/final"

dq_df = spark.read.format("delta").load(DQ_FINAL_PATH)

valid_df = dq_df.filter(
    F.col("dq_status") == "VALID"
)

print("Valid records:", valid_df.count())

# COMMAND ----------

temporal_df = (
    valid_df
    .withColumn(
        "event_time",
        F.to_timestamp("event_time")
    )
    .withColumn(
        "ingestion_timestamp",
        F.to_timestamp("ingestion_timestamp")
    )
    .withColumn(
        "temporal_key",
        F.concat_ws(
            "||",
            F.col("vendor"),
            F.col("ticker"),
            F.date_format("event_time", "yyyy-MM-dd HH:mm:ss")
        )
    )
)

temporal_df.select(
    "temporal_key",
    "vendor",
    "ticker",
    "event_time",
    "revenue",
    "ingestion_timestamp"
).show(20, truncate=False)

# COMMAND ----------

temporal_df = temporal_df.withColumn(
    "knowledge_time",
    F.col("ingestion_timestamp")
)

# COMMAND ----------

revision_window = (
    Window
    .partitionBy("temporal_key")
    .orderBy(
        F.col("knowledge_time").asc(),
        F.col("ingestion_timestamp").asc()
    )
)

temporal_df = temporal_df.withColumn(
    "record_version",
    F.row_number().over(revision_window)
)

# COMMAND ----------

temporal_df = temporal_df.withColumn(
    "valid_from",
    F.col("knowledge_time")
)

# COMMAND ----------

temporal_df = temporal_df.withColumn(
    "valid_to",
    F.lead("knowledge_time").over(revision_window)
)

# COMMAND ----------

temporal_df = temporal_df.withColumn(
    "is_current",
    F.col("valid_to").isNull()
)

# COMMAND ----------

temporal_df.filter(
    F.col("is_current") == True
).show(truncate=False)

# COMMAND ----------

temporal_history_df = temporal_df.select(
    "record_id",
    "vendor",
    "ticker",
    "event_time",
    "revenue",
    "currency",
    "status",

    "knowledge_time",
    "ingestion_timestamp",

    "valid_from",
    "valid_to",

    "record_version",
    "is_current",

    "source_file",
    "batch_id",

    "temporal_key"
)

# COMMAND ----------

temporal_history_df.orderBy(
    "ticker",
    "event_time",
    "knowledge_time"
).show(50, truncate=False)

# COMMAND ----------

(
    temporal_history_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(TEMPORAL_PATH)
)

print("Temporal history written to:")
print(TEMPORAL_PATH)

# COMMAND ----------

revision_demo = [
    (
        "A-REV-001",
        "vendor_a",
        "AAPL",
        "2026-01-05 00:00:00",
        125000.0,
        "USD",
        "ACTIVE",
        "2026-01-05 10:00:00",
        "2026-01-05 10:05:00",
        "revision_demo_v1"
    ),
    (
        "A-REV-002",
        "vendor_a",
        "AAPL",
        "2026-01-05 00:00:00",
        130000.0,
        "USD",
        "ACTIVE",
        "2026-01-10 09:00:00",
        "2026-01-10 09:05:00",
        "revision_demo_v2"
    )
]

revision_schema = [
    "record_id",
    "vendor",
    "ticker",
    "event_time",
    "revenue",
    "currency",
    "status",
    "knowledge_time",
    "ingestion_timestamp",
    "source_file"
]

revision_df = spark.createDataFrame(
    revision_demo,
    revision_schema
)

revision_df = (
    revision_df
    .withColumn("event_time", F.to_timestamp("event_time"))
    .withColumn("knowledge_time", F.to_timestamp("knowledge_time"))
    .withColumn("ingestion_timestamp", F.to_timestamp("ingestion_timestamp"))
)

# COMMAND ----------

revision_df = revision_df.withColumn(
    "temporal_key",
    F.concat_ws(
        "||",
        F.col("vendor"),
        F.col("ticker"),
        F.date_format("event_time", "yyyy-MM-dd HH:mm:ss")
    )
)

# COMMAND ----------

revision_window = (
    Window
    .partitionBy("temporal_key")
    .orderBy(
        F.col("knowledge_time").asc(),
        F.col("ingestion_timestamp").asc()
    )
)

# COMMAND ----------

revision_history_df = (
    revision_df
    .withColumn(
        "record_version",
        F.row_number().over(revision_window)
    )
    .withColumn(
        "valid_from",
        F.col("knowledge_time")
    )
    .withColumn(
        "valid_to",
        F.lead("knowledge_time").over(revision_window)
    )
    .withColumn(
        "is_current",
        F.col("valid_to").isNull()
    )
)

# COMMAND ----------

revision_history_df.orderBy(
    "knowledge_time"
).show(truncate=False)

# COMMAND ----------

#as_of_time = "2026-01-07 12:00:00"
#as_of_time = "2026-01-07 12:00:00"
as_of_time = "2026-01-12 12:00:00"

as_of_df = revision_history_df.filter(
    (F.col("valid_from") <= F.to_timestamp(F.lit(as_of_time))) &
    (
        F.col("valid_to").isNull() |
        (F.col("valid_to") > F.to_timestamp(F.lit(as_of_time)))
    )
)

as_of_df.select(
    "ticker",
    "event_time",
    "revenue",
    "record_version",
    "knowledge_time",
    "valid_from",
    "valid_to"
).show(truncate=False)

as_of_df = revision_history_df.filter(
    (F.col("valid_from") <= F.to_timestamp(F.lit(as_of_time))) &
    (
        F.col("valid_to").isNull() |
        (F.col("valid_to") > F.to_timestamp(F.lit(as_of_time)))
    )
)

as_of_df.select(
    "ticker",
    "event_time",
    "revenue",
    "record_version",
    "knowledge_time",
    "valid_from",
    "valid_to"
).show(truncate=False)

# COMMAND ----------

late_arriving = [
    (
        "C-LATE-001",
        "vendor_c",
        "MSFT",
        "2026-01-05 00:00:00",
        61858.0,
        "USD",
        "ACTIVE",
        "2026-01-12 08:00:00",
        "2026-01-12 08:05:00"
    )
]

late_schema = [
    "record_id",
    "vendor",
    "ticker",
    "event_time",
    "revenue",
    "currency",
    "status",
    "knowledge_time",
    "ingestion_timestamp"
]

late_df = spark.createDataFrame(
    late_arriving,
    late_schema
)

late_df = (
    late_df
    .withColumn("event_time", F.to_timestamp("event_time"))
    .withColumn("knowledge_time", F.to_timestamp("knowledge_time"))
    .withColumn("ingestion_timestamp", F.to_timestamp("ingestion_timestamp"))
)

# COMMAND ----------

late_df = late_df.withColumn(
    "arrival_delay_days",
    F.datediff(
        F.to_date("knowledge_time"),
        F.to_date("event_time")
    )
)

late_df.select(
    "ticker",
    "event_time",
    "knowledge_time",
    "arrival_delay_days"
).show()

# COMMAND ----------

