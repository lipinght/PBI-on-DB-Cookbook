# Architecture
![](/RT_with_DB_and_PBI_DAIS23/img/arch_scenario3.jpg)

# Demo Prep

* Download the the files in [Scenario 3 Structured Streaming API folder](../RT_with_DB_and_PBI_DAIS23/Scenario3_Structured_Streaming_API)
* Import notebooks into Databricks workspace
* Populate relevant <data_path> in the notebooks

# Demo Flow

* Create a Power BI Streaming Dataset and get API information from dataset properties
* Attach the structured streaming notebook to a cluster, populate Power BI API Key in secret scope and quote the secret in the notebook and run the notebook
* Create a dashboard in Power BI service using tiles and streaming dataset