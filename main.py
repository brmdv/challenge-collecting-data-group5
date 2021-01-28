from scrapers.immo_scraping import ImmoPropScraper
from scrapers.immoweb import ImmoWebProp, ImmoWebList

immoweb_links = ImmoWebList("https://www.immoweb.be/en")
immoweb_links.scrape()
immoweb_links.write_links("data/immoweb.txt")
list_house_scrapers = [ImmoWebProp(link) for link in immoweb_links.get_links()]
all_houses = [house.get_property() for house in list_house_scrapers]

