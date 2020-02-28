from contents.app import create_app
from contents.db import db, db_config
from contents.articles.models import CategoryModel, ArticleModel

if __name__ == '__main__':
    app = create_app(db, db_config)
    app.app_context().push()
    app.db.drop_all()
    app.db.create_all()
