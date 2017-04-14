# Collect Australia Child Care information

This is a web spider to collect Child Care information from the website  
http://ifp.mychild.gov.au/Search/AZSearch.aspx.  
The code is written with Scrapy framework. It goes through the A to Z and fetch
the Child Care information.  
There are about **197k** items.


# Data fields
Most of Child Care centres have `name`, `type`, and `address`. Other fields will be collected if possible.
- name
- type
- address
- *email* (optional)
- *phone*
- *web*


# How to run?
Clone the code and run following command  
```bash
scrapy crawl mychildcare -o filename.csv
```
This will export the result to `filename.csv`, change it to `filename.json` if you prefer json format.  
Please refer to th Scrapy project to get more option.  

>**Suggestion**  
>If you start the program by default, it goes through all letters from A to Z, which takes long time.
>Change the start_url to Z only to avoid that, and quick turn around to fix or verify it.
