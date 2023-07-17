# Databricks notebook source
# Specify the location to download the reference data from the Adventure Works sample data
reference_path = "<data_path>"

# COMMAND ----------

import requests
import os

# Define a function to download CSV file from https path to local path
def download_csv(https_path: str, local_path: str) -> bool:
    try:
        response = requests.get(https_path)
        with open(local_path, 'w') as file:
            file.write(response.content.decode('utf-16'))
        return True
    except:
        raise
# Define an array of https paths to download CSV files from
csvs = ['DimProduct.csv', 'DimProductCategory.csv','DimProductSubcategory.csv','DimSalesTerritory.csv','FactProductInventory.csv']
# Download CSV files from each https path
for csv in csvs:
    https_path = f'https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/databases/adventure-works/data-warehouse-install-script/{(csv)}'      
    local_path = f'{reference_path}/{os.path.basename(https_path)}'
    result = download_csv(https_path, local_path)
    print(f"Downloaded {https_path} to {local_path}: {result}")

