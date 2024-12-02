This is the project of scraping the data for different websites.

First I have created three different files from where i can scrap the data in each link, 
after we run these file we will be able to fetch the data and than we should create the tables mannually beacuse I didn't create the method by code.(on TODO)
I have named files in this way NorsemenTvSeries,VikingSeries,VikingNFLteam.
Next thing that I've done is that i have create a class called HandlingDataDB and on this class I have
defined different methods that I use them into my files, method names are :
connect_db which creates the connection between postgres and our code,
close_connection which closes the connection after we push the data,
push_df_to_db after i have transformed the data to a dataframe I pushed these data to their tables.

I have used connection_main.json from which i do the connection with my postgresql database.
I have also include the cronjob.py file which is supposed to launch the pipeline in each file and scrap the data daily.

For the web development I have used framework FLASK where i have create my models also the routes for my project.
Here I have also include the templates for the design of the website , for each table we will have its page.
If we want to launch the project all we have to do is that we need the requirements and 
after that we just run the command python main.py.


######### NOTEE ######
U SHOULD INSTALL THE REQUIREMENTS TO RUN THE PROJECT WITH THIS COMMAND 

pip install -r requirements.txt
===========

Strucutre of the database is listed on the database.png
On the project.png is the design and how the project is looking like when we launch the project


#TODO List
Data Handling
Create a method to automatically generate tables in the database:
Implement a method within HandlingDataDB to create tables dynamically based on the data scraped.

Current Status: Currently, tables need to be manually created in the database.
A method to automate table creation should be added.
Code Organization
Combine Scraping Logic into a Single Class: 
Currently, the scraping logic is spread across three separate files. 
Refactor and consolidate the scraping logic into one class to make 
the project more maintainable and easier to extend in the future.