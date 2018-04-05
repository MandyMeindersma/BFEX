from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.components.search_engine import parser, builder
from bfex.models import Faculty, Keywords
from bfex.common.schema import FacultySchema, KeywordSchema
from bfex.blueprints.search_api import SearchAPI

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

class BatchSearchAPI(Resource):
    
    def get(self):
        query = request.args.get('query')
        approach = request.args.get('approach')
        approach = int(approach)

        if query is None or approach is None:
            abort(400)

        q_parser = parser.QueryParser()
        q_builder = builder.QueryBuilder()

        try:
            pf_query = q_parser.parse_query(query)
        except parser.QueryException:
            abort(400)

        keywords_elastic_query = q_builder.build(pf_query)        
        response = Keywords.search().query(keywords_elastic_query).execute()    
        faculty_with_keywords = SearchAPI.get_faculty_with_keywords(response)

        empty_profs = []
        for faculty_id, keywords in faculty_with_keywords.items():
            filtered_keywords = []
            for keyword_obj in keywords:
                if keyword_obj.approach_id == approach:
                    filtered_keywords.append(keyword_obj)
            faculty_with_keywords[faculty_id] = filtered_keywords
            
            if len(filtered_keywords) == 0:
                empty_profs.append(faculty_id)
        
        for faculty_id in empty_profs:
            del faculty_with_keywords[faculty_id]

        return {
            "data": SearchAPI.create_results(faculty_with_keywords, dept_filter=[])
        }

api.add_resource(BatchAPI, '/batch')
api.add_resource(BatchSearchAPI, '/batch/search')
