from contents.db import db
from contents.models import BaseModel


class ArticleModel(BaseModel):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    slug = db.Column(db.String(150), nullable=False, index=True, unique=True)
    title = db.Column(db.String(130), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), nullable=True)
    author_id = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated = db.Column(db.DateTime, default=db.func.current_timestamp(),
                        onupdate=db.func.current_timestamp())
    published = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),
                            nullable=True)
    category = db.relationship('CategoryModel',
                               backref=db.backref('articles', lazy=True))

    def __repr__(self):
        """Article info"""
        return f'<Article id={self.id} title={self.title}>'


class CategoryModel(BaseModel):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'
