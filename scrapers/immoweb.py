"""
This is a custom scraper for "immoweb.be".
"""
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re

# import local modules
from scrapers.immo_scraping import ImmoListScraper, ImmoPropScraper


class ImmoWebList(ImmoListScraper):
    """Scrape links to immo listing pages from "immoweb.be"."""

    def scrape(self):
        """Get all links from the provided url."""

        # Download page
        # self._download_page()

        # parse with Beautifulsoup
        # soup = bs(self._data)

        # Get listed links
        # link_tags = soup.main.find_all("a", attrs={"class": "property-content"})
        # self._links = [link.attrs["href"] for link in link_tags]

        # Create webdriver object
        driver = webdriver.Firefox()

        # Wait 30 ms to navigate to the webpage
        driver.implicitly_wait(30)
        driver.get(self.page_url)

        # When opening the url on Firefox, a pop-up window appears.
        # Click on "Keep browsing" to get to the actual page.
        python_button = driver.find_elements_by_xpath("//button[@id='uc-btn-accept-banner']")[0]
        python_button.click()

        # Search for all houses and apartment
        # 1. Select "House and apartment" label
        python_label_button = driver.find_elements_by_xpath("//button[@id='propertyTypesDesktop']")[0]
        python_label_button.click()
        python_house_apartment_button = driver.find_elements_by_xpath("//li[@data-value='HOUSE,APARTMENT']")[0]
        python_house_apartment_button.click()

        # 2. Click on search
        python_search_button = driver.find_elements_by_xpath("//button[@id='searchBoxSubmitButton']")[0]
        python_search_button.click()

        # 3. Get links of houses and apartment in 5 pages
        self._links = []

        # Get links for each page
        for _ in range(5):
            links_tags = driver.find_elements_by_xpath("//a[@class='card__title-link']")
            for link in links_tags:
                self._links.append(link.get_attribute('href'))

            # Navigate to next page
            python_label_button = driver.find_elements_by_xpath("//a[@class='pagination__link pagination__link--next button button--text button--size-small']")[0]
            python_label_button.click()

        
        # print(self._links)
        driver.close()


class ImmoWebProp(ImmoPropScraper):
    """This scraper get information on individual properties on immoweb.be"""

    def scrape(self):
        """Create a Property instance from provided url."""

        # download page
        self._download_page()

        # parse data
        soup = bs(self._data)

        # Get property information
        # title_details = soup.select_one("#detail-title")
        # details_section = soup.select_one("section#detail-details")

        # 1. locality: str = None
        label = soup.select_one('th:-soup-contains("locality")')
        self._property.locality = label.next_sibling.next_sibling.text.strip()

        # 2. property_type: str = None
        property_type = soup.select_one('classified__title')
        if 'house' in property_type:
            self._property.property_type = 'house'
        elif 'apartment' in property_type:
            self._property._property.property_type = 'apartment'


        # # property type
        # property_type = title_details.select_one(".category").text.strip().lower()
        # if "woning" in property_type:
        #     self._property.property_type = "house"
        # elif property_type in ["appartement", "loft", "gelijkvloers"]:
        #     self._property.property_type = "appartment"
        #     self._property.property_subtype = property_type
        # else:
        #     self._property.property_type = "other"
        #     self._property.property_subtype = property_type

        # 3. property_subtype: str = None
        # 4. price: float = None
        # 5. sale_type: str = None
        # 6. number_rooms: int = None
        # 7. area: float = None
        # 8. fully_equipped_kitchen: bool = None
        # 9. is_furnished: bool = None
        # 10. has_open_fire: bool = None
        # 11. has_terrace: bool = None
        # 12. has_garden: bool = None
        # 13. land_surface: float = None
        # 14. land_plot_area: float = None
        # 15. number_facades: int = None
        # 16. has_swimming_pool: bool = None
        # 17. building_state: str = None

        # # locality: get place name from address
        # self._property.locality = (
        #     title_details.select_one(".address")
        #     .text.strip()
        #     .split(" ")[-1]
        #     .capitalize()
        # )


        # # simple function to get values from details table
        # def get_detail(name):
        #     """Get detail from table by name."""
        #     # find cell
        #     tag = details_section.find("dt", text=re.compile(name, re.IGNORECASE))
        #     if tag is None:
        #         return False
        #     # info is in sibling dd tag
        #     data = tag.parent.dd.text.strip()
        #     # convert booleans
        #     if data in ["ja", "nee"]:
        #         return True if data == "ja" else "False"
        #     else:
        #         return data

        # # price
        # price = get_detail("prijs")
        # price = (
        #     price.replace("€ ", "").replace(".", "").replace(",", ".")
        # )  # convert to English number format
        # self._property.price = float(price)

        # # number of rooms
        # rooms = int(get_detail("slaapkamer"))
        # self._property.number_rooms = rooms

        # # area
        # area = get_detail("bewoonbare opp")
        # area = float(price.replace(" m²", "").replace(".", "").replace(",", "."))
        # self._property.area = area

        # # Kitchen
        # kitchen_info = get_detail("type keuken")
        # self._property.fully_equipped_kitchen = kitchen_info

        # # Is furnished? Not specified on website but probably not
        # self._property.is_furnished = False

        # # for open fire, just look if mentioned in description
        # self._property.has_open_fire = (
        #     "open haard" in soup.select_one("#description").text.lower()
        # )

        # self._property.has_terrace = get_detail("terras")

        # pass