-- Databricks notebook source
SET landing_area_path = "<data_path>/source/stream"

-- COMMAND ----------

-- Create a streaming live table named internetsales
CREATE STREAMING LIVE TABLE internetsales(
  -- Define a constraint named correct_schema that expects _rescued_data to be NULL. This constrain will be triggered if the input schema evolves. 
  CONSTRAINT correct_schema EXPECT (_rescued_data IS NULL)
  )

COMMENT "Internet Sales bronze table, streamed from the landing area."
-- Populate the table with data selected from cloud_files function, which automatically uses Databticks AutoLoader(https://learn.microsoft.com/en-gb/azure/databricks/ingestion/auto-loader/) 
AS SELECT * 
FROM cloud_files(landing_area_path, "json", map("cloudFiles.inferColumnTypes" , "true"))

-- COMMAND ----------

-- Create a streaming live table named fact_internetsales
CREATE STREAMING LIVE TABLE fact_internetsales (
  -- Define a constraint named positive_quantity that expects OrderQuantity to be greater than 0. If violated, drop the row.
  CONSTRAINT positive_quantity EXPECT (OrderQuantity > 0) ON VIOLATION DROP ROW,
  -- Define a constraint named existing_product that expects ProductKey to be greater than 0. If violated, drop the row.
  CONSTRAINT existing_product EXPECT (ProductKey > 0) ON VIOLATION DROP ROW,
  -- Define a constraint named valid_territory that expects SalesTerritoryKey to be greater than 0. If violated, drop the row.
  CONSTRAINT valid_territory EXPECT (SalesTerritoryKey > 0) ON VIOLATION DROP ROW
)
COMMENT "Internet Sales curated table."
-- Populate the table with selected columns from the streaming live table named internetsales previously defined
AS SELECT orderdate
      , ProductKey
      , SalesTerritoryKey
      , SalesOrderNumber
      , OrderQuantity
      , SalesAmount  
FROM STREAM(LIVE.internetsales)
