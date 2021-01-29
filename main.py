import threading
import csv

from property_structure import Property
from scrapers.immohans import ImmoHansProp


# Immo Hans
test_scraper = ImmoHansProp(
    "https://www.hansimmo.be/appartement-te-koop-in-kapellen/9572"
)
# test_scraper.scrape()
prop = test_scraper.get_property()
pass
