# Databricks notebook source
silver_df = spark.table("rahul_de_databricks.customer_data.customers_enriched")
silver_df.show()

# COMMAND ----------

from pyspark.sql.functions import count, col

gold_df = silver_df.groupBy("City", "IsMetro").agg(
    count("CustomerID").alias("NumCustomers")
)

gold_df.orderBy(col("NumCustomers").desc()).show()

# COMMAND ----------

gold_df.write.mode("overwrite").saveAsTable("rahul_de_databricks.customer_data.customers_gold_summary")

# COMMAND ----------

spark.sql("SELECT * FROM rahul_de_databricks.customer_data.customers_gold_summary").show()