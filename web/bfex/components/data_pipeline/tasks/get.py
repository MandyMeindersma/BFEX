from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import Faculty
from bfex.common.exceptions import WorkflowException


class GetFacultyFromElasticSearch(Task):
    """
    Gets all Faculty Members data from elastic.
    """
    def __init__(self):
        self.task_name = "Get all Faculty Members"

    def is_requirement_satisfied(self, data):
        """ Checks the requirements for a faculty page scraping are satisfied.

        :param list data: list of all faculty
        :return: True if data is null. Data should be null as we pass 
        nothing into it to run the code
        """

        return data == None

    def run(self, data):
        """ Searches through all results in elastic search
        :param data: str or Faculty instance.
        :return: all faculty
        """
        s = Faculty.search()
        allFaculty = [faculty for faculty in s.scan()]
        return allFaculty


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()