# System Table 

Steps to set up power bi template on top of System Tables
* Populate parameters below when you open the PBIT and save it as PBIX
    * server hostname  (use your sql warehouse connection strings)
    * httppath (use your sql warehouse connection strings)
    * SQL query 
        * ```SELECT *, EXPLODE(custom_tags) AS (TagName, TagValue) FROM system.billing.usage```
        * Replace system.billing.usage from above with the catalog.schema.table if you are querying a normal delta table
    * default catalog (system)
        * Replace system from above using catalog name of your table if you are query a normal delta table
* Replace the SKU pricing table with your own hard coded table or the list_prices table from system.billing
* Replace the workspace table with your own workspace name look up table
* For authentication, make sure you have access to the billing schema of system catalog
* Make sure you set up cluster policy so that the new clusters are created with the tags you want to analyse, and you can go through existing clusters and tag them. 
