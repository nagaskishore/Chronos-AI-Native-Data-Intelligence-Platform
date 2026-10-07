# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql.window import Window

TEMPORAL_PATH = "/Volumes/workspace/default/chronos/temporal/vendor_events_history"

GOLD_BASE = "/Volumes/workspace/default/chronos/gold"

GOLD_RECONCILIATION_PATH = (
    f"{GOLD_BASE}/reconciled_events"
)

GOLD_EVIDENCE_PATH = (
    f"{GOLD_BASE}/reconciliation_evidence"
)

print(TEMPORAL_PATH)
print(GOLD_RECONCILIATION_PATH)

# COMMAND ----------

temporal_df = (
    spark.read
    .format("delta")
    .load(TEMPORAL_PATH)
)

print("Temporal records:", temporal_df.count())

temporal_df.show(20, truncate=False)

# COMMAND ----------

current_df = temporal_df.filter(
    F.col("is_current") == True
)

print("Current observations:", current_df.count())

# COMMAND ----------

current_df.select(
    "vendor",
    "ticker",
    "event_time",
    "revenue",
    "record_version",
    "knowledge_time"
).orderBy(
    "ticker",
    "event_time",
    "vendor"
).show(50, truncate=False)

# COMMAND ----------

current_df = current_df.withColumn(
    "business_event_key",
    F.concat_ws(
        "||",
        F.col("ticker"),
        F.date_format(
            "event_time",
            "yyyy-MM-dd HH:mm:ss"
        )
    )
)

# COMMAND ----------

source_priority_expr = (
    F.when(F.col("vendor") == "vendor_a", 1)
     .when(F.col("vendor") == "vendor_b", 2)
     .when(F.col("vendor") == "vendor_c", 3)
     .otherwise(999)
)

current_df = current_df.withColumn(
    "source_priority",
    source_priority_expr
)

# COMMAND ----------

current_df.select(
    "vendor",
    "source_priority"
).distinct().orderBy(
    "source_priority"
).show()

# COMMAND ----------

event_stats = (
    current_df
    .groupBy(
        "ticker",
        "event_time"
    )
    .agg(
        F.countDistinct("vendor").alias(
            "vendor_count"
        ),
        F.countDistinct("revenue").alias(
            "revenue_value_count"
        ),
        F.min("revenue").alias(
            "min_revenue"
        ),
        F.max("revenue").alias(
            "max_revenue"
        )
    )
)

# COMMAND ----------

event_stats = event_stats.withColumn(
    "has_conflict",
    (
        (F.col("vendor_count") > 1) &
        (F.col("revenue_value_count") > 1)
    )
)

# COMMAND ----------

event_stats.orderBy(
    "ticker",
    "event_time"
).show(50, truncate=False)

# COMMAND ----------

current_with_stats = current_df.join(
    event_stats,
    on=["ticker", "event_time"],
    how="left"
)

# COMMAND ----------

winner_window = (
    Window
    .partitionBy(
        "ticker",
        "event_time"
    )
    .orderBy(
        F.col("source_priority").asc(),
        F.col("knowledge_time").desc()
    )
)

# COMMAND ----------

ranked_df = current_with_stats.withColumn(
    "source_rank",
    F.row_number().over(winner_window)
)

# COMMAND ----------

winner_df = ranked_df.filter(
    F.col("source_rank") == 1
)

# COMMAND ----------

winner_df.select(
    "ticker",
    "event_time",
    "vendor",
    "revenue",
    "source_priority",
    "vendor_count",
    "revenue_value_count",
    "has_conflict"
).orderBy(
    "ticker",
    "event_time"
).show(50, truncate=False)

# COMMAND ----------

winner_df = winner_df.withColumn(
    "reconciliation_status",
    F.when(
        F.col("vendor_count") == 1,
        "SINGLE_SOURCE"
    )
    .when(
        F.col("has_conflict") == True,
        "CONFLICT_RESOLVED"
    )
    .otherwise(
        "MULTI_SOURCE_AGREEMENT"
    )
)

# COMMAND ----------

