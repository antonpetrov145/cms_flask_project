from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash

from managers.auth import AuthManager
from db import db
from models.users import AdminUserModel


class AdminManager:
    @staticmethod
    def register(admin_data):
        admin_data["password"] = generate_password_hash(
            admin_data["password"], method="sha256"
        )
        admin = AdminUserModel(**admin_data)
        try:
            db.session.add(admin)
            db.session.flush()
        except Exception as e:
            if e.orig.pgcode == UNIQUE_VIOLATION:
                raise BadRequest("Please Login!")
            else:
                raise InternalServerError("Server not available!")
        return AuthManager.encode_token(admin)

    @staticmethod
    def login(data):
        try:
            admin = AdminUserModel.query.filter_by(email=data["email"]).first()
            if admin and check_password_hash(admin.password, data["password"]):
                return admin
            raise Exception
        except Exception:
            raise BadRequest("Check your email and password!")
