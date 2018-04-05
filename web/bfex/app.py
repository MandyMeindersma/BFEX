import os
from flask import Flask, request, send_from_directory
from bfex.blueprints import *
from bfex.blueprints.faculty_api import faculty_bp
from bfex.blueprints.search_api import search_bp
from bfex.blueprints.batch_api import batch_bp
from bfex.blueprints.workflow_api import workflow_bp
from flask_cors import CORS, cross_origin
from bfex.models import initialize_models
from bfex.components.key_generation.rake_approach import *
from bfex.components.key_generation.generic_approach import *
from bfex.components.key_generation.key_generator import *


def create_app():
    """Instantiates and configures the BFEX application.

    First, any environment variables needed are retrieved using sensible defaults for a development environment.
    Next, any initializations that need to be performed are done. Currently, we instantiate a connection to elastic
    and initialize the model definitions in the database.
    Finally, API blueprints are registered to the application so they can be accessed.

    Environment Variables:
    ELASTIC_HOST: URL of the elasticsearch instance to be used. If undefined, localhost is used.

    :return An initialized and configured instance of a Flask application.
    """
    from elasticsearch_dsl.connections import connections
    
    app = Flask("bfex", static_url_path='')
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    # Elasticsearch connection setup
    elastic_host = os.getenv("ELASTIC_HOST", "localhost")
    connections.create_connection(hosts=[elastic_host])
    initialize_models()

    app.register_blueprint(faculty_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(batch_bp)
    app.register_blueprint(workflow_bp)
    app.register_blueprint(grants_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(keyword_bp)
    app.register_blueprint(lexicon_bp)

    return app


app = create_app()