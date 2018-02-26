from bfex.components.scraper.orcid_scraper import *
from bfex.components.scraper.researchid_scraper import *
from bfex.components.scraper.profile_scraper import *
from bfex.components.scraper.scraper_type import *


class ScraperFactory(object):

    @staticmethod
    def create_scraper(url, type):
        if type == ScraperType.ORCID:
            return OrcIdScraper(url, type)
        if type == ScraperType.RESEARCHID:
            return ResearchIdScraper(url, type)
        if type == ScraperType.PROFILE:
            return ProfileScraper(url, type)