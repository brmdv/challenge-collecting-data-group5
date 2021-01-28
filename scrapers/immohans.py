from bs4 import BeautifulSoup as bs

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
        self._links = [link.attrs["href"] for link in link_tags]


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
            self._property.property_type = "appartment"
            self._property.property_subtype = property_type
        else:
            self._property.property_type = "other"
            self._property.property_subtype = property_type

        pass