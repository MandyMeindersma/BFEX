import os
import pytest

from elasticsearch_dsl import connections
from bfex.models import initialize_models


@pytest.fixture(scope="session", autouse=True)
def setup_elastic_connection(request):
    """Creates a connection to elasticsearch for use in tests.

    If the environment variable PYTEST_ENV is set, and a connection does
    not already exist, a new one will be created. Runs before every test.
    """
    if is_dev_env():
        return
    
    try:
        connections.get_connection()
    except KeyError:
        elastic_host = os.getenv("ELASTIC_HOST", "localhost")
        connections.create_connection(hosts=[elastic_host])
        initialize_models()


def is_dev_env():
    """Checkis if the environment variable PYTEST_ENV is not dev."""
    return os.getenv("PYTEST_ENV", "dev") == "dev"
