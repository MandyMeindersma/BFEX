import pytest
import requests
from bfex.components.scraper.orcid_scraper import OrcIdScraper
from bfex.components.scraper.scraper_type import ScraperType
from bfex.components.scraper.scraper_factory import ScraperFactory
from bfex.components.scraper.scraper_type import ScraperType
from bfex.models import Faculty, Document, Keywords
from bfex.common.utils import URLs, FacultyNames
from bfex.common.exceptions import WorkflowException
from bfex.components.data_pipeline.tasks.task import Task
from bfex.components.key_generation.rake_approach import *
from bfex.components.data_pipeline.tasks.researchid import *

from test.conftest import is_dev_env


class TestReaseachId():
    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")
    def test_create__success(self):
        link = 'http://www.researcherid.com/rid/C-6729-2008'
        rid = ResearchIdPageScrape()
        obj = Faculty(name="Test.Prof", faculty_id=110, email="test@test.com")
        obj.research_id = link
        res = rid.is_requirement_satisfied(obj)
        assert res is True
        res = rid.run(obj)
        print(res)
        assert res is not None