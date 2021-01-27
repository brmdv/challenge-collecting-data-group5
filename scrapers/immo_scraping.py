import requests

from property_structure import Property


class ImmoScraper:
    """Base class for an immo scraper. All other scrapers should inherit from this one."""

    def __init__(self, page_url: str):
        self.page_url = page_url

        # Download to html file
        self._download_page()

    def _download_page(self):
        """Downloads the page for internal purposes."""
        response = requests.get(self.page_url)
        self._data = response.content


class ImmoPageScraper(ImmoScraper):
    """Gets all information for a certain house/appartment."""

    def __init__(self, page_url: str):
        super().__init__(page_url)
        self._property = Property()

    def scrape(self):
        """Reimplement this method for every scraper. It should get all needed
        information from self._data and save it in self._property
        """
        pass


class ImmoListScraper(ImmoScraper):
    """Scrape an index on the site to get links."""

    pass
