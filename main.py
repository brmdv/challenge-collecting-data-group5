from scrapers.immo_scraping import ImmoPropScraper
from scrapers.immohans import ImmoHansProp, ImmoHansList

hans_links = ImmoHansList("https://www.hansimmo.be/te-koop")
hans_links.scrape()
hans_links.write_links("data/hans.txt")
list_house_scrapers = [ImmoHansProp(link) for link in hans_links.get_links()]
all_houses = [house.get_property() for house in list_house_scrapers]

for house in all_houses:
    house
pass
