# CUBED-DE-INTERN-CHALLENGE : Data Scraping Program

Goal: 
This program crawls through the amazon website and scraps below attributes for all the proucts found: 
Name, Category, SalePrice, OriginalPrice, Availability, URL 

How to use: 
The python scripts are included in the project which include the functionality to crawl the links and scrap data from all the links. Main.py has a variable homeopage which is the URL for the scraping to start from. Since Captha was an issue faced while scraping from amazon, we need to keep updating the homepage to point to a new product's link. 

The program is designed to save the data into an mssql database. It also includes code to save the data into csv file. either one can be used

Since it was a bit slower to write scrapped data directly into the database, data was saved into a csv file and the csv file was imported into mssql database. The database backup has been uploaded as zipped file Amazon.zip. The DTS package used to import the data has also been uploaded 

