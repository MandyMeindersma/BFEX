import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.persist import *
import elasticsearch_dsl as es
from test.conftest import is_dev_env
from time import sleep


class TestPersistTasks(object):

    """Example of how to write a test that will not run on your dev machine."""

    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")
    def test_persist_faculty(self):
        assert es.connections.get_connection()

    def test_requirement_not_satisfied(self):
    
        name = "name"
        data =((name))

        requirement = UpdateFacultyFromScrape.is_requirement_satisfied(self,data)

        assert requirement is False

    def test_requirement_satisfied(self):

        name = "William.Allison"
        scrapp = Scrapp()
        scrapp.set_text("some text")

        data = (name,scrapp)

        requirement = UpdateFacultyFromScrape.is_requirement_satisfied(self,data)

        assert requirement is True

    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")    
    def test_update_from_scrape(self):
        faculty = Faculty(name="William.Allison", full_name="Allison, William.", faculty_id=379, email="william.allison@ualberta.ca")
        faculty.save()
        scrapp = Scrapp()
        scrapp.add_meta("orcid_link","http://orcid.org/0000-0002-8461-4864")
        scrapp.add_meta("researchid_link","http://www.researcherid.com/rid/A-2612-2014")
        scrapp.add_meta("googlescholar_link", "www.this.is.a.real.link.com")
        scrapp.add_meta("text", "This is super real text from a real source.")
        sleep(3)
        data = (faculty.name,scrapp)
        task = UpdateFacultyFromScrape()
        res = task.run(data)

        assert res != None
        
    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")    
    def test_update_after_scrape(self):
        keywords = []
        key = Keywords(faculty_id=379, datasource="GoogleScholar", approach_id=1, keywords="Bob")
        key.save()
        keywords.append(key)
        key = Keywords(faculty_id=379, datasource="GoogleScholar", approach_id=3, keywords="Jim")
        keywords.append(key)
        sleep(3)
        data = keywords
        task = UpdateKeywordsFromGenerator()
        res = task.is_requirement_satisfied(data)
        assert res is True
        res = task.run(data)

        assert res != None

