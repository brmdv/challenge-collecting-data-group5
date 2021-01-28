import requests
from typing import List

from property_structure import Property


class ImmoScraper:
    """Base class for an immo scraper. All other scrapers should inherit from this one."""

    def __init__(self, page_url: str):
        """Create an ImmoScraper.

        :param page_url: Url to download data from.
        """
        self.page_url = page_url

    def _download_page(self):
        """Downloads the page for internal purposes."""
        response = requests.get(self.page_url)
        self._data = response.content

    def __str__(self) -> str:
        return f"Scraper for {self.page_url}"


class ImmoPropScraper(ImmoScraper):
    """Gets all information for a certain house/appartment."""

    def __init__(self, page_url: str):
        """Create a scraper for a property.

        :param page_url: Url to download data from.
        """
        super().__init__(page_url)
        self._property = Property()
        self._scraped = False

    def scrape(self):
        """Reimplement this method for every scraper. It should get all needed
        information from self._data and save it in self._property
        """
        raise NotImplementedError(
            "This method should be implemented for each individual website."
        )

    def get_property(self):
        """Get the internal Property object."""
        return self._property


class ImmoListScraper(ImmoScraper):
    """Scrape an index on the site to get links."""

    def __init__(self, page_url: str):
        """Create a scraper to get a list of properties from an immo site.

        :param page_url: Url to download data from.
        """
        super().__init__(page_url)
        self._links: List[str] = []

    def get_links(self) -> List[str]:
        """Returns a list of the scraped urls for listed properties."""

        # When not scraped yet, do it now
        if len(self._links) == 0:
            self.scrape()

        return self._links

    def scrape(self):
        """Reimplement this method for every scraper. It should get all links to
        individual pages and save them in self._links
        """

        raise NotImplementedError(
            "This method should be implemented for each individual website."
        )

    def write_links(self, filename: str):
        """Save collected links to txt file.

        :param filename: Path to filename. This will be overwritten without warning.
        """
        with open(filename, "w") as outfile:
            for link in self.get_links():
                outfile.write(link + "\n")
        print(f"{len(self._links)} links from {self.page_url} written to {filename}.")
