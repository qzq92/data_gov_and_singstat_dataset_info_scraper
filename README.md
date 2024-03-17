# About
This repository is used for scraping the latest available data provided by Data.gov.sg and Singstat's Table Builder. In particular, for each Data.gov.sg and SingStat website, Selenium would attempt to expand the data categories and pull its metadata information before exporting them into csv file(s) for each data source. 

For Data.gov.sg, 2 csv files representing *Data Collections* and *Datasets* would be generated, where *Data Collections* can be thought as a group of related datasets defined by Data.gov.sg, while the *Datasets* are the actual data 

For SingStat, the csv file would contain the categories of the data which it belongs to and the url link for download.  

## Key Libraries used
- Pandas
- Selenium

