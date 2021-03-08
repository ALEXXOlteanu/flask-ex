import os
from flask import Flask
from flask_migrate import Migrate
from whitenoise import WhiteNoise
from werkzeug.contrib.fixers import ProxyFix

from app.extensions import db


def create_app(config_filename):
    """
    Factory to create the application using a file

    :param config_filename: The name of the file that will be used for configuration.
    :return: The created application
    """
    app = Flask(__name__)
    app.config.from_object(config_filename)

    setup_db(app)

    # Add ProxyFix for HTTP headers
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # add whitenoise for static files
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/')

    print("Creating a Flask app with DEBUG: {}".format(app.debug))

    @app.route("/")
    def hello():
        return curl -k -X GET -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluMiIsInJvbGUiOiJBZG1pbiIsInBlcm1pc3Npb25zIjpbImFjY2Vzc19pbmZvcm1hdGlvbl9hc3NldHMiLCJ2aWV3X3F1YWxpdHkiLCJtYW5hZ2VfaW5mb3JtYXRpb25fYXNzZXRzIiwibWFuYWdlX21ldGFkYXRhX2ltcG9ydCIsIm1hbmFnZV9kaXNjb3ZlcnkiLCJtYW5hZ2VfcXVhbGl0eSIsInZpZXdfZ292ZXJuYW5jZV9hcnRpZmFjdHMiLCJhdXRob3JfZ292ZXJuYW5jZV9hcnRpZmFjdHMiLCJhY2Nlc3NfY2F0YWxvZyIsImFkbWluaXN0cmF0b3IiLCJjYW5fcHJvdmlzaW9uIiwibWFuYWdlX2NhdGFsb2ciLCJtYW5hZ2VfZ292ZXJuYW5jZV93b3JrZmxvdyIsIm1hbmFnZV9jYXRlZ29yaWVzIiwidmlydHVhbGl6ZV90cmFuc2Zvcm0iLCJzaWduX2luX29ubHkiXSwiZ3JvdXBzIjpbMTAwMDBdLCJzdWIiOiJhZG1pbjIiLCJpc3MiOiJLTk9YU1NPIiwiYXVkIjoiRFNYIiwidWlkIjoiMTAwMDMzMTA1NiIsImF1dGhlbnRpY2F0b3IiOiJkZWZhdWx0IiwiaWF0IjoxNjE1MjAwMDI1LCJleHAiOjE2MTUyNDMxODl9.jb-SOWgbc7OlqXXRD8tzsyti2wDQBnUkwIKvKmsc88uXQep6GuL2-GhCkbCUuRA_O50tISllLf40z3DdHDsy_BVQTNt_BFE7XgE7fFtL2UCqq0NZwmwclMvQm2LDA2CF5dw2EtJN6nNTIrxeyjA-frKRXrkoAtoTwxx1SDY-wf9ZZWxyVMu37083mys4mx48qU4px4iiTB_q_1FPW0hqOLAwgPJWDNyg1hB5N365XiT4o6XxnTu9NEo4y1lBwQn-0u1GHR6EW1rroGVY0QZH820ZSftRuZRPbdI2Van96gNbwkHXMiC1TG_Kun4LSU73HDpL6sILi2jYF2tQzFF_ww" -H "cache-control: no-cache" "https://cp4d-poc-cpd-cp4d-poc.apps.cp4d-poc.cp4d.ichp.nietsnel.nu/icp4d-api/v1/users"
        
#         return "Hello World 2 OA!: DEBUG: {} Environment: {}".format(app.debug, app.env)

    return app


def setup_db(app):
    """
    Creates a database for the application
    :param app: Flask application to use
    :return:
    """
    print("Database Engine is: {}".format(app.config.get("DB_ENGINE", None)))
    if app.config.get("DB_ENGINE", None) == "postgresql":
        print("Setting up PostgreSQL database")
        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            app.config["DB_USER"],
            app.config["DB_PASS"],
            app.config["DB_SERVICE_NAME"],
            app.config["DB_PORT"],
            app.config["DB_NAME"]
        )
    else:
        _basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(_basedir, 'webapp.db')

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)
    db.app = app
