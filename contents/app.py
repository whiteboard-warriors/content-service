from flask import Flask
from flask_cors import CORS
from flask_restplus import Api


def create_app(db, db_config):
    from contents.articles.api import api_ns
    app = Flask(__name__)
    CORS(app)
    api = Api(app, version='1.0', title="Contents API")

    app.config.update(db_config)
    db.init_app(app)
    app.db = db

    api.add_namespace(api_ns)
    return app
