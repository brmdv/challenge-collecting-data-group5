from threading import Thread, Lock
import csv

from property_structure import Property
from scrapers.immohans import ImmoHansProp


print_lock = Lock()


class PropertyThread(Thread):
    def __init__(self, scraper):
        super().__init__()
        self.scraper = scraper

    def run(self):
        """Scrape a property link."""
        self.scraper.scrape()
        with print_lock:
            print(f"{self.scraper.page_url} is scraped.")


test_links = [
    "https://www.hansimmo.be/loft-te-koop-in-antwerpen/9676",
    "https://www.hansimmo.be/woning-te-koop-in-edegem/9675",
    "https://www.hansimmo.be/woning-te-koop-in-stabroek/9674",
    "https://www.hansimmo.be/opbrengsteigendom-te-koop-in-antwerpen/9673",
    "https://www.hansimmo.be/gelijkvloers-te-koop-in-berchem/9670",
    "https://www.hansimmo.be/appartement-te-koop-in-antwerpen/9669",
    "https://www.hansimmo.be/appartement-te-koop-in-antwerpen/9668",
    "https://www.hansimmo.be/woning-te-koop-in-deurne/9667",
    "https://www.hansimmo.be/opbrengsteigendom-te-koop-in-deurne/9666",
    "https://www.hansimmo.be/appartement-te-koop-in-antwerpen/9664",
    "https://www.hansimmo.be/appartement-te-koop-in-antwerpen/9663",
    "https://www.hansimmo.be/gemengd-gebouw-te-koop-in-borsbeek/9661",
    "https://www.hansimmo.be/parking-garagebox-te-koop-in-stabroek/9659",
    "https://www.hansimmo.be/appartement-te-koop-in-deurne/9657",
    "https://www.hansimmo.be/woning-te-koop-in-kapellen/9656",
    "https://www.hansimmo.be/appartement-te-koop-in-borgerhout/9655",
    "https://www.hansimmo.be/woning-te-koop-in-sint-antonius/9654",
    "https://www.hansimmo.be/appartement-te-koop-in-stabroek/9646",
    "https://www.hansimmo.be/appartement-te-koop-in-stabroek/9645",
    "https://www.hansimmo.be/gelijkvloers-te-koop-in-stabroek/9644",
    "https://www.hansimmo.be/gelijkvloers-te-koop-in-stabroek/9643",
    "https://www.hansimmo.be/appartement-te-koop-in-antwerpen/9639",
]


threads = [PropertyThread(ImmoHansProp(link)) for link in test_links]
for t in threads:
    t.start()

for t in threads:
    t.join()

results = [thread.scraper.get_property() for thread in threads]
pass