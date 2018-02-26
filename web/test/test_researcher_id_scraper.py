import pytest
from bfex.components.scraper.researchid_scraper import ResearchIdScraper
from bfex.components.scraper.scraper_type import ScraperType

base_url = "http://www.researcherid.com/ProfileView.action?returnCode=ROUTER.Success&Init=Yes&SrcApp=CR&queryString="


class TestResearcherIdScraper():
    def test_create__success(self):
        my_scraper = ResearchIdScraper(base_url + "KG0UuZjN5WlSDh3Egt%252BvR7KcT2noXjIhnW%252FR6Bpj4HU%253D&SID=5BJkfitOyV2CIVB1oFx", ScraperType.RESEARCHID)
        assert my_scraper is not None
        assert my_scraper.url == base_url + "KG0UuZjN5WlSDh3Egt%252BvR7KcT2noXjIhnW%252FR6Bpj4HU%253D&SID=5BJkfitOyV2CIVB1oFx"
        assert my_scraper.type == ScraperType.RESEARCHID

        my_scraper.validate_url()

        soup = my_scraper.get_content()
        assert soup is not None

        scrapps = my_scraper.get_scrapps()
        assert scrapps is not None
