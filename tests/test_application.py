import json
import factory
from flask_testing import TestCase
from config import create_app
from db import db

from tests.base import generate_token
from tests.factories import AuthorFactory, PostFactory


class TestApp(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def set_up(self):
        db.init_app(self.app)

    def tear_down(self):
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
