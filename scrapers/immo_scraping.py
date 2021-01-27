from ..property_structure import Property


class ImmoScraper:
    """Base class for an immo scraper. All other scrapers should inherite from this one."""

    def __init__(self, page_url):
        self.page_url = page_url
        # Download to html file
        self._download_page()

    def _download_page(self):
        """Downloads the page for internal purposes."""
        pass


class ImmoPageScraper(ImmoScraper):
    """Gets all information for a certain house/appartment."""

    def __init__(self, page_url):
        super().__init__(page_url)
        self._property = Property()

    def scrape(self):
        """Reimplement this method for every scraper."""
        pass


class ImmoListScraper(ImmoScraper):
    """Scrape an index on the site to get links."""

    pass
