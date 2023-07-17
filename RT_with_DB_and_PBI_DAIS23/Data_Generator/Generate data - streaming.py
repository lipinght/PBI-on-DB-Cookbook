# Databricks notebook source
# Specify the location to generate the synthetic data
file_path = "<data_path>"

# COMMAND ----------

# Reset the data generation
stream_path = f"{file_path}/stream"

# Delete folder and its contents
dbutils.fs.rm(stream_path, recurse=True)

# Recreate the folder
dbutils.fs.mkdirs(stream_path)


# COMMAND ----------

import json
import time
import random
from datetime import datetime, timedelta

# Function to generate random data
def generate_random_data(date):
    sales_data = []
    for _ in range(random.randint(1, 10)):
        order_quantity = random.randint(1, 100)
        unit_price = round(random.uniform(1, 1000), 2)
        sales_amount = order_quantity * unit_price
        sales_data.append({
            "ProductKey": random.randint(1, 600),
            "OrderDate": date.strftime("%Y-%m-%d %H:%M:%S"),
            "PromotionKey": random.randint(1, 50),
            "SalesTerritoryKey": random.randint(1, 10),
            "SalesOrderNumber": f"SO{random.randint(10000, 99999)}",
            "SalesAmount": round(sales_amount, 2),
            "OrderQuantity": order_quantity,
        })
    return sales_data

# Function to generate and save a JSON file for a given date
def generate_and_save_json_file(date, path):
    data = generate_random_data(date)
    json_data = json.dumps(data)
    file_name = date.strftime("%Y-%m-%d_%H%M%S_FactInternetSales.json")
    dbutils.fs.put(f"{path}/{file_name}", json_data, overwrite=True)
    print(f"Wrote {path}/{date}_FactInternetSales.json")

# Generate and save JSON files for each hour. Specify the start and end intervals. 
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 7, 31)

current_date = start_date
while current_date <= end_date:
    for hour in range(24):
        current_hour_date = current_date + timedelta(hours=hour)
        generate_and_save_json_file(current_hour_date, stream_path)
        time.sleep(3)  # Pause for 3 seconds
    current_date += timedelta(days=1)

