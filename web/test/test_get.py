import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.get import *
from test.conftest import is_dev_env

class TestGet(object):
    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")    
    def test_update_from_scrape(self):
        data = None
        task = GetFacultyFromElasticSearch()
        res = task.is_requirement_satisfied(data)
        assert res is True
        res = task.run(data)

        assert res is not None