import pytest
from bfex.common.exceptions import *


class TestExceptions(object):

    def test_exceptions(self):
        code = 4
        exception = DataIngestionException("my_message", code)
        assert exception.code == code

        exception = WorkflowException("my_message", code)
        assert exception.code == code

        exception = WorkflowTaskArgumentException("my_message", code)
        assert exception.code == code
