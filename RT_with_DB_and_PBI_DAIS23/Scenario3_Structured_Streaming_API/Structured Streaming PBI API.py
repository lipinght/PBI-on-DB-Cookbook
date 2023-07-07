# Databricks notebook source
# Delete checkpoint
dbutils.fs.rm("<checkpoint_location>", recurse=True)

# COMMAND ----------

# Static reference data - df_sales_territory

# Define the path to the CSV file
csv_path_sales_territory = '<data_path>/reference/DimSalesTerritory.csv'

# Define the schema for the DataFrame
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType
schema_sales_territory = StructType([
   StructField('SalesTerritoryKey', IntegerType(), True),
    StructField('SalesTerritoryAlternateKey', StringType(), True),
    StructField('SalesTerritoryRegion', StringType(), True),
    StructField('SalesTerritoryCountry', StringType(), True),
    StructField('SalesTerritoryGroup', StringType(), True),
    StructField('SalesTerritoryType', StringType(), True),
    StructField('SalesTerritoryCode', StringType(), True),
    StructField('StartDate', StringType(), True),
    StructField('EndDate', StringType(), True)])
    
# Load the CSV file into a DataFrame
df_sales_territory = spark.read.format('csv') \
             .schema(schema_sales_territory) \
             .option('delimiter', '|') \
             .load(csv_path_sales_territory)

# Display the first 10 rows of the DataFrame
display(df_sales_territory.limit(10))

# COMMAND ----------

# Static reference data - df_promotion

# Define the path to the CSV file
csv_path_promotion = '<data_path>/reference/DimPromotion.csv'

# Define the schema for the DataFrame
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType
schema_promotion = StructType([
    StructField('PromotionKey', IntegerType(), True),
    StructField('PromotionAlternateKey', StringType(), True),
    StructField('EnglishPromotionName', StringType(), True),
    StructField('SpanishPromotionName', StringType(), True),
    StructField('FrenchPromotionName', StringType(), True),
    StructField('DiscountPct', StringType(), True),
    StructField('EnglishPromotionType', StringType(), True),
    StructField('SpanishPromotionType', StringType(), True),
    StructField('FrenchPromotionType', StringType(), True),
    StructField('EnglishPromotionCategory', StringType(), True),
    StructField('SpanishPromotionCategory', StringType(), True),
    StructField('FrenchPromotionCategory', StringType(), True),
    StructField('StartDate', StringType(), True),
    StructField('EndDate', StringType(), True),
    StructField('MinQty', IntegerType(), True),
    StructField('MaxQty', IntegerType(), True)])
    
# Load the CSV file into a DataFrame
df_promotion = spark.read.format('csv') \
             .schema(schema_promotion) \
             .option('delimiter', '|') \
             .load(csv_path_promotion)

# Display the first 10 rows of the DataFrame
display(df_promotion.limit(10))

# COMMAND ----------

# Read raw sales data as a stream using AutoLoader

raw_df = spark.readStream.format("cloudFiles") \
          .option("cloudFiles.format","json") \
          .option("cloudFiles.schemaLocation", "<checkpoint_location>") \
          .load("<data_path>/stream/")

# COMMAND ----------

display(raw_df)

# COMMAND ----------

# Enrich raw sales data with static reference data about Sales Territory and Promotion

from pyspark.sql.functions import lit
from pyspark.sql.functions import current_timestamp

clean_df = (raw_df
            .join(df_sales_territory, raw_df.SalesTerritoryKey == df_sales_territory.SalesTerritoryKey)
            .join(df_promotion, raw_df.PromotionKey == df_promotion.PromotionKey)
            .select(
                "orderdate",
                "SalesTerritoryRegion",
                "EnglishPromotionType",
                "SalesOrderNumber",
                "OrderQuantity",
                "SalesAmount")
            .withColumnRenamed("SalesTerritoryRegion", "Region")
            .withColumnRenamed("EnglishPromotionType", "PromotionType")
            .withColumn("MinQuantity", lit(0))
            .withColumn("MaxQuantity", lit(100))
            .withColumn("TargetQuantity", lit(75))
            .withColumn("DateTime", current_timestamp())
           )


# COMMAND ----------

display(clean_df)

# COMMAND ----------

# Set Power BI Key, this is for demo purpose only, do not hardcode your key in notebooks, please use secret scope instead https://docs.databricks.com/security/secrets/secret-scopes.html

pbi_dataset = "<dataset_id>"
pbi_key = "<powerbi_api_key>"

# COMMAND ----------

def pbi_api(df, epoch_id):
  # python code to call Power BI
  import urllib.request
  import json
  import os
  import ssl
  import pandas as pd

  def allowSelfSignedHttps(allowed):
      # bypass the server certificate verification on client side
      if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
          ssl._create_default_https_context = ssl._create_unverified_context

  allowSelfSignedHttps(True) 

  #convert to pandas df and prepare the data to call Power BI
  pdf=df.toPandas()
  pdf1=pdf.applymap(str)
  payload_json = pdf1.to_json(orient='records', date_format='iso')


  body = str.encode(payload_json)


  url = f'https://api.powerbi.com/beta/<tenent_id>/datasets/{pbi_dataset}/rows?experience=power-bi&key={pbi_key}'

  headers = {'Content-Type':'application/json'}

  req = urllib.request.Request(url, body, headers)

  try:
      response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))

      # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      print(error.info())
      print(json.loads(error.read().decode("utf8", 'ignore')))

# COMMAND ----------

#for each batch call pbi_api function
clean_df.writeStream.foreachBatch(pbi_api).start() 

# COMMAND ----------


