from scrapers.immohans import ImmoHansProp, ImmoHansList

list_houses = ImmoHansList("https://www.hansimmo.be/te-koop").get_links()
test = ImmoHansProp("https://www.hansimmo.be/woning-te-koop-in-edegem/9675")
test.scrape()

all_houses = [ImmoHansProp(house).get_property() for house in list_houses]
for house in all_houses:
    house
pass
