from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.components.search_engine import parser, builder
from bfex.models import Faculty, Keywords
from bfex.common.schema import FacultySchema, KeywordSchema

# Setup the blueprint and add to the api.
search_bp = Blueprint("search_api", __name__)
api = Api(search_bp)


class SearchAPI(Resource):
    """Contains methods for performing search over keywords."""

    def get(self):
        """HTTP Get that enables boolean query processing and search."""
        query = request.args.get('query')
        dept = request.args.get('department')

        if query is None:
            abort(400)

        # Take dept string and turn it into an easy to compare set.
        try:
            if dept is not None:
                dept_filter = set([x.strip() for x in dept.split(',')])
        except:
            abort(400)

        q_parser = parser.QueryParser()
        q_builder = builder.QueryBuilder()

        pf_query = q_parser.parse_query(query)
        elastic_query = q_builder.build(pf_query)

        response = Keywords.search().query(elastic_query).execute()

        # Build keyword set for each faculty
        keyword_schema = KeywordSchema(exclude=['faculty_id'])
        faculty_with_keywords = {}
        for keywords in response:
            if keywords.faculty_id not in faculty_with_keywords:
                faculty_with_keywords[keywords.faculty_id] = []

            faculty_with_keywords[keywords.faculty_id].append(keywords)        

        # Build json representations with nested keywords
        schema = FacultySchema()
        results = []
        for faculty_id, keywords in faculty_with_keywords.items():
            faculty = Faculty.safe_get(faculty_id)

            if faculty is None or \
                (dept is not None and faculty.department not in dept_filter): 
                continue
            
            faculty.generated_keywords = keywords
            results.append(schema.dump(faculty))
            
        return {
            "data": results
        }


api.add_resource(SearchAPI, '/search')