winner_df = winner_df.withColumn(
    "confidence",
    F.when(
        F.col("reconciliation_status") == "SINGLE_SOURCE",
        F.lit("MEDIUM")
    )
    .when(
        F.col("reconciliation_status") == "MULTI_SOURCE_AGREEMENT",
        F.lit("HIGH")
    )
    .when(
        (
            F.col("reconciliation_status") ==
            "CONFLICT_RESOLVED"
        ) &
        (F.col("source_priority") == 1),
        F.lit("HIGH")
    )
    .otherwise(
        F.lit("LOW")
    )
)

# COMMAND ----------

gold_df = winner_df.select(
    "business_event_key",

    "ticker",
    "event_time",

    F.col("revenue").alias(
        "canonical_revenue"
    ),

    "currency",
    "status",

    F.col("vendor").alias(
        "canonical_source"
    ),

    "source_priority",

    "vendor_count",
    "revenue_value_count",

    "has_conflict",
    "reconciliation_status",
    "confidence",

    "record_version",
    "knowledge_time",

    "source_file",
    "batch_id"
)

# COMMAND ----------

gold_df.orderBy(
    "ticker",
    "event_time"
).show(50, truncate=False)

# COMMAND ----------

(
    gold_df
    .write
    .format("delta")
    .mode("overwrite")
    .option(
        "overwriteSchema",
        "true"
    )
    .save(GOLD_RECONCILIATION_PATH)
)

print(
    f"Gold reconciliation written to: "
    f"{GOLD_RECONCILIATION_PATH}"
)

# COMMAND ----------

evidence_df = ranked_df.withColumn(
    "reconciliation_role",
    F.when(
        F.col("source_rank") == 1,
        "WINNER"
    ).otherwise(
        "SUPPORTING_OBSERVATION"
    )
)

# COMMAND ----------

evidence_df = evidence_df.withColumn(
    "reconciliation_reason",
    F.when(
        F.col("source_rank") == 1,
        F.concat(
            F.lit("Selected by source priority. "),
            F.lit("Source priority = "),
            F.col("source_priority").cast("string")
        )
    ).otherwise(
        F.lit(
            "Retained as supporting evidence; "
            "not selected as canonical value."
        )
    )
)

# COMMAND ----------

evidence_output = evidence_df.select(
    "business_event_key",
    "ticker",
    "event_time",

    "vendor",
    "revenue",
    "currency",

    "source_priority",
    "source_rank",

    "vendor_count",
    "revenue_value_count",
    "has_conflict",

    "reconciliation_role",
    "reconciliation_reason",

    "knowledge_time",
    "record_version",

    "source_file",
    "batch_id"
)

# COMMAND ----------

(
    evidence_output
    .write
    .format("delta")
    .mode("overwrite")
    .option(
        "overwriteSchema",
        "true"
    )
    .save(GOLD_EVIDENCE_PATH)
)

# COMMAND ----------

gold = (
    spark.read
    .format("delta")
    .load(GOLD_RECONCILIATION_PATH)
)

gold.select(
    "ticker",
    "event_time",
    "canonical_revenue",
    "canonical_source",
    "reconciliation_status",
    "confidence"
).orderBy(
    "ticker",
    "event_time"
).show(50, truncate=False)

# COMMAND ----------

evidence = (
    spark.read
    .format("delta")
    .load(GOLD_EVIDENCE_PATH)
)

evidence.filter(
    F.col("has_conflict") == True
).select(
    "ticker",
    "event_time",
    "vendor",
    "revenue",
    "source_priority",
    "source_rank",
    "reconciliation_role",
    "reconciliation_reason"
).orderBy(
    "ticker",
    "event_time",
    "source_rank"
).show(50, truncate=False)

# COMMAND ----------

reconciliation_summary = (
    gold
    .groupBy(
        "reconciliation_status",
        "confidence"
    )
    .agg(
        F.count("*").alias("event_count")
    )
    .orderBy(
        "reconciliation_status"
    )
)

reconciliation_summary.show()

# COMMAND ----------



# COMMAND ----------

