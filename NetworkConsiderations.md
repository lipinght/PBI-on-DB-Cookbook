# Network and bandwidth considerations

It is important to consider the location of your Power BI Premium capacity (if you are using one) or your Power BI home tenant relative to the location of Databricks. 
You can find out where your Power BI home tenant is located using the instructions [here](https://learn.microsoft.com/en-us/power-bi/admin/service-admin-where-is-my-tenant-located).
Power BI Premium multi-geo capacities, which allow you to control which Azure Region a capacity is located in, are described [here](https://learn.microsoft.com/en-us/power-bi/admin/service-admin-premium-multi-geo).
In order to reduce the impact of network latency and bandwidth you should locate Power BI and Databricks as close to each other as possible.