# challenge-collecting-data-group5
## Web scraping project

### What?
This is a web scraping project for the real estate company *"ImmoEliza"*. 
It's objective is to collect **real estate data accross all Belgium**.

The project is structured as follows:
```
challenge-collecting-data-group5/
|-- main.py :to run all the scripts in the *scrapers* directory
|-- property_structure.py :explicit the data structure of any property
|-- scrapers/ :directory contains all the scripts to scrap the websites
|-- test/
|   |-- init.py
|   |   |-- test_main.py :to run all the unit tests
|-- README.md
```

### Why?
*ImmoEliza* wants to create a machine learning model to make **price predictions** on real estate sales in Belgium.

### When?
It is a 3 days project.
The deadline to complete it is scheduled to `29/01/2021 at 4 p.m.`

### How?
- [x] Create the project structure
- [ ] Scrape real estate websites
- [ ] Build the Belgian real estate database
- [ ] Export the data into csv-file

#### Object Oriented Scraping 

We opted for a OOP approach to the challenge.

Every property for sale is saved in a dataclass. In this way, the fields can be
typed, and general export methods can be written. The scraping itself is also
OO. As every website is different, every scraper has to be custom made. But
they do share some basic functionality. So we made a scraper base class from
which all scrapers inherit.

### Who?
This project is carried out by **Group 5** from Theano 2.27 promotion at BeCode.
Group 5 is comprised of:
- Bram De Vroey
- Van Frausum Derrick
- Vincent Rolin

### Pending things to do
