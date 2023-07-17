# Architecture
![](/RT_with_DB_and_PBI_DAIS23/img/arch_scenario1.jpg)


# Demo Prep

* Download the the files in [Data Generator folder](../Data_Generator) and [Scenario 1 DLT DQ folder](../Scenario1_DLT_DQ)
* Import notebooks into Databricks workspace
* Populate relevant <data_path> in the notebooks

# Demo Flow

* Attach the data generator notebook to a cluster and run the notebook
* Create a Delta Live Table pipeline using the "DLT- xxx" notebooks and start running the pipeline in a continuous mode
* Create/start a SQL warehouse
* Populate the connection string in pbit, turn on page refresh and publish the power bi report
* Check the admin portal in Power BI for capacity setting --> Power BI Workloads, make sure the auto page refresh is turned on and the interval is set at appropriate level
* Check the published Power BI report to see real-time data visualization in Power BI
