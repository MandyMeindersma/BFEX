import pytest
from bfex.components.scraper.scraper_factory import *
from bfex.components.scraper.scraper_type import ScraperType

class TestScraperFactory():
    def test_create__profile(self):
        url = "http:/fake.url"
        my_scraper = ScraperFactory.create_scraper(url, ScraperType.PROFILE)
        
        assert my_scraper is not None
        assert isinstance(my_scraper, ProfileScraper)
        assert not isinstance(my_scraper, OrcIdScraper)
        assert not isinstance(my_scraper, ResearchIdScraper)

    def test_create__orc(self):
        url = "http:/fake.url"
        my_scraper = ScraperFactory.create_scraper(url, ScraperType.ORCID)
        
        assert my_scraper is not None
        assert isinstance(my_scraper, OrcIdScraper)
        assert not isinstance(my_scraper, ResearchIdScraper)
        assert not isinstance(my_scraper, ProfileScraper)

    def test_create__research(self):
        url = "http:/fake.url"
        my_scraper = ScraperFactory.create_scraper(url, ScraperType.RESEARCHID)
        
        assert my_scraper is not None
        assert isinstance(my_scraper, ResearchIdScraper)
        assert not isinstance(my_scraper, OrcIdScraper)
        assert not isinstance(my_scraper, ProfileScraper)