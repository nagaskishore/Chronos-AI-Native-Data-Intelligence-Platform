# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql.window import Window

SILVER_BASE = "/Volumes/workspace/default/chronos/silver"
DQ_BASE = "/Volumes/workspace/default/chronos/dq"

SILVER_PATH = f"{SILVER_BASE}/vendor_events"

print(SILVER_PATH)

# COMMAND ----------

silver_df = (
    spark.read
    .format("delta")
    .load(SILVER_PATH)
)

print("Silver records:", silver_df.count())

display(silver_df)

# COMMAND ----------

dq_required_check = (
    silver_df
    .withColumn(
        "missing_required_field",
        F.when(
            F.col("record_id").isNull()
            | F.col("vendor").isNull()
            | F.col("ticker").isNull()
            | F.col("event_time").isNull()
            | F.col("revenue").isNull()
            | F.col("currency").isNull(),
            F.lit(True)
        ).otherwise(F.lit(False))
    )
)

display(
    dq_required_check
    .filter(F.col("missing_required_field") == True)
)

# COMMAND ----------

dq_revenue_check = (
    dq_required_check
    .withColumn(
        "invalid_revenue",
        F.when(
            F.col("revenue") < 0,
            F.lit(True)
        ).otherwise(F.lit(False))
    )
)

display(
    dq_revenue_check
    .filter(F.col("invalid_revenue") == True)
)

# COMMAND ----------

dq_currency_check = (
    dq_revenue_check
    .withColumn(
        "invalid_currency",
        F.when(
            F.col("currency") != "USD",
            F.lit(True)
        ).otherwise(F.lit(False))
    )
)

display(
    dq_currency_check
    .filter(F.col("invalid_currency") == True)
)

# COMMAND ----------

duplicate_window = (
    Window
    .partitionBy("vendor", "record_id")
    .orderBy(F.col("ingestion_timestamp"))
)

# COMMAND ----------

dedup_check = (
    dq_currency_check
    .withColumn(
        "_duplicate_rank",
        F.row_number().over(duplicate_window)
    )
)

display(
    dedup_check
    .filter(F.col("_duplicate_rank") > 1)
)

# COMMAND ----------

dq_classified = (
    dedup_check
    .withColumn(
        "is_duplicate",
        F.when(
            F.col("_duplicate_rank") > 1,
            F.lit(True)
        ).otherwise(F.lit(False))
    )
)

# COMMAND ----------

display(
    dq_classified
    .select(
        "record_id",
        "vendor",
        "ticker",
        "event_time",
        "revenue",
        "is_duplicate",
        "_duplicate_rank"
    )
    .orderBy("vendor", "record_id", "_duplicate_rank")
)

# COMMAND ----------

dq_final = (
    dq_classified
    .withColumn(
        "dq_status",
        F.when(
            F.col("missing_required_field") == True,
            F.lit("REJECTED")
        )
        .when(
            F.col("invalid_revenue") == True,
            F.lit("REJECTED")
        )
        .when(
            F.col("invalid_currency") == True,
            F.lit("REJECTED")
        )
        .when(
            F.col("is_duplicate") == True,
            F.lit("REJECTED")
        )
        .otherwise(F.lit("VALID"))
    )
)

# COMMAND ----------

dq_final = (
    dq_final
    .withColumn(
        "dq_reason",
        F.when(
            F.col("missing_required_field") == True,
            F.lit("MISSING_REQUIRED_FIELD")
        )
        .when(
            F.col("invalid_revenue") == True,
            F.lit("INVALID_REVENUE")
        )
        .when(
            F.col("invalid_currency") == True,
            F.lit("INVALID_CURRENCY")
        )
        .when(
            F.col("is_duplicate") == True,
            F.lit("DUPLICATE_RECORD")
        )
        .otherwise(F.lit(None))
    )
)

# COMMAND ----------

display(
    dq_final.select(
        "record_id",
        "vendor",
        "ticker",
        "event_time",
        "revenue",
        "dq_status",
        "dq_reason"
    )
)

