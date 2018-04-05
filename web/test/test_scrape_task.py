import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.scrape import *

class TestScrapeTasks(object):
    
    def test_requirement_is_satisfied(self):

        name = "William.Allison"

        requirement = FacultyPageScrape.is_requirement_satisfied(self,name)

        assert requirement is not None


    def test_requirement_is_not_satisfied(self):

        name = "wrongname"

        requirement = FacultyPageScrape.is_requirement_satisfied(self,name)

        assert requirement is False

    def test_scrape_task(self):
        name = "J.Nelson.Amaral"
        task = FacultyPageScrape()
        res = task.is_requirement_satisfied(name)
        assert res is True
        res = task.run(name)
        assert res is not None

    def test_scrape_task(self):
        fac = Faculty(name="J.Nelson.Amaral", faculty_id=123, email="real@email.com")
        task = FacultyPageScrape()
        res = task.is_requirement_satisfied(fac)
        assert res is True
        res = task.run(fac)
        assert res is not None

