from marshmallow import Schema, fields, post_load

from bfex.models import *


class KeywordSchema(Schema):
    """Marshmallow schema used for validating Faculty JSON objects.
    A marshmallow schema allows us to easily extract information from JSON input, while at the same time, performing
    basic validation of that data.
    """
    faculty_id = fields.Integer(load_from="id", required=True)
    datasource = fields.String()
    approach_id = fields.Integer()
    keywords = fields.List(fields.String)

    @post_load
    def _create_faculty(self, data):
        """Turns the extracted json data into an instance of Faculty"""
        return Keywords(meta={}, **data)


class FacultySchema(Schema):
    """Marshmallow schema used for validating Faculty JSON objects.

    A marshmallow schema allows us to easily extract information from JSON input, while at the same time, performing
    basic validation of that data.
    """
    faculty_id = fields.Integer(load_from="id", required=True)
    name = fields.String(required=True)
    full_name = fields.String(load_from="fullName", required=True)
    email = fields.Email(required=True)
    department = fields.String(allow_none=True, missing="Unknown")

    google_scholar = fields.String(load_from="googleScholarId")
    orc_id = fields.String(load_from="orcId")
    sciverse_id = fields.String(load_from="sciverseId")
    research_id = fields.String(load_from="researchId")

    generated_keywords = fields.Nested(KeywordSchema, exclude=('faculty_id',), many=True)

    @post_load
    def _create_faculty(self, data):
        """Turns the extracted json data into an instance of Faculty"""
        return Faculty(meta={'id': data["faculty_id"]}, **data)

    class Meta:
        ordered = True


class GrantSchema(Schema):
    faculty_name = fields.String(load_from="faculty_name", required=True)
    title = fields.String(missing="", required=True)
    text = fields.String(load_from="summary", required=True)
    source = fields.String(missing="nserc")


class DocumentSchema(Schema):
    faculty_id = fields.String(required=True)
    source = fields.String(required=True)

    title = fields.String()
    text = fields.String()
    date = fields.Date()
    keywords = fields.String()

class LexiconSchema(Schema):
    keywords = fields.List(fields.String)