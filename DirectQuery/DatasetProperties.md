# Dataset, workspace and capacity properties for DirectQuery

Several properties can be set on datasets, workspaces and Power BI Premium capacities that affect DirectQuery mode.

## Single Sign-On

Single Sign-On (SSO) allows Power BI to pass the identity of the user running a report back to Azure Databricks. 
Instructions for enabling SSO in the Power BI Service can be found [here](https://learn.microsoft.com/en-us/azure/databricks/partners/bi/power-bi#access-azure-databricks-data-source-using-the-power-bi-service)
If you are using an on-premises data gateway, more information on enabling SSO can be found [here](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-sso-overview).

## Controlling the number of connections between Power BI and Databricks

The number of connections that Power BI can open between itself and Databricks can have a significant impact on the performance of a report, especially when multiple users are running reports at the same time.
The number of connections is determined by the "Maximum connections per data source" property that can be set in the Options dialog in Power BI Desktop.
Details of how to find this property are [here](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about#maximum-number-of-connections).
The default value for this property is 10, meaning that Power BI can use up to 10 connections back to Databricks.
However, if you are using Power BI Premium, this can be increased to 30.
Be aware that increasing the number of connections does not always lead to better report performance: if too many concurrent queries are run it may result in worse performance.

## Controlling the amount of parallelism within a DAX query

The data displayed in a single visual in a Power BI report is returned by a single DAX query to the dataset. 
In DirectQuery mode, Power BI gets the data for that DAX query by generating one or more SQL queries to Databricks. By default these SQL queries are run in sequence and this may lead to slow performance. 
If you are using Power BI Premium you can increase the number of SQL queries that can be run in parallel by a single DAX query by changing the [MaxParallelismPerQuery property](https://powerbi.microsoft.com/en-us/blog/query-parallelization-helps-to-boost-power-bi-dataset-performance-in-directquery-mode/) of your dataset, either using a [TMSL script](https://learn.microsoft.com/en-us/analysis-services/tmsl/tabular-model-scripting-language-tmsl-reference?view=asallproducts-allversions) or with a tool like [Tabular Editor](https://tabulareditor.github.io/).

## The one-million row query limit

Power BI has a limit on the number of rows that a SQL query can return of one million rows.
This limit is most commonly encountered when complex DAX calculations require a lot of detailed data.
Although this limit can be increased by setting the [Max Intermediate Row Set Count](https://powerbi.microsoft.com/en-gb/blog/five-new-power-bi-premium-capacity-settings-is-available-on-the-portal-preloaded-with-default-values-admin-can-review-and-override-the-defaults-with-their-preference-to-better-fence-their-capacity/) property on a capacity or a workspace, this does not solve the problem that any SQL query that returns more than one million rows is likely to be very slow and expensive to run.
As a result a better option is to try to tune your DAX calculations to avoid the need for this type of SQL query.
You may also be able to avoid this limit in some cases by using Import mode aggregation tables, as shown [here](https://blog.crossjoin.co.uk/2023/02/08/avoiding-the-maximum-allowed-size-error-in-power-bi-directquery-mode-with-aggregations-on-degenerate-dimensions/).

