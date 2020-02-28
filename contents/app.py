from flask import Flask
from flask_cors import CORS


def create_app(db, db_config):
    app = Flask(__name__)
    CORS(app)

    app.config.update(db_config)
    db.init_app(app)
    app.db = db

    return app
