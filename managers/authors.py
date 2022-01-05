from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from managers.auth import AuthManager
from db import db
from models.users import AuthorUserModel
from services.check_mail import CheckMail


class AuthorManager:
    @staticmethod
    def register(author_data):
        author_data["password"] = generate_password_hash(
            author_data["password"], method="sha256"
        )
        if CheckMail(author_data["email"]) == True:
            raise BadRequest("You cannot use temporary mail! Please use a real one!")
        else:
            author = AuthorUserModel(**author_data)
            try:
                db.session.add(author)
                db.session.flush()
            except Exception as e:
                if e.orig.pgcode == UNIQUE_VIOLATION:
                    raise BadRequest("Please Login!")
                else:
                    raise InternalServerError("Server not available!")
            return AuthManager.encode_token(author)

    @staticmethod
    def login(data):
        try:
            author = AuthorUserModel.query.filter_by(email=data["email"]).first()
            if author and check_password_hash(author.password, data["password"]):
                return author
            raise Exception
        except Exception:
            raise BadRequest("Check your email and password!")

    @staticmethod
    def delete(pk):
        user_pk = AuthorUserModel.query.filter_by(pk=pk)
        user = user_pk.first()
        if not user:
            raise NotFound("User not found")

        db.session.delete(user)
        db.session.flush()
