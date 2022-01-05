import json
import factory
from flask_testing import TestCase
from config import create_app
from db import db

from tests.base import generate_token
from tests.factories import AuthorFactory, ClientFactory, PostFactory


class TestApp(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_protected(self):
        for method, url in [
            ("PUT", "/posts/12"),
            ("DELETE", "/posts/12"),
            ("GET", "/authors/1/posts"),
            ("DELETE", "/authors/12"),
        ]:
            if method == "PUT":
                resp = self.client.put(
                    url,
                    data=json.dumps({}),
                )
            elif method == "DELETE":
                resp = self.client.delete(url)
            elif method == "GET":
                resp = self.client.get(url)
            self.assert401(resp, {"message": "Token is missing or invalid!"})

    def test_admin_rights(self):
        for method, url in [
            ("DELETE", "/authors/12"),
            ("DELETE", "/editors/12"),
        ]:
            author = AuthorFactory()
            token = generate_token(author)
            headers = {"Authorization": f"Bearer {token}"}
            if method == "DELETE":
                resp = self.client.delete(url, headers=headers)
            expected_message = {"message": "You don't have access for this request!"}
            self.assert_403(resp, expected_message)

    def test_client_rights(self):
        for method, url in [("GET", "/clients/1/posts")]:
            client = ClientFactory()
            token = generate_token(client)
            headers = {"Authorization": f"Bearer {token}"}
            if method == "GET":
                resp = self.client.get(url, headers=headers)
            self.assert200(resp)

    def test_regular_user_access(self):
        for method, url in [("GET", "/posts")]:
            if method == "GET":
                resp = self.client.get(url)
            self.assert200(resp)

    def test_post_create(self):
        for method, url in [("POST", "/posts")]:
            author = AuthorFactory()
            token = generate_token(author)
            headers = {"Authorization": f"Bearer {token}"}
            post = PostFactory()
            if method == "POST":
                resp = self.client.post(
                    url,
                    data=json.dumps(
                        {"title": post.title, "post_content": post.post_content}
                    ),
                    headers=headers,
                )
            self.assert200(resp)
