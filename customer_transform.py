# Databricks notebook source
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("abfss://landing@rahulde2026lake.dfs.core.windows.net/dbo.Customers.txt")

df.show()
from pyspark.sql.functions import concat, lit

df_with_fullname = df.withColumn("FullName", concat(df["FirstName"], lit(" "), df["LastName"]))
df_with_fullname.show()

# COMMAND ----------

from pyspark.sql.functions import concat, lit

df_with_fullname = df.withColumn("FullName", concat(df["FirstName"], lit(" "), df["LastName"]))
df_with_fullname.show()

# COMMAND ----------

df_with_fullname.write.format("parquet") \
    .mode("overwrite") \
    .save("abfss://landing@rahulde2026lake.dfs.core.windows.net/customer.parquet")

# COMMAND ----------

files = dbutils.fs.ls("abfss://landing@rahulde2026lake.dfs.core.windows.net/customer.parquet/")
for f in files:
    print(f.path)
    

# COMMAND ----------

df_parquet = spark.read.format("parquet") \
    .load("abfss://landing@rahulde2026lake.dfs.core.windows.net/customer.parquet")

df_parquet.show()
df_parquet.write.format("csv") \
    .option("header", "true") \
    .mode("overwrite") \
    .save("abfss://landing@rahulde2026lake.dfs.core.windows.net/processed/customer1.csv")
    files = dbutils.fs.ls("abfss://landing@rahulde2026lake.dfs.core.windows.net/processed/customer1.csv/")
for f in files:
    print(f.path)