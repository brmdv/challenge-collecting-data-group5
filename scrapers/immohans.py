from bs4 import BeautifulSoup as bs
import re

from scrapers.immo_scraping import ImmoListScraper, ImmoPropScraper


class ImmoHansList(ImmoListScraper):
    """Scrape links to immo listing pages from hansimmo.be."""

    def scrape(self):
        """Get all links from the provided url."""

        # Download page
        self._download_page()

        # parse with Beautifulsoup
        soup = bs(self._data)

        # Get listed links
        link_tags = soup.main.find_all("a", attrs={"class": "property-content"})
        self._links = [
            link.attrs["href"]
            for link in link_tags
            if not "referenties" in link.attrs["href"]
        ]


class ImmoHansProp(ImmoPropScraper):
    """This scraper get information on individual properties on hansimmo.be"""

    def scrape(self):
        """Create a Property instance from provided url."""

        # download page
        self._download_page()

        # parse data
        soup = bs(self._data)

        # get information
        title_details = soup.select_one("#detail-title")
        details_section = soup.select_one("section#detail-details")

        # locality: get place name from address
        self._property.locality = (
            title_details.select_one(".address")
            .text.strip()
            .split(" ")[-1]
            .capitalize()
        )
        # property type
        property_type = title_details.select_one(".category").text.strip().lower()
        if "woning" in property_type:
            self._property.property_type = "house"
        elif property_type in ["appartement", "loft", "gelijkvloers"]:
            self._property.property_type = "apartment"
            self._property.property_subtype = property_type
        else:
            self._property.property_type = "other"
            self._property.property_subtype = property_type

        # simple helper function to get values from details table
        def get_detail(name):
            """Get detail from table by name."""
            # find cell
            tag = details_section.find("dt", text=re.compile(name, re.IGNORECASE))
            # if not found, it's probably False
            if tag is None:
                return False
            # info is in sibling dd tag
            data = tag.parent.dd.text.strip()
            # convert booleans
            if data in ["ja", "nee"]:
                return True if data == "ja" else False
            else:
                return data

        # helper function for Dutch numbers
        def convert_number(text: str) -> float:
            """Convert written number to float"""
            # get number, throw away units
            match = re.search(r"([0-9.,]+)", text)
            if match:
                text = match.group(1)
            # ge from dutch 1.000.000,00 to 1000000.00
            text = text.replace(".", "").replace(",", ".")
            # convert to float if possible
            try:
                return float(text)
            except:
                return text

        # price
        price = get_detail("prijs")
        price = convert_number(price)
        self._property.price = price

        # number of rooms
        rooms = int(get_detail("slaapkamer"))
        self._property.number_rooms = rooms

        # area
        area = get_detail("bewoonbare opp")
        area = convert_number(area)
        self._property.area = area

        # Kitchen, this will be in Dutch
        kitchen_info = get_detail("type keuken")
        self._property.fully_equipped_kitchen = kitchen_info

        # Is furnished? Not specified on website but probably not
        self._property.is_furnished = False

        # for open fire, just look if mentioned in description
        self._property.has_open_fire = (
            "open haard" in soup.select_one("#description").text.lower()
        )

        self._property.has_terrace = bool(get_detail("terras"))
        if self._property.has_terrace:
            terras_area = get_detail("Terras 1")
            if terras_area:
                self._property.terrace_area = convert_number(terras_area)

        self._property.has_garden = bool(get_detail("tuin"))
        if self._property.has_garden:
            try:
                # garden area is saved in same cell
                self._property.garden = convert_number(garden_area)
            except:
                pass

        perceel_opp = get_detail("Perceel opp")
        if perceel_opp:
            self._property.land_plot_area = float(
                perceel_opp.replace(" m²", "").replace(".", "").replace(",", ".")
            )

        # swimming pool
        self._property.has_swimming_pool = get_detail("zwembad")

        # Building state: for now just copy dutch decription
        self._property.building_state = get_detail("Staat")
        pass