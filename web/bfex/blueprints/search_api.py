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
            else:
                dept_filter = set()
        except:
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
        
        SearchAPI.add_name_search_results(faculty_with_keywords, pf_query)
        
        return {
            "data": SearchAPI.create_results(faculty_with_keywords, dept_filter)
        }
    
    @staticmethod
    def get_faculty_with_keywords(response):
        """ Builds a dictionary of faculty ids to list of all keywords.

        Finds all keywords that belong to a professor, and creates a list. The
        list contains the json representation of the Keywords model, not
        including the faculty id.
        :param response: List of faculty model objects.
        :returns: Dictionary of integer id's to a list of strings.
        """
        faculty_with_keywords = {}
        for keywords in response:
            if keywords.faculty_id not in faculty_with_keywords:
                faculty_with_keywords[keywords.faculty_id] = []

            faculty_with_keywords[keywords.faculty_id].append(keywords) 
        
        return faculty_with_keywords

    @staticmethod
    def create_results(faculty_with_keywords, dept_filter):
        """ Creates the json representation of a faculty member, including all keywords.

        :param faculty_with_keywords: A dictionary of id's to lists of keywords.
            The keywords are inserted into the faculty object before being dumped to json.
        :param dept_filter: List of string departments to be included in the results. If a
            professor does not belong one of the departments, they are not included.
            All professors are included if the filter is empty.
        :returns: List of JSON objects, each representing a faculty member and keywords.
        """
        # Build json representations with nested keywords
        schema = FacultySchema()
        results = []
        for faculty_id, keywords in faculty_with_keywords.items():
            faculty = Faculty.safe_get(faculty_id)

            if faculty is None or \
                    (len(dept_filter) > 0 and faculty.department not in dept_filter):
                continue
            
            faculty.generated_keywords = keywords
            results.append(schema.dump(faculty))
        
        return results

    @staticmethod
    def add_name_search_results(faculty_with_keywords, pf_query):
        """ Inserts results of pf_query on faculty index into faculty_with_keywords.

        If an faculty is returned from the query, but does not currently exist in
        faculty_with_words, the faculty member plus their entire keyword set,
        is inserted into the dictionary.
        :param faculty_with_keywords: Dictionary of faculty id's to keywords.
        :param pf_query: Postfix query created by the Query Builder.
        :returns: faculty_with_keywords also containing faculty whose names match the
            query.
        """
        print("QUERY", pf_query)
        # Add functionality of searching names in query.
        q_builder = builder.QueryBuilder()
        name_elastic_query = q_builder.build(pf_query, search_field="full_name")
        print(name_elastic_query)
        names_response = Faculty.search().query(name_elastic_query).execute()

        print(names_response)

        for faculty in names_response:
            # We already have the faculty who was searched in the results.
            print(faculty)
            if faculty.faculty_id in faculty_with_keywords:
                continue

            faculty_keywords = Keywords.search()\
                .query('match', faculty_id=faculty.faculty_id).execute()
            
            faculty_with_keywords[faculty.faculty_id] = faculty_keywords

api.add_resource(SearchAPI, '/search')
