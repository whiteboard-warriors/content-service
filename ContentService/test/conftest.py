import pytest
import os
from pathlib import Path
import http.client
from contents.app import create_app
from contents.db import db
from .constants import PRIVATE_KEY
from contents import token_validation
from contents.articles.models import CategoryModel
from faker import Faker
fake = Faker()


@pytest.fixture
def app():
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    path = dir_path / '..'

    # Database initialisation
    FILE_PATH = f'{path}/testdb.sqlite3'
    DB_URI = 'sqlite+pysqlite:///{file_path}'
    db_config = {
        'SQLALCHEMY_DATABASE_URI': DB_URI.format(file_path=FILE_PATH),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }

    application = create_app(db, db_config)
    application.app_context().push()
    application.db.drop_all()
    application.db.create_all()
    # Create some categories
    c1 = CategoryModel(name="Algorithm")
    c2 = CategoryModel(name="Data Structures")
    c3 = CategoryModel(name="Graphs")
    application.db.session.add_all([c1, c2, c3])
    application.db.session.commit()

    yield application

    # Explicitly close DB connection
    application.db.session.close()
    application.db.drop_all()


@pytest.fixture
def article_fixture(client):
    '''
    Generate five articles in the system.
    '''
    article_ids = []

    user_payload = {
        'userid': 1,
        'username': 'whiteboardwarriors',
        'email': 'engineer@whiteboardwarriors.org'
    }

    for _ in range(5):
        article = {
            'slug': fake.slug(),
            'title': fake.text(250),
            'content': fake.text(500),
            'category_id': fake.random_int(1, 3),
            'status': 'DRAFT'
        }
        header = token_validation.generate_token_header(user_payload,
                                                        PRIVATE_KEY)
        headers = {
            'Authorization': header,
        }
        response = client.post('/api/me/articles', data=article,
                               headers=headers)
        assert http.client.CREATED == response.status_code
        result = response.json
        article_ids.append(result['id'])

    yield article_ids
