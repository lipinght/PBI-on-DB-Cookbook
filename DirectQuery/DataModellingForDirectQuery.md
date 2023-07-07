# Data Modelling for DirectQuery mode

## Star schemas versus flat, wide tables

How you model your data is a key factor in determining how successful you will be when using DirectQuery mode in Power BI.

Power BI has a strong preference for dimensional models and having the data it uses modelled as a [star schema](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema).
Even if there may be some occasional advantages to modelling all the data for your report as a single flat, wide table, in almost all cases these advantages are outweighed by the advantages of using a star schema.

## Avoid doing transformations inside Power BI or using views

Power BI has a number of options for transforming data, for example in the Power Query Editor or by creating calculated columns using DAX. 
While this functionality works in DirectQuery mode (with some limitations) there is always a performance penalty to pay from using them.
The same applies to the use of views that contain complex business logic.
It is always preferable to materialise all transformations before the data reaches Power BI.

## Referential integrity

You should ensure that referential integrity exists between the columns used to join the dimension tables and the fact tables in your star schema.
If referential integrity exists then it means you can set the ["Assume Referential Integrity"](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-assume-referential-integrity) property on the relationships in your Power BI dataset, which in turn allows Power BI to generate SQL queries that join these tables using inner joins rather than left outer joins.
Inner joins may result in faster SQL queries.

## Nullable columns

Always set NOT NULL constraints on columns in Databricks where possible.
This is because Power BI may generate more efficient SQL queries when it knows a column is not nullable.

## Composite models

Different tables in a single Power BI dataset can have different storage modes: some tables can be in Import mode and some can be in DirectQuery mode, for example.
Using different storage modes for different tables in the same dataset can help you find the right balance between report performance and data latency.

Apart from DirectQuery mode and Import mode, Power BI has a third storage mode called Dual mode which allows a table to switch between DirectQuery mode and Import mode depending on the circumstances. 
If you have a large fact table using DirectQuery mode it is highly recommended to use Dual mode for your dimension tables: this means that any queries which need to join dimension tables to the fact table can be resolved wholly in DirectQuery mode while queries that only get data from the dimension tables can be resolved in Import mode. 


## Hybrid tables

It is also possible to use Import mode and DirectQuery mode for different data in the same table, a feature known as hybrid tables.
This feature is only available if you are using Power BI Premium.
For example, this allows you to use Import mode to store historical data but DirectQuery mode for more recent data that may change frequently.
You can configure this as part of a table's Incremental Refresh settings using the ["Get the latest data in real time with DirectQuery"](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#optional-settings) option.

## Aggregations

Power BI allows you to define [aggregation tables](https://learn.microsoft.com/en-us/power-bi/transform-model/aggregations-advanced) containing pre-aggregated data derived from a fact table as part of a dataset.
When a report runs, Power BI can detect if pre-aggregated data can be used from one of these tables rather than using data from the fact table, which can result in much better performance.
Aggregation tables can use Import mode or DirectQuery mode, but can only be built on top of tables that use DirectQuery mode.

You can build aggregation tables manually or allow Power BI to build aggregation tables automatically using its [Automatic Aggregations](https://learn.microsoft.com/en-us/power-bi/enterprise/aggregations-auto) feature.


## SQL queries as sources for tables

Power BI allows you to use your own SQL queries as the source for tables in a dataset, rather than just connecting a table in a dataset to a table in Databricks.
However, this is not recommended when using DirectQuery mode: it can result in a performance overhead if the SQL query contains complex logic, and it can also make maintenance of your dataset much harder.
Instead, always try to model your data so that all of your transforms are materialised and you can connect a table in a dataset to a table in Databricks.

## Dynamic M parameters

The [Dynamic M parameter](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-dynamic-m-query-parameters) feature allows you to take a selection made in a slicer or filter in a report and pass it back to an M parameter in the Power Query Editor. 
This gives you more control over how Power BI generates SQL queries: for example you can use this feature to pass values to a Databricks SQL Table UDF used as a fact table.
It is also possible to allow end users to enter values in a report, rather than selecting from a list of pre-defined values, and pass these values to a dynamic M parameter as shown [here](https://blog.crossjoin.co.uk/2023/01/29/passing-any-arbitrary-value-from-a-power-bi-report-to-a-dynamic-m-parameter/).

## DAX calculations

There are often several different ways to write the same DAX calculation for a measure, some of which can be more efficient than others.
If you can see that a DAX calculation is causing slow performance you should experiment with rewriting it: for example, the new DAX [Window functions](https://pbidax.wordpress.com/2022/12/15/introducing-dax-window-functions-part-1/) can result in much better performance in DirectQuery mode as shown [here](https://blog.crossjoin.co.uk/2023/01/02/why-dax-window-functions-are-important-for-performance-in-power-bi-directquery-mode/).