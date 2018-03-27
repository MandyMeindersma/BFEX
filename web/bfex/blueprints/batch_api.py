from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.components.search_engine import parser, builder
from bfex.models import Faculty, Keywords
from bfex.common.schema import FacultySchema, KeywordSchema

# Setup the blueprint and add to the api.
batch_bp = Blueprint("batch_api", __name__)
api = Api(batch_bp)


class BatchAPI(Resource):
    """Contains methods for performing batch over keywords."""

    def get(self):
        """HTTP Get that enables boolean query processing and batch."""
        response = Keywords.search()
        schema = KeywordSchema()
        results = [schema.dump(s) for s in response.scan()]

        return {
            "data": results
        }


api.add_resource(BatchAPI, '/batch')
