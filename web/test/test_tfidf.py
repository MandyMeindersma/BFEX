import pytest

from test.conftest import is_dev_env
from bfex.components.key_generation.tfidf_approach import *


class TestTfidf(object):
    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")    
    def test_tfidf(self):
        text = "This is a text document. Words are fun. I do research. Thinking is fun."
        task = TfidfApproach()
        res = task.get_id()
        assert res == 3
        results = task.generate_keywords(text)
        assert results is not None
