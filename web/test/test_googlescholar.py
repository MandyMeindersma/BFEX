import pytest
import requests
from bfex.components.scraper.orcid_scraper import OrcIdScraper
from bfex.components.scraper.scraper_type import ScraperType
from bfex.components.scraper.scraper_factory import ScraperFactory
from bfex.components.scraper.scraper_type import ScraperType
from bfex.models import Faculty, Document
from bfex.common.utils import URLs, FacultyNames
from bfex.common.exceptions import WorkflowException
from bfex.components.data_pipeline.tasks.task import Task
from bfex.components.key_generation.rake_approach import *
from bfex.components.data_pipeline.tasks.googlescholar import *

from test.conftest import is_dev_env


class TestGoogleScholar():
    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")
    def test_create__success(self):
        link = 'https://scholar.google.ca/citations?user=KffJRdgAAAAJ&hl=en&oi=sra'
        ga = GoogleScholarPageScrape()
        obj = Faculty(name="Test.Profman", faculty_id=115, email="test@test.com")
        obj.google_scholar = link
        res = ga.is_requirement_satisfied(obj)
        assert res is True
        res = ga.run(obj)
        print(res)
        assert res != None
