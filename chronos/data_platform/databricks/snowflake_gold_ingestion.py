# Databricks notebook source
SNOWFLAKE_OPTIONS = {
    "sfURL": "EGQLJCW-QS91215.snowflakecomputing.com",
    "sfDatabase": "CHRONOS",
    "sfSchema": "GOLD",
    "sfWarehouse": "COMPUTE_WH",
    "sfRole": "ACCOUNTADMIN",
    "sfUser": "KISHORSVV",
    "sfPassword": "Venkateswara@10"
}

# COMMAND ----------

SNOWFLAKE_OPTIONS = {
    "sfURL": "EGQLJCW-QS91215.snowflakecomputing.com",
    "sfDatabase": "CHRONOS",
    "sfSchema": "GOLD",
    "sfUser": "KISHORSVV",
    "sfPassword": "Venkateswara@10"
}

# COMMAND ----------

gold_df = (
    spark.read
    .format("delta")
    .load(f"/Volumes/workspace/default/chronos/gold/reconciled_events/")
)

display(gold_df)

# COMMAND ----------

(
    gold_df
    .write
    .format("snowflake")
    .options(**SNOWFLAKE_OPTIONS)
    .option(
        "dbtable",
        "RECONCILED_EVENTS"
    )
    .mode("overwrite")
    .save()
)

# COMMAND ----------

gold_df = (
    spark.read
    .format("delta")
    .load("/Volumes/workspace/default/chronos/gold/reconciled_events/")
)

display(gold_df)

(
    gold_df.write
    .format("jdbc")
    .option("databricks.connection", "snowflake_gold")
    .option("dbtable", "CHRONOS.GOLD.RECONCILED_EVENTS")
    .mode("overwrite")
    .save()
)


# COMMAND ----------

SNOWFLAKE_OPTIONS = {
    "host": "EGQLJCW-QS91215.snowflakecomputing.com",
    "sfDatabase": "CHRONOS",
    "sfSchema": "GOLD",
    "sfWarehouse": "COMPUTE_WH",
    "sfRole": "ACCOUNTADMIN",
    "sfUser": "KISHORSVV",
    "sfPassword": "Venkateswara@10"
}

gold_df = (
    spark.read
    .format("delta")
    .load("/Volumes/workspace/default/chronos/gold/reconciled_events/")
)

display(gold_df)

(
    gold_df.write
    .format("snowflake")
    .options(**SNOWFLAKE_OPTIONS)
    .option("dbtable", "RECONCILED_EVENTS")
    .mode("overwrite")
    .save()
)


# COMMAND ----------

evidence_output = (
    spark.read
    .format("delta")
    .load("/Volumes/workspace/default/chronos/gold/reconciliation_evidence")
)

# COMMAND ----------

display(evidence_output)

# COMMAND ----------

(
    evidence_output.write
    .format("snowflake")
    .options(**SNOWFLAKE_OPTIONS)
    .option("dbtable", "RECONCILIATION_EVIDENCE")
    .mode("overwrite")
    .save()
)

# COMMAND ----------

SNOWFLAKE_OPTIONS = {
    "host": "EGQLJCW-QS91215.snowflakecomputing.com",
    "sfDatabase": "CHRONOS",
    "sfSchema": "GOLD",
    "sfWarehouse": "COMPUTE_WH",
    "sfRole": "ACCOUNTADMIN",
    "sfUser": "KISHORSVV",
    "sfPassword": "Venkateswara@10"
}

evidence_output = (
    spark.read
    .format("delta")
    .load("/Volumes/workspace/default/chronos/gold/reconciliation_evidence/")
)

display(evidence_output)

(
    evidence_output.write
    .format("snowflake")
    .options(**SNOWFLAKE_OPTIONS)
    .option("dbtable", "RECONCILIATION_EVIDENCE")
    .mode("overwrite")
    .save()
)
