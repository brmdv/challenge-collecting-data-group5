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
        python_button = driver.find_elements_by_xpath(
            "//button[@id='uc-btn-accept-banner']"
        )[0]
        python_button.click()

        # Search for all houses and apartment
        # 1. Select "House and apartment" label
        python_label_button = driver.find_elements_by_xpath(
            "//button[@id='propertyTypesDesktop']"
        )[0]
        python_label_button.click()
        python_house_apartment_button = driver.find_elements_by_xpath(
            "//li[@data-value='HOUSE,APARTMENT']"
        )[0]
        python_house_apartment_button.click()

        # 2. Click on search
        python_search_button = driver.find_elements_by_xpath(
            "//button[@id='searchBoxSubmitButton']"
        )[0]
        python_search_button.click()

        # 3. Get links of houses and apartment in 5 pages
        self._links = []

        # Get links for each page
        for _ in range(334):
            # Initialize attempts count
            attempts_count = 0
            while attempts_count < 5:
                try:
                    links_tags = driver.find_elements_by_xpath("//a[@class='card__title-link']")
                    self._links.extend([link.get_attribute("href") for link in links_tags])
                    break

                except:
                    attempts_count += 1

            # Navigate to next page
            python_label_button = driver.find_elements_by_xpath(
                "//a[@class='pagination__link pagination__link--next button button--text button--size-small']"
            )[0]
            python_label_button.click()


        # print(self._links)
        driver.close()


class ImmoWebProp(ImmoPropScraper):
    """This scraper get information on individual properties on immoweb.be"""

    # Simple function to get values from details table
    @staticmethod
    def get_detail(soup, name):
        """Get detail from table by name."""
        # Find cell
        tag = soup.find("th", text=re.compile(name, re.IGNORECASE))
        if tag is None:
            return None
        # Info is in sibling tag
        data = tag.next_sibling.next_sibling.contents[0].strip().lower()

        # Convert booleans
        if data in ["yes", "no"]:
            return True if data == "yes" else "False"
        else:
            return data

    def scrape(self):
        """Create a Property instance from provided url."""

        # download page
        self._download_page()

        # parse data
        soup = bs(self._data, features="lxml")

        # 1. locality: str = None
        # label = soup.select_one('th:-soup-contains("locality")')
        # self._property.locality = label.next_sibling.next_sibling.contents[0].strip()
        self._property.locality = self.get_detail(soup, "locality")
        # if locality not specified in the info table, get it from the url
        if self._property.locality is None:
            self._property.locality = self.page_url.split("/")[7]

        # 2. property_type: str = None
        try:
            property_type = soup.select_one(".classified__title").text.strip().lower()
            if "house" in property_type or "house" in self.page_url:
                self._property.property_type = "house"
            elif "apartment" in property_type or "apartment" in self.page_url:
                self._property.property_type = "apartment"
        except:
            if "house" in self.page_url:
                self._property.property_type = "house"
            elif "apartment" in self.page_url:
                self._property.property_type = "apartment"

        # 3. property_subtype: str = None
        house_subtype = [
            "Bungalow",
            "Chalet",
            "Castle",
            "Farmhouse",
            "Country cottage",
            "Exceptional property",
            "Apartment block",
            "Mixed-use building",
            "Town-house",
            "Mansion",
            "Villa",
            "Other properties",
            "Country house",
            "Pavilion",
        ]

        apartment_subtype = [
            "Ground floor",
            "Duplex",
            "Triplex",
            "Studio",
            "Penthouse",
            "Loft",
            "Kot",
            "Service flat",
        ]

        property_subtype = soup.select_one(".classified__title").text.strip().lower()
        if property_subtype in house_subtype:
            self._property.property_subtype = property_subtype
            self._property.property_type = "house"
        elif property_subtype in apartment_subtype:
            self._property.property_subtype = property_subtype
            self._property.property_type = "apartment"

        # 4. price: float = None
        try:
            price = soup.select_one('span:-soup-contains("€")').text
            price = price.replace("€", "").replace(
                ",", ""
            )  # convert into right number format
            # take the min price available
            min_price = min(re.findall("(\d+)", price))
            self._property.price = float(min_price)
        except:
            self._property.price = None


        # 5. sale_type: str = None

        # 6. number_rooms: int = None
        # label = soup.select_one('th:-soup-contains("Bedrooms")')
        # self._property.number_rooms = int(label.next_sibling.next_sibling.contents[0].strip())
        self._property.number_rooms = self.get_detail(soup, "Bedrooms")
        # Convert number_rooms into integer if not None
        self._property.number_rooms = (
            int(self._property.number_rooms) if self._property.number_rooms else None
        )

        # 7. area: float = None
        # label = soup.select_one('th:-soup-contains("area")')
        # self._property.area = float(label.next_sibling.next_sibling.contents[0].strip())
        self._property.area = self.get_detail(soup, "area")
        # Convert area into float if not None
        self._property.area = (
            float(self._property.area) if self._property.area else None
        )

        # 8. fully_equipped_kitchen: bool = None
        kitchen_type = self.get_detail(soup, "Kitchen type")
        # Determine if the kitchen is fully equipped or not
        not_installed_labels = ["notinstalled", "uninstalled", "not installed"]
        installed_labels = ["fully", "hyper", "installed"]
        if kitchen_type is not None:
            if any(label in kitchen_type for label in not_installed_labels):
                self._property.fully_equipped_kitchen = False
            elif any(label in kitchen_type for label in installed_labels):
                self._property.fully_equipped_kitchen = True

        # 9. is_furnished: bool = None
        self._property.is_furnished = self.get_detail(soup, "Furnished")

        # 10. has_open_fire: bool = None
        fireplace = self.get_detail(soup, "fireplace")
        # Determine if there is a fireplace
        if fireplace is not None:
            self._property.has_open_fire = True if int(fireplace) > 0 else False

        # 11. has_terrace: bool = None ; # 12. terrace_area: float = None
        terrace = self.get_detail(soup, "Terrace")
        # Determine if there is a terrace
        if terrace is not None:
            if terrace == 'yes':
                self._property.has_terrace = True
                self._property.terrace_area = None # None as the terrace area is not specified
            elif terrace == 'no':
                self._property.has_terrace = False
                self._property.terrace_area = 0
            else:
                try:
                    terrace = float(terrace)
                    self._property.has_terrace = True if terrace > 0 else False
                    self._property.terrace_area = terrace
                except:
                    self._property.has_terrace = None
                    self._property.terrace_area = None

        # 13. has_garden: bool = None
        garden = self.get_detail(soup, "Garden")
        # Determine if there is a garden
        if garden is not None:
            self._property.has_garden = True if float(garden) > 0 else False

        # 14. garden_area: float = None
        self._property.garden_area = float(garden) if garden else None

        # 15. land_surface: float = None

        # 16. land_plot_area: float = None
        self._property.land_plot_area = self.get_detail(soup, "Surface of the plot")
        # Convert area into float if not None
        self._property.land_plot_area = (
            float(self._property.land_plot_area)
            if self._property.land_plot_area
            else None
        )

        # 17. number_facades: int = None
        self._property.number_facades = self.get_detail(soup, "frontage")
        # Convert number_facades into integer if not None
        self._property.number_facades = (
            int(self._property.number_facades)
            if self._property.number_facades
            else None
        )

        # 18. has_swimming_pool: bool = None
        self._property.has_swimming_pool = self.get_detail(soup, "Swimming")

        # 19. building_state: str = None
        self._property.building_state = self.get_detail(soup, "condition")

