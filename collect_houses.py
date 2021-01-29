import csv
import os.path
from threading import Thread, Lock

from scrapers.immo_scraping import ImmoPropScraper
from scrapers.immohans import ImmoHansProp
from scrapers.immoweb import ImmoWebProp

# Setup
print_lock = Lock()
output_path = os.path.abspath("./data")


class ThreadedScraping(Thread):
    def __init__(self, scraper: ImmoPropScraper):
        super().__init__()
        self.scraper = scraper

    def run(self):
        self.scraper.scrape()


# IMMO HANS
# load links from file
with open(os.path.join(output_path, "hans_links.txt"), "r") as file:
    hans_links = file.read().split()

# create Scrapers
hans_scrapers = [ImmoHansProp(url) for url in hans_links]

# Create threads
hans_threads = [ThreadedScraping(scraper) for scraper in hans_scrapers]

# start threads
for thr in hans_threads:
    thr.start()


# IMMOWEB
# load links from file
with open(os.path.join(output_path, "immoweb_links.txt"), "r") as file:
    immoweb_links = file.read().split()

# create Scrapers
immoweb_scrapers = [ImmoWebProp(url) for url in immoweb_links]

# Create threads
immoweb_threads = [ThreadedScraping(scraper) for scraper in immoweb_scrapers]

# start threads
for thr in immoweb_threads:
    thr.start()


# make sure all threads are done before continueing
for thr in hans_threads + immoweb_threads:
    thr.join()


# Write collected data to CSV file
with open(os.path.join(output_path, "immo_properties.csv"), "w") as outfile:
    data_file = csv.DictWriter(
        outfile,
        fieldnames=[
            "locality",
            "property_type",
            "property_subtype",
            "price",
            "sale_type",
            "number_rooms",
            "area",
            "fully_equipped_kitchen",
            "is_furnished",
            "has_open_fire",
            "has_terrace",
            "terrace_area",
            "has_garden",
            "garden_area",
            "land_surface",
            "land_plot_area",
            "number_facades",
            "has_swimming_pool",
            "building_state",
            "source_url",
        ],
    )
    data_file.writeheader()

    # write hans and immoweb properties to file
    for thread in hans_threads + immoweb_threads:
        # get from thread
        property = thread.scraper.get_property()
        # write as csv
        data_file.writerow(property.__dict__)
