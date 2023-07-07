# Databricks notebook source
import dlt

# COMMAND ----------

reference_data_path = '<data_path>/source/reference'

# COMMAND ----------

# Define the path to the CSV file
csv_path_product = f"{reference_data_path}/DimProduct.csv"

# Define the schema for the DataFrame
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType
schema_product = StructType([
    StructField('ProductKey', IntegerType(), True),
    StructField('ProductAlternateKey', StringType(), True),
    StructField('ProductSubcategoryKey', IntegerType(), True),
    StructField('WeightUnitMeasureCode', StringType(), True),
    StructField('SizeUnitMeasureCode', StringType(), True),
    StructField('EnglishProductName', StringType(), True),
    StructField('SpanishProductName', StringType(), True),
    StructField('FrenchProductName', StringType(), True),
    StructField('StandardCost', FloatType(), True),
    StructField('FinishedGoodsFlag', IntegerType(), True),
    StructField('Color', StringType(), True),
    StructField('SafetyStockLevel', IntegerType(), True),
    StructField('ReorderPoint', IntegerType(), True),
    StructField('ListPrice', FloatType(), True),
    StructField('Size', StringType(), True),
    StructField('SizeRange', StringType(), True),
    StructField('Weight', FloatType(), True),
    StructField('DaysToManufacture', IntegerType(), True),
    StructField('ProductLine', StringType(), True),
    StructField('DealerPrice', FloatType(), True),
    StructField('Class', StringType(), True),
    StructField('Style', StringType(), True),
    StructField('ModelName', StringType(), True),
    StructField('LargePhoto', StringType(), True),
    StructField('EnglishDescription', StringType(), True),
    StructField('FrenchDescription', StringType(), True),
    StructField('ChineseDescription', StringType(), True),
    StructField('ArabicDescription', StringType(), True),
    StructField('HebrewDescription', StringType(), True),
    StructField('ThaiDescription', StringType(), True),
    StructField('GermanDescription', StringType(), True),
    StructField('JapaneseDescription', StringType(), True),
    StructField('TurkishDescription', StringType(), True),
    StructField('StartDate', StringType(), True),
    StructField('EndDate', StringType(), True)])

# Load the CSV file into a DataFrame
df_product = spark.read.format('csv') \
             .schema(schema_product) \
             .option('delimiter', '|') \
             .load(csv_path_product)

# Define a DLT table
@dlt.table
def product():
  return df_product

# COMMAND ----------

# Define the path to the CSV file
csv_path_product_category = f"{reference_data_path}/DimProductCategory.csv"

# Define the schema for the DataFrame
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType
schema_product_category = StructType([
    StructField('ProductCategoryKey', IntegerType(), True),
    StructField('ProductCategoryAlternateKey', StringType(), True),
    StructField('EnglishProductCategoryName', StringType(), True),
    StructField('SpanishProductCategoryName', StringType(), True),
    StructField('FrenchProductCategoryName', StringType(), True),
    StructField('StartDate', StringType(), True),
    StructField('EndDate', StringType(), True)])

# Load the CSV file into a DataFrame
df_product_category = spark.read.format('csv') \
             .schema(schema_product_category) \
             .option('delimiter', '|') \
             .load(csv_path_product_category)

# Define a DLT table
@dlt.table
def productcategory():
  return df_product_category

# COMMAND ----------

# Define the path to the CSV file
csv_path_product_subcategory = f"{reference_data_path}/DimProductSubcategory.csv"

# Define the schema for the DataFrame
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType
schema_product_subcategory = StructType([
    StructField('ProductSubcategoryKey', IntegerType(), True),
    StructField('ProductSubcategoryAlternateKey', StringType(), True),
    StructField('EnglishProductSubcategoryName', StringType(), True),
    StructField('SpanishProductSubcategoryName', StringType(), True),
    StructField('FrenchProductSubcategoryName', StringType(), True),
    StructField('ProductCategoryKey', IntegerType(), True),
    StructField('StartDate', StringType(), True),
    StructField('EndDate', StringType(), True)])

# Load the CSV file into a DataFrame
df_product_subcategory = spark.read.format('csv') \
             .schema(schema_product_subcategory) \
             .option('delimiter', '|') \
             .load(csv_path_product_subcategory)

# Define a DLT table
@dlt.table
def productsubcategory():
  return df_product_subcategory

# COMMAND ----------

@dlt.table
def dim_product():

  bronze_product = dlt.read("product")
  bronze_ProductCategory = dlt.read("productcategory")
  bronze_ProductSubcategory = dlt.read("productsubcategory")

  joined_table = bronze_product.join(bronze_ProductSubcategory, "ProductSubcategoryKey").join(bronze_ProductCategory, "ProductCategoryKey")

  result_table = joined_table.selectExpr(
      "ProductKey",
      "EnglishProductName as Name",
      "Class",
      "Style",
      "Color",
      "EnglishProductCategoryName as Category"
  )
  return result_table

# COMMAND ----------

# Define the path to the CSV file
csv_path_sales_territory = f"{reference_data_path}/DimSalesTerritory.csv"

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

# Define a DLT table
@dlt.table
def salesterritory():
  return df_sales_territory

# COMMAND ----------

# Define a DLT table
@dlt.table
def dim_salesterritory():
  return \
    dlt.read("salesterritory") \
      .withColumnRenamed("SalesTerritoryRegion", "Region") \
      .withColumnRenamed("SalesTerritoryCountry", "Country") \
      .withColumnRenamed("SalesTerritoryType", "Type") \
      .select("SalesTerritoryKey", "Region", "Country", "Type")

# COMMAND ----------

# Define the path to the CSV file
csv_path_product_inventory = f"{reference_data_path}/FactProductInventory.csv"

# Define the schema for the DataFrame
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, DoubleType
schema_product_inventory = StructType([
   StructField('ProductKey', IntegerType(), True),
    StructField('DateKey', IntegerType(), True),
    StructField('MovementDate', StringType(), True),
    StructField('UnitCost', DoubleType(), True),
    StructField('UnitsIn', IntegerType(), True),
    StructField('UnitsOut', IntegerType(), True),
    StructField('UnitsBalance', IntegerType(), True),
    StructField('InventoryValue', DoubleType(), True)])
    
# Load the CSV file into a DataFrame
df_product_inventory = spark.read.format('csv') \
             .schema(schema_product_inventory) \
             .option('delimiter', '|') \
             .load(csv_path_product_inventory)

# Define a DLT table
@dlt.table
def productinventory():
  return df_product_inventory

# COMMAND ----------

# Define a DLT table
@dlt.table
def fact_productinventory():
  return \
    dlt.read("productinventory") \
      .select("ProductKey", "DateKey", "UnitsIn", "UnitsOut","UnitCost","UnitsBalance","InventoryValue")
