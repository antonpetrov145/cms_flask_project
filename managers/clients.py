from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from managers.auth import AuthManager
from db import db
from models.users import ClientUserModel
from services.check_mail import CheckMail


class ClientManager:
    @staticmethod
    def register(client_data):
        client_data["password"] = generate_password_hash(
            client_data["password"], method="sha256"
        )
        if CheckMail(client_data["email"]) == True:
            raise BadRequest("You cannot use temporary mail! Please use a real one!")
        else:
            client = ClientUserModel(**client_data)
            try:
                db.session.add(client)
                db.session.flush()
            except Exception as e:
                if e.orig.pgcode == UNIQUE_VIOLATION:
                    raise BadRequest("Please login!")
                else:
                    raise InternalServerError("Server Unavailable!")
            return AuthManager.encode_token(client)

    @staticmethod
    def login(data):
        try:
            client = ClientUserModel.query.filter_by(email=data["email"]).first()
            if client and check_password_hash(client.password, data["password"]):
                return client
            raise Exception
        except Exception:
            raise BadRequest("Check your email and password!")

    @staticmethod
    def delete(pk):
        user_pk = ClientUserModel.query.filter_by(pk=pk)
        user = user_pk.first()
        if not user:
            raise NotFound("User not found")

        db.session.delete(user)
        db.session.flush()
