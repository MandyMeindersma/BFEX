import pytest
from bfex.components.scraper.scrapp import Scrapp

class TestScrapp():
    def test_create__success(self):
        my_scrapp = Scrapp()
        assert my_scrapp is not None

        my_scrapp.set_name("Eleni")
        assert my_scrapp.formated_name == "Eleni"

        my_scrapp.set_source("Faculty pages")
        assert my_scrapp.data_source == "Faculty pages"

        my_scrapp.set_title("How I became the best prof")
        assert my_scrapp.title == "How I became the best prof"

        my_scrapp.set_text("I made sure to read all of the students tests")
        assert my_scrapp.text == "I made sure to read all of the students tests"

        my_scrapp.set_date("Night before deadline")
        assert my_scrapp.date == "Night before deadline"
