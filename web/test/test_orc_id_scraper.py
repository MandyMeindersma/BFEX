import pytest
from bfex.components.scraper.orcid_scraper import OrcIdScraper
from bfex.components.scraper.scraper_type import ScraperType

base_url = "http://orcid.org/"

class TestOrcIdScraper():
    def test_create__success(self):
        my_scraper = OrcIdScraper(base_url + "0000-0002-8461-4864", ScraperType.ORCID)
        assert my_scraper is not None
        assert my_scraper.url == base_url + "0000-0002-8461-4864"
        assert my_scraper.type == ScraperType.ORCID

        my_scraper.validate_url()

        soup = my_scraper.get_content()
        assert soup is not None

        scrapps = my_scraper.get_scrapps()
        assert scrapps is not None
