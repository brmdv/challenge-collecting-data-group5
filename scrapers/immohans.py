from bs4 import BeautifulSoup as bs

from scrapers.immo_scraping import ImmoListScraper


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
