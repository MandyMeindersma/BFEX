import pytest
import requests
from bfex.components.scraper.researchid_scraper import ResearchIdScraper
from bfex.components.scraper.scraper_type import ScraperType

base_url = "http://www.researcherid.com/ProfileView.action?returnCode=ROUTER.Success&Init=Yes&SrcApp=CR&queryString=KG0UuZjN5WlSDh3Egt%252BvR3RyhPpglAW%252Bxqd0e24388w%253D&SID=8F9UW21U6UX9w45s1Lh"


class TestResearcherIdScraper():
    def test_create__success(self):
        my_scraper = ResearchIdScraper(base_url, ScraperType.RESEARCHID)
        assert my_scraper is not None
        assert my_scraper.url == base_url
        assert my_scraper.type == ScraperType.RESEARCHID

        my_scraper.validate_url()

        soup = my_scraper.get_content()
        assert soup is not None

        scrapps = my_scraper.get_scrapps()
        assert scrapps is not None
        print(scrapps[0].meta_data["keywords"])

        assert scrapps[0].meta_data["keywords"] is not None
        assert scrapps[0].meta_data["description"] is not None
        assert scrapps[0].data_source is not None

        for scrapp in scrapps[1:]:
            assert scrapp.title is not None
            assert scrapp.data_source is not None

    def test_invalid_url(self):
        my_url = "http://www.asdffghhh.com"
        my_scraper = ResearchIdScraper(my_url, ScraperType.RESEARCHID)
        with pytest.raises(requests.exceptions.ConnectionError):
            my_scraper.get_content()
            
