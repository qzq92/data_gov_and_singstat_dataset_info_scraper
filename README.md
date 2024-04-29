# About
This repository contains notebook codes for scraping the latest available public data metadata as follows using Selenium library:
|Data source|Description|Sample image|
|---|---|---|
|[Data.gov.sg](https://beta.data.gov.sg/datasets)|Data shared by Singapore Government.|![Data.gov.sg](img/Datagov.png)|
|[Singstats Table Builder](https://tablebuilder.singstat.gov.sg/)| Singapore economic and socio-demographic statistics.|![Singstats](img/Singstat.png)|
|[SmartLocal](https://thesmartlocal.com/event-calendar/?a=alltime)| Website for Singapore lifestyle/leisure events.|![Smartlocal](img/smartlocal.png)|
|[timeanddate](https://www.timeanddate.com/holidays/?allcountries)| Website for various countries/region holidays covering the period from 2000-2040.|![timeanddate](img/timeanddate.png)|
|[SACEOS](https://saceos.org.sg/)| Singapore Association of Convention & Exhibition Organisers & Suppliers trade association for Meetings, Incentives, Conventions, Exhibitions & Events industry website.|![SACEOS](img/SACEOS.png)|

## Installation of libraries (Python)
You may install using package manager such as Python pip or environment management system such as Conda to install all the libraries listed in *requirements.txt*

## Execution and output files
To conduct scraping of metadata from the above sources please execute the cells in the notebook with the *.ipynb* extension. The metadata would be saved as a csv file and stored in the same directory as the corresponding notebooks used for metadata scraping and are named in the following format: *data source_ddmmyyyy_hhmmss.csv* (e.g SACEOS_dataset_16042024_000325.csv). Do note that Data.gov.sg and Singstats data are residing in a common folder, instead of separate folder.