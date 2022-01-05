import json
from flask_testing import TestCase
from config import create_app
from db import db


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
            ("PUT", "/posts/<int:pk>"),
            ("DELETE", "/posts/<int:pk>"),
        ]:
            if method == "PUT":
                resp = self.client.put(
                    url,
                    data=json.dumps({}),
                )
            elif method == "DELETE":
                resp = self.client.delete(url)
            self.assert401(resp, {"message": "Invalid or missing token"})
