import http.client
from flask_restplus import Namespace, Resource, fields
from contents.db import db
from contents import config
from contents.articles.models import ArticleModel
from contents.token_validation import validate_token_header
from flask import abort
from datetime import datetime

# URLs for this namespace are prefixed with /article/
api_ns = Namespace('api', description='Articles API')


def authentication_header_parser(token):
    payload = validate_token_header(token, config.PUBLIC_KEY)
    if payload is None:
        abort(401)
    return payload


# Input and output formats for Article
authentication_parser = api_ns.parser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type=str,
                                   help='Bearer Access Token')

article_parser = authentication_parser.copy()
article_parser.add_argument('slug', type=str, help='Slug', required=True)
article_parser.add_argument('title', type=str, help='Title', required=True)
article_parser.add_argument('content', type=str, help='Content', required=True)
article_parser.add_argument('category_id', type=int,
                            help='Article publish date')
article_parser.add_argument('status', type=str, required=True,
                            help='Article status: DRAFT or PUBLISHED')
model = {
    'id': fields.Integer(),
    'slug': fields.String(),
    'title': fields.String(),
    'content': fields.String(),
    'author_id': fields.Integer(),
    'category_id': fields.Integer(),
    'status': fields.String(),
    'published': fields.DateTime()
}

article_model = api_ns.model('Article', model)


@api_ns.route('/me/articles')
class MeArticle(Resource):

    @api_ns.doc('loggedin_user_articles')
    @api_ns.expect(authentication_parser)
    @api_ns.marshal_with(article_model)
    def get(self):
        """Retrieve all articles by the authenticated user"""

        args = authentication_parser.parse_args()
        header = authentication_header_parser(args['Authorization'])
        articles = (ArticleModel
                    .query
                    .filter(ArticleModel.author_id == header['userid'])
                    .order_by('id')
                    .all())

        if articles:
            return articles

        return '', http.client.NOT_FOUND

    @api_ns.doc('create_article')
    @api_ns.expect(article_parser)
    @api_ns.marshal_with(article_model, code=http.client.CREATED)
    def post(self):
        '''
        Create a new article
        '''
        args = article_parser.parse_args()
        header = authentication_header_parser(args['Authorization'])

        published = None

        if args['status'] == 'PUBLISHED':
            published = datetime.now()

        new_article = ArticleModel(
            slug=args['slug'],
            title=args['title'],
            content=args['content'],
            author_id=header['userid'],
            category_id=args['category_id'],
            status=args['status'],
            published=published
        )
        new_article.save_to_db()
        result = api_ns.marshal(new_article, article_model)

        return result, http.client.CREATED


@api_ns.route('/articles')
class Article(Resource):
    @api_ns.doc('list_articles')
    @api_ns.marshal_with(article_model)
    def get(self):
        '''
        Retrieves all articles
        '''
        articles = ArticleModel.find_all()
        return articles
