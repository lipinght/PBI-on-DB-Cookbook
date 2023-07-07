# What is DirectQuery mode in Power BI and when should I use it?

Power BI has two ways of working with data: Import mode and DirectQuery mode.
In Import mode all of the data that your report might ever need is copied into Power BI's own native, in-memory database engine and when your report runs that is where Power BI gets its data from. 
In DirectQuery mode no data is copied into Power BI and instead, when a report runs, Power BI queries your data source to get just the data that is needed.
Power BI can work with Databricks as a source in both Import mode and DirectQuery mode.

This document outlines best practices for working with Databricks as a data source in DirectQuery mode and the first question to consider is whether DirectQuery mode is the right choice for your project.

Generally speaking, Import mode should be your default choice unless you have a good reason why you cannot use it.
This is because Import mode almost always provides better performance than DirectQuery mode.
The most common reasons to use DirectQuery mode instead are:

* Your data volumes are too large for Power BI to manage. 
Power BI can work with different data volumes in Import mode depending on whether you are using Power BI Premium or not, and the size of the Premium capacity you are using, but it is perfectly feasible to work with fact tables of 1-2 billion rows in Import mode.
* You need to see near real-time data in your reports and you cannot wait for the amount of time needed for an Import mode refresh.
Remember that Power BI features such as incremental refresh and hybrid tables mean that you do not need to import all the data in a table every time existing data changes or new data is added.
* Your data cannot be stored in Power BI for compliance or security reasons.