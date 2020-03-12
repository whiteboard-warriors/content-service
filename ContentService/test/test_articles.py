'''
Test the articles operations
Use the article_fixture to have data to retrieve,
it generates three articles
'''
from unittest.mock import ANY
import http.client
from .constants import PRIVATE_KEY
from contents import token_validation
from faker import Faker
fake = Faker()


def test_get_me_articles_unauthorized(client):
    response = client.get('/api/me/articles')
    assert http.client.UNAUTHORIZED == response.status_code


def test_get_me_articles_not_found(client):
    user_payload = {
        'userid': fake.random_int(2, 100),
        'username': fake.user_name(),
        'email': fake.email()
    }

    header = token_validation.generate_token_header(user_payload,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }

    response = client.get('/api/me/articles/', headers=headers)
    assert http.client.NOT_FOUND == response.status_code


def test_get_me_articles(client, article_fixture):
    user_payload = {
        'userid': 1,
        'username': 'whiteboardwarriors',
        'email': 'engineer@whiteboardwarriors.org'
    }

    header = token_validation.generate_token_header(user_payload,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }

    response = client.get('/api/me/articles', headers=headers)
    assert http.client.OK == response.status_code


def test_delete_me_article(client, article_fixture):
    article_id = article_fixture[0]
    user_payload = {
        'userid': 1,
        'username': 'whiteboardwarriors',
        'email': 'engineer@whiteboardwarriors.org'
    }

    header = token_validation.generate_token_header(user_payload,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }

    url = f'/api/me/article/{article_id}'
    response = client.delete(url, headers=headers)
    assert http.client.NO_CONTENT == response.status_code


def test_delete_me_article_noheader(client, article_fixture):
    article_id = article_fixture[1]

    url = f'/api/me/article/{article_id}'
    response = client.delete(url)
    assert http.client.UNAUTHORIZED == response.status_code


def test_delete_me_article_unauthorized(client, article_fixture):
    article_id = article_fixture[1]
    user_payload = {
        'userid': 2,
        'username': 'whiteboardwarriors',
        'email': 'engineer@whiteboardwarriors.org'
    }

    header = token_validation.generate_token_header(user_payload,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }

    url = f'/api/me/article/{article_id}'
    response = client.delete(url, headers=headers)
    assert http.client.UNAUTHORIZED == response.status_code


def test_delete_me_article_invalid_articleid(client, article_fixture):
    article_id = 1234455
    user_payload = {
        'userid': 2,
        'username': 'whiteboardwarriors',
        'email': 'engineer@whiteboardwarriors.org'
    }

    header = token_validation.generate_token_header(user_payload,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }

    url = f'/api/me/article/{article_id}'
    response = client.delete(url, headers=headers)
    assert http.client.NOT_FOUND == response.status_code


def test_create_me_articles_unauthorized(client):
    new_article = {
        'slug': fake.slug(),
        'title': fake.text(250),
        'content': fake.text(500),
        'category_id': fake.random_int(1, 3),
        'status': 'DRAFT'
    }
    response = client.post('/api/me/articles', data=new_article)
    assert http.client.UNAUTHORIZED == response.status_code


def test_create_me_article(client):
    new_article = {
        'slug': fake.slug(),
        'title': fake.text(250),
        'content': fake.text(500),
        'category_id': fake.random_int(1, 3),
        'status': 'DRAFT'
    }
    user_payload = {
        'userid': fake.random_int(2, 100),
        'username': fake.user_name(),
        'email': fake.email()
    }

    header = token_validation.generate_token_header(user_payload,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/articles', data=new_article,
                           headers=headers)
    result = response.json
    assert http.client.CREATED == response.status_code

    expected = {
        'id': ANY,
        'slug': new_article['slug'],
        'title': new_article['title'],
        'content': new_article['content'],
        'author_id': ANY,
        'category_id': new_article['category_id'],
        'status': new_article['status'],
        'published': ANY
    }
    assert result == expected


def test_list_articles(client, article_fixture):
    response = client.get('/api/articles')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the ids are increasing
    previous_id = -1
    for article in result:
        expected = {
            'id': ANY,
            'slug': ANY,
            'title': ANY,
            'content': ANY,
            'author_id': ANY,
            'category_id': ANY,
            'status': ANY,
            'published': ANY
        }
        assert expected == article
        assert article['id'] > previous_id
        previous_id = article['id']


def test_get_article(client, article_fixture):
    article_id = article_fixture[1]
    response = client.get(f'/api/articles/{article_id}')
    result = response.json

    assert http.client.OK == response.status_code
    assert 'title' in result
    assert 'content' in result
    assert 'category_id' in result
    assert 'slug' in result
    assert 'status' in result
    assert 'published' in result
    assert 'id' in result


def test_get_non_existing_article(client, article_fixture):
    article_id = 123456
    response = client.get(f'/api/article/{article_id}')
    result = response.json
    assert http.client.NOT_FOUND == response.status_code
    assert result == None
