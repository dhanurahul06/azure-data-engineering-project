# Databricks notebook source
# COMMAND ----------
# Read raw customer data from ADLS Gen2 landing zone
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("abfss://landing@rahulde2026lake.dfs.core.windows.net/dbo.Customers.txt")

# COMMAND ----------
# Add a derived FullName column by combining first and last name
from pyspark.sql.functions import concat, lit
df_with_fullname = df.withColumn("FullName", concat(df["FirstName"], lit(" "), df["LastName"]))# Databricks notebook source
spark.sql("CREATE SCHEMA IF NOT EXISTS rahul_de_databricks.customer_data")

# COMMAND ----------

spark.sql("SHOW SCHEMAS IN rahul_de_databricks").show()

# COMMAND ----------

df_customer = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("abfss://landing@rahulde2026lake.dfs.core.windows.net/processed/customer1.csv")

df_customer.show()

# COMMAND ----------

df_customer.write.mode("overwrite").saveAsTable("rahul_de_databricks.customer_data.customers_bronze")

# COMMAND ----------

spark.sql("SELECT * FROM rahul_de_databricks.customer_data.customers_bronze").show()

# COMMAND ----------

from pyspark.sql.functions import when, col

df_customer2 = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("abfss://landing@rahulde2026lake.dfs.core.windows.net/processed/customer1.csv")

# Add one extra column — a simple derived flag based on City
df_customer2 = df_customer2.withColumn(
    "IsMetro",
    when(col("City").isin("Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad", "Kolkata"), "Yes")
    .otherwise("No")
)

df_customer2.show()

# COMMAND ----------

df_customer2.write.mode("overwrite").saveAsTable("rahul_de_databricks.customer_data.customers_enriched")

# COMMAND ----------

spark.sql("SELECT * FROM rahul_de_databricks.customer_data.customers_enriched").show()

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE VIEW rahul_de_databricks.customer_data.metro_customers_view AS
SELECT CustomerID, FirstName, LastName, City, IsMetro
FROM rahul_de_databricks.customer_data.customers_enriched
WHERE IsMetro = 'Yes'
""")

# COMMAND ----------

spark.sql("SELECT * FROM rahul_de_databricks.customer_data.metro_customers_view").show()

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE FUNCTION rahul_de_databricks.customer_data.classify_signup(signup_date DATE)
RETURNS STRING
RETURN CASE
    WHEN signup_date >= '2024-06-01' THEN 'Recent'
    ELSE 'Older'
END
""")

# COMMAND ----------

spark.sql("""
SELECT CustomerID, FirstName, SignupDate,
       rahul_de_databricks.customer_data.classify_signup(SignupDate) AS SignupCategory
FROM rahul_de_databricks.customer_data.customers_bronze
""").show()