# COMMAND ----------

(
    dq_final
    .write
    .format("delta")
    .mode("append")
    .save(f"{DQ_BASE}/final")
)

# COMMAND ----------

quarantine_df = (
    dq_final
    .filter(F.col("dq_status") == "REJECTED")
)

display(quarantine_df)

# COMMAND ----------

valid_silver_df = (
    dq_final
    .filter(F.col("dq_status") == "VALID")
)

print("Valid records:", valid_silver_df.count())
print("Rejected records:", quarantine_df.count())

# COMMAND ----------

valid_silver_df

# COMMAND ----------

business_event_summary = (
    valid_silver_df
    .groupBy("ticker", "event_time")
    .agg(
        F.countDistinct("vendor").alias("vendor_count"),
        F.countDistinct("revenue").alias("revenue_value_count")
    )
)

display(
    business_event_summary
    .orderBy("event_time", "ticker")
)

# COMMAND ----------

conflicts = (
    business_event_summary
    .filter(
        (F.col("vendor_count") > 1)
        &
        (F.col("revenue_value_count") > 1)
    )
)

display(conflicts)

# COMMAND ----------

conflict_keys = (
    conflicts
    .select(
        "ticker",
        "event_time"
    )
    .withColumn("has_conflict", F.lit(True))
)

# COMMAND ----------

silver_with_conflicts = (
    dq_final
    .join(
        conflict_keys,
        on=["ticker", "event_time"],
        how="left"
    )
    .withColumn(
        "has_conflict",
        F.coalesce(
            F.col("has_conflict"),
            F.lit(False)
        )
    )
)

# COMMAND ----------

display(
    silver_with_conflicts
    .filter(F.col("has_conflict") == True)
    .select(
        "ticker",
        "event_time",
        "vendor",
        "revenue",
        "currency",
        "record_id"
    )
    .orderBy("event_time", "ticker", "vendor")
)

# COMMAND ----------

source_priority = {
    "vendor_a": 1,
    "vendor_b": 2,
    "vendor_c": 3
}

priority_expr = F.create_map(
    *[
        x
        for pair in source_priority.items()
        for x in (F.lit(pair[0]), F.lit(pair[1]))
    ]
)

# COMMAND ----------

silver_with_priority = (
    silver_with_conflicts
    .withColumn(
        "source_priority",
        priority_expr[F.col("vendor")]
    )
)

display(
    silver_with_priority.select(
        "ticker",
        "event_time",
        "vendor",
        "revenue",
        "source_priority",
        "has_conflict"
    )
)

# COMMAND ----------

conflict_window = (
    Window
    .partitionBy("ticker", "event_time")
    .orderBy(
        F.col("source_priority").asc(),
        F.col("ingestion_timestamp").desc()
    )
)

reconciled = (
    silver_with_priority
    .withColumn(
        "_source_rank",
        F.row_number().over(conflict_window)
    )
)

# COMMAND ----------

display(
    reconciled
    .filter(F.col("has_conflict") == True)
    .select(
        "ticker",
        "event_time",
        "vendor",
        "revenue",
        "source_priority",
        "_source_rank"
    )
    .orderBy("event_time", "ticker", "_source_rank")
)

# COMMAND ----------

(
    quarantine_df
    .write
    .format("delta")
    .mode("overwrite")
    .save(f"{DQ_BASE}/quarantine")
)

# COMMAND ----------

(
    reconciled
    .filter(F.col("has_conflict") == True)
    .write
    .format("delta")
    .mode("overwrite")
    .save(f"{DQ_BASE}/conflicts")
)

# COMMAND ----------

dq_summary = (
    dq_final
    .groupBy("dq_status", "dq_reason")
    .count()
    .orderBy("dq_status")
)

display(dq_summary)

# COMMAND ----------

conflict_metrics = (
    reconciled
    .agg(
        F.count("*").alias("total_records"),
        F.sum(
            F.when(F.col("has_conflict"), 1).otherwise(0)
        ).alias("conflicting_records")
    )
)

display(conflict_metrics)