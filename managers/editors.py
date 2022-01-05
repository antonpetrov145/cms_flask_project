from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from managers.auth import AuthManager
from db import db
from models.users import EditorUserModel
from services.check_mail import CheckMail


class EditorManager:
    @staticmethod
    def register(editor_data):
        editor_data["password"] = generate_password_hash(
            editor_data["password"], method="sha256"
        )
        disposable = CheckMail(editor_data["email"])
        if disposable.check:
            raise BadRequest("You cannot use temporary mail! Please use a real one!")
        elif not disposable.check:
            editor = EditorUserModel(**editor_data)
            try:
                db.session.add(editor)
                db.session.flush()
            except Exception as e:
                if e.orig.pgcode == UNIQUE_VIOLATION:
                    raise BadRequest("Please login!")
                else:
                    raise InternalServerError("Server Unavailable!")
            return AuthManager.encode_token(editor)

    @staticmethod
    def login(data):
        try:
            author = EditorUserModel.query.filter_by(email=data["email"]).first()
            if author and check_password_hash(author.password, data["password"]):
                return author
            raise Exception
        except Exception:
            raise BadRequest("Check your email and password!")

    @staticmethod
    def delete(pk):
        user_pk = EditorUserModel.query.filter_by(pk=pk)
        user = user_pk.first()
        if not user:
            raise NotFound("User not found")

        db.session.delete(user)
        db.session.flush()
