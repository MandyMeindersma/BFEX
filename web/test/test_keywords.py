import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.keywords import *
import elasticsearch_dsl as es
from test.conftest import is_dev_env
from bfex.components.scraper.scraper_type import ScraperType

class TestKeywordsTask(object):

    def test_requirement_not_satisfied(self):
    
        faculty = Faculty()
        faculty.faculty_id = None

        requirement = GetKeywordsFromScrape.is_requirement_satisfied(self,faculty)

        assert requirement is False

    def test_requirement_satisfied(self):

        faculty = Faculty()
        faculty.faculty_id = 1
        requirement = GetKeywordsFromScrape.is_requirement_satisfied(self,faculty)
        assert requirement is True

    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")
    def test_create__success(self):
        link = 'https://scholar.google.ca/citations?user=KffJRdgAAAAJ&hl=en&oi=sra'
        task = GetKeywordsFromScrape()
        doc = Document(text="This is test text in a document.", faculty_id=375, source="GoogleScholar")
        doc.save()
        res = task.is_requirement_satisfied(doc)
        assert res is True
        res = task.run(doc)
        print(res)
        assert res != None