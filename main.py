import threading
import csv

from property_structure import Property
from scrapers.immohans import ImmoHansProp


# Immo Hans
test_scraper = ImmoHansProp("https://www.hansimmo.be/woning-te-koop-in-deurne/966")
# test_scraper.scrape()
test_scraper.get_property()
pass