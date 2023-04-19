# Report design considerations for DirectQuery mode

The best way to achieve fast report performance in DirectQuery mode is to reduce the number of SQL queries that are generated when a report runs. 
This can be achieved in a number of different ways:
* Reducing the number of visuals on a report page and instead spreading the visuals over a number of different pages.
* Reducing the number of visuals needed to display the same amount of data: for example, using [small multiples](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-small-multiples) you can replace a several visuals with a single visual.
* Using an Apply All Slicers and Clear All Slicers button to allow end-users to refresh a report page only once they have made all the slicer selections they need, as shown [here](https://powerbi.microsoft.com/en-us/blog/deep-dive-into-the-new-apply-all-slicers-and-clear-all-slicers-buttons/).
* Change the [query reduction settings](https://learn.microsoft.com/en-gb/power-bi/create-reports/desktop-optimize-ribbon-scenarios#apply-query-reduction-settings) for your report.

As a report developer the functionality in the [Optimize ribbon](https://learn.microsoft.com/en-gb/power-bi/create-reports/desktop-optimize-ribbon-scenarios) of Power BI Desktop can make life much easier.
