# About
This repository is used for scraping the latest available data provided by Data.gov.sg and Singstat's Table Builder. In particular, for each Data.gov.sg and SingStat website, Selenium would attempt to expand the data categories and pull its metadata information before exporting them into csv file(s) for each data source. 

For Data.gov.sg, 2 csv files representing Data Collections (i.e. *Datagovsg_collections_17032024_202304.csv*) and Datasets (i.e. *Datagovsg_dataset_17032024_202304.csv*) would be generated. 

## Definitions for files generated from scraping Data.gov.sg:
 - **Data Collections**: Group of related datasets defined by Data.gov.sg
 - **Datasets**: Actual data files.

For **Data Collections**, the headers are identified by
- "Collections";
- "Data period";
- "Number of datasets";
- "Datatype";
- "Source";
- "Collections url";
- "Date_of_check";

For **Datasets**, the headers are identified by
- "Data period";
- "Last updated";
- "Datatype";
- "Source";
- "Dataset url";
- "Date_of_check";

For SingStat, the csv file would contain the categories of the data which it belongs to and the url link for download. The headers are identfied by 
- "Dataset";
- "Theme";
- "Categories";
- "SubCategories";
- "URL";
- "Date_of_check"

## Installation of libraries (Python)
You may install using package manager such as Python pip or environment management system such as Conda to install all the libraries listed in *requirements.txt